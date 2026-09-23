-- INSIDE E-COMMERCE, Chapter 03 — Hoàng Marketplace educational schema.
-- Target: PostgreSQL (modern supported version); run in a NEW EMPTY database.
-- Scope: one seller order / seller / checkout; one reservation / order item / warehouse.
-- See README.md for architectural simplifications and test scenarios.

BEGIN;

CREATE TABLE sellers (
    seller_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seller_name TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PENDING', 'APPROVED', 'SUSPENDED'))
);

CREATE TABLE products (
    product_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_name TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('DRAFT', 'ACTIVE', 'ARCHIVED'))
);

CREATE TABLE product_variants (
    variant_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES products(product_id),
    sku_code TEXT NOT NULL UNIQUE,
    color TEXT NOT NULL,
    capacity TEXT NOT NULL,
    UNIQUE (product_id, color, capacity)
);

CREATE TABLE warehouses (
    warehouse_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seller_id BIGINT NOT NULL REFERENCES sellers(seller_id),
    warehouse_name TEXT NOT NULL,
    UNIQUE (warehouse_id, seller_id)
);

CREATE TABLE seller_offers (
    offer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seller_id BIGINT NOT NULL REFERENCES sellers(seller_id),
    variant_id BIGINT NOT NULL REFERENCES product_variants(variant_id),
    unit_price NUMERIC(18, 2) NOT NULL CHECK (unit_price >= 0),
    currency CHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    status TEXT NOT NULL CHECK (status IN ('DRAFT','ACTIVE','PAUSED')),
    UNIQUE (offer_id, seller_id),
    UNIQUE (seller_id, variant_id)
);

CREATE TABLE inventory_stock (
    offer_id BIGINT NOT NULL,
    seller_id BIGINT NOT NULL,
    warehouse_id BIGINT NOT NULL,
    on_hand_quantity INTEGER NOT NULL CHECK (on_hand_quantity >= 0),
    reserved_quantity INTEGER NOT NULL DEFAULT 0 CHECK (reserved_quantity >= 0),
    PRIMARY KEY (offer_id, warehouse_id),
    FOREIGN KEY (offer_id, seller_id)
        REFERENCES seller_offers(offer_id, seller_id),
    FOREIGN KEY (warehouse_id, seller_id)
        REFERENCES warehouses(warehouse_id, seller_id),
    CHECK (reserved_quantity <= on_hand_quantity)
);

CREATE TABLE order_groups (
    order_group_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    idempotency_key TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PENDING_PAYMENT','PAID','CANCELLED','PARTIAL')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (customer_id, idempotency_key)
);

CREATE TABLE seller_orders (
    seller_order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_group_id BIGINT NOT NULL REFERENCES order_groups(order_group_id),
    seller_id BIGINT NOT NULL REFERENCES sellers(seller_id),
    status TEXT NOT NULL CHECK (status IN
        ('PENDING_PAYMENT','PAID','FULFILLING','SHIPPED','DELIVERED','CANCELLED')),
    UNIQUE (order_group_id, seller_id),
    UNIQUE (seller_order_id, seller_id)
);

CREATE TABLE order_items (
    order_item_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    seller_order_id BIGINT NOT NULL,
    seller_id BIGINT NOT NULL,
    offer_id BIGINT NOT NULL,
    sku_code_snapshot TEXT NOT NULL,
    title_snapshot TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_snapshot NUMERIC(18,2) NOT NULL CHECK (unit_price_snapshot >= 0),
    currency CHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    FOREIGN KEY (seller_order_id, seller_id)
        REFERENCES seller_orders(seller_order_id, seller_id),
    FOREIGN KEY (offer_id, seller_id)
        REFERENCES seller_offers(offer_id, seller_id),
    UNIQUE (order_item_id, offer_id)
);

CREATE TABLE stock_reservations (
    reservation_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_item_id BIGINT NOT NULL UNIQUE,
    offer_id BIGINT NOT NULL,
    warehouse_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    status TEXT NOT NULL CHECK (status IN ('ACTIVE','CONFIRMED','RELEASED','EXPIRED')),
    expires_at TIMESTAMPTZ NOT NULL,
    FOREIGN KEY (order_item_id, offer_id)
        REFERENCES order_items(order_item_id, offer_id),
    FOREIGN KEY (offer_id, warehouse_id)
        REFERENCES inventory_stock(offer_id, warehouse_id)
);

CREATE TABLE payment_attempts (
    payment_attempt_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_group_id BIGINT NOT NULL REFERENCES order_groups(order_group_id),
    idempotency_key TEXT NOT NULL,
    provider TEXT NOT NULL,
    provider_reference TEXT,
    status TEXT NOT NULL CHECK (status IN ('PENDING','SUCCEEDED','FAILED','UNKNOWN')),
    amount NUMERIC(18,2) NOT NULL CHECK (amount > 0),
    currency CHAR(3) NOT NULL CHECK (currency ~ '^[A-Z]{3}$'),
    UNIQUE (order_group_id, idempotency_key),
    UNIQUE (provider, provider_reference)
);

CREATE INDEX idx_offers_variant_status ON seller_offers (variant_id, status);
CREATE INDEX idx_inventory_warehouse ON inventory_stock (warehouse_id);
CREATE INDEX idx_order_groups_customer_created ON order_groups (customer_id, created_at DESC);
CREATE INDEX idx_seller_orders_seller ON seller_orders (seller_id, status);
CREATE INDEX idx_stock_reservations_expiry ON stock_reservations (expires_at)
    WHERE status = 'ACTIVE';

COMMIT;
