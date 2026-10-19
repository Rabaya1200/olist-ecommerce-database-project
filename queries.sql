
-- Task 4: SQL Query & Business Analysis
-- Student Name: Rita Rabaya Jahan
-- Dataset: Brazilian E-Commerce (Olist)


-- Query 1: Customer order statistics within a time range
SELECT 
    DATE_TRUNC('month', order_purchase_timestamp) AS order_month,
    COUNT(o.order_id) AS total_orders,
    SUM(p.payment_value) AS total_revenue
FROM olist_orders o
JOIN olist_order_payments p ON o.order_id = p.order_id
WHERE order_purchase_timestamp BETWEEN '2017-01-01' AND '2017-12-31'
GROUP BY DATE_TRUNC('month', order_purchase_timestamp)
ORDER BY order_month;

-- Query 2: Top-selling product ranking
SELECT 
    p.product_category_name, 
    COUNT(*) AS times_sold
FROM olist_order_items i
JOIN olist_products p ON i.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY times_sold DESC
LIMIT 10;

-- Query 3: Multi-table join query for order detail with customer and product info
SELECT 
    o.order_id, 
    c.customer_city, 
    p.product_category_name, 
    i.price
FROM olist_orders o
JOIN olist_customers c ON o.customer_id = c.customer_id
JOIN olist_order_items i ON o.order_id = i.order_id
JOIN olist_products p ON i.product_id = p.product_id
LIMIT 100;

-- Query 4: Aggregate analysis of sales by category
SELECT 
    p.product_category_name, 
    SUM(i.price) AS total_sales
FROM olist_order_items i
JOIN olist_products p ON i.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_sales DESC;

-- Query 5: Subquery to find high-value customers
SELECT customer_id, total_spent
FROM (
    SELECT o.customer_id, SUM(p.payment_value) AS total_spent
    FROM olist_orders o
    JOIN olist_order_payments p ON o.order_id = p.order_id
    GROUP BY o.customer_id
) AS customer_totals
WHERE total_spent > (SELECT AVG(payment_value) FROM olist_order_payments);

-- Query 6: Create view for frequently used statistical data
CREATE VIEW monthly_sales_summary AS
SELECT 
    DATE_TRUNC('month', order_purchase_timestamp) AS month,
    COUNT(o.order_id) AS total_orders,
    SUM(p.payment_value) AS revenue
FROM olist_orders o
JOIN olist_order_payments p ON o.order_id = p.order_id
GROUP BY DATE_TRUNC('month', order_purchase_timestamp)
ORDER BY month;

-- Test the view:
SELECT * FROM monthly_sales_summary LIMIT 5;

-- Query 7: Stored function (PostgreSQL equivalent of a stored procedure) for order query
CREATE OR REPLACE FUNCTION get_order_details(input_order_id VARCHAR)
RETURNS SETOF olist_orders
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM olist_orders WHERE order_id = input_order_id;
END;
$$;

-- Test the function:
SELECT * FROM get_order_details('00010242fe8c5a6d1ba2dd792cb16214');

-- Query 8: Query with filter conditions and sorting
SELECT 
    order_id, 
    order_status, 
    order_purchase_timestamp
FROM olist_orders
WHERE order_status = 'delivered'
ORDER BY order_purchase_timestamp DESC
LIMIT 50;