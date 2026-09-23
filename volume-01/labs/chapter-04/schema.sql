-- Inside E-commerce / Chapter 04 / PostgreSQL teaching schema
-- Run on a disposable PostgreSQL database: psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f schema.sql
-- This is a bounded lab schema; not a complete multi-currency, tax, invoicing or ledger design.
BEGIN;
DROP SCHEMA IF EXISTS ecommerce_pricing_lab CASCADE;
CREATE SCHEMA ecommerce_pricing_lab;
SET search_path TO ecommerce_pricing_lab;

CREATE TABLE seller (
    id BIGINT PRIMARY KEY,
    display_name TEXT NOT NULL
);
CREATE TABLE product_variant (
    id BIGINT PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    product_name TEXT NOT NULL,
    variant_label TEXT NOT NULL
);
CREATE TABLE seller_offer (
    id BIGINT PRIMARY KEY,
    seller_id BIGINT NOT NULL REFERENCES seller(id),
    variant_id BIGINT NOT NULL REFERENCES product_variant(id),
    active_price NUMERIC(18,0) NOT NULL CHECK (active_price >= 0),
    currency CHAR(3) NOT NULL DEFAULT 'VND' CHECK (currency = 'VND'),
    price_version BIGINT NOT NULL DEFAULT 1 CHECK (price_version >= 1),
    status TEXT NOT NULL CHECK (status IN ('DRAFT','ACTIVE','PAUSED','ENDED')),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (seller_id, variant_id)
);
CREATE TABLE offer_price_history (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    offer_id BIGINT NOT NULL REFERENCES seller_offer(id),
    price_version BIGINT NOT NULL,
    amount NUMERIC(18,0) NOT NULL CHECK (amount >= 0),
    currency CHAR(3) NOT NULL DEFAULT 'VND' CHECK (currency = 'VND'),
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (offer_id, price_version)
);
CREATE TABLE promotion_budget (
    promotion_id BIGINT PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    usage_limit INTEGER NOT NULL CHECK (usage_limit > 0),
    reserved_uses INTEGER NOT NULL DEFAULT 0 CHECK (reserved_uses >= 0),
    consumed_uses INTEGER NOT NULL DEFAULT 0 CHECK (consumed_uses >= 0),
    CHECK (reserved_uses + consumed_uses <= usage_limit)
);
CREATE TABLE customer_order (
    id BIGINT PRIMARY KEY,
    buyer_id BIGINT NOT NULL,
    currency CHAR(3) NOT NULL CHECK (currency = 'VND'),
    payable_total NUMERIC(18,0) NOT NULL CHECK (payable_total >= 0),
    status TEXT NOT NULL CHECK (status IN ('PENDING_PAYMENT','PAID','CANCELLED')),
    checkout_request_key TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (buyer_id, checkout_request_key)
);
CREATE TABLE order_item_snapshot (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES customer_order(id),
    offer_id BIGINT NOT NULL REFERENCES seller_offer(id),
    product_name_snapshot TEXT NOT NULL,
    variant_label_snapshot TEXT NOT NULL,
    unit_price_snapshot NUMERIC(18,0) NOT NULL CHECK (unit_price_snapshot >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    allocated_discount NUMERIC(18,0) NOT NULL DEFAULT 0 CHECK (allocated_discount >= 0),
    net_line_amount NUMERIC(18,0) NOT NULL CHECK (net_line_amount >= 0),
    currency CHAR(3) NOT NULL CHECK (currency = 'VND'),
    price_version BIGINT NOT NULL,
    CHECK (net_line_amount = unit_price_snapshot * quantity - allocated_discount),
    CHECK (allocated_discount <= unit_price_snapshot * quantity)
);
CREATE TABLE promotion_redemption (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    promotion_id BIGINT NOT NULL REFERENCES promotion_budget(promotion_id),
    buyer_id BIGINT NOT NULL,
    request_key TEXT NOT NULL,
    order_id BIGINT REFERENCES customer_order(id),
    status TEXT NOT NULL CHECK (status IN ('RESERVED','CONSUMED','RELEASED')),
    UNIQUE (promotion_id, buyer_id, request_key)
);
CREATE INDEX order_item_snapshot_order_idx ON order_item_snapshot(order_id);
CREATE INDEX offer_price_history_offer_idx ON offer_price_history(offer_id, price_version DESC);
COMMIT;
