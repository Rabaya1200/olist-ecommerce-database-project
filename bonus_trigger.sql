Implement Trigger for Data Integrity


-- 1. Create the function
CREATE OR REPLACE FUNCTION check_positive_price()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.price < 0 THEN
        RAISE EXCEPTION 'Error: Price cannot be negative! You entered: %', NEW.price;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2. Create the trigger
CREATE TRIGGER trg_check_positive_price
BEFORE INSERT OR UPDATE ON olist_order_items
FOR EACH ROW
EXECUTE FUNCTION check_positive_price();




Test the Trigger (Prove it works)

INSERT INTO olist_order_items (order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value)
VALUES ('test_order_id', 1, 'test_product_id', 'test_seller_id', NOW(), -10.00, 5.00);