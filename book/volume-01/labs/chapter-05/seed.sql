SET search_path TO ecommerce_ch05, public;
INSERT INTO customers(id,name) VALUES (101,'Customer A'),(102,'Customer B');
INSERT INTO inventory(sku_id,on_hand,reserved) VALUES (1001,1,0),(1002,5,0);
