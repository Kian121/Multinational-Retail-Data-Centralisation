SELECT SUM(ot.product_quantity * dp.product_price) AS total_sales, dt.month
FROM orders_table ot
JOIN dim_date_times dt ON ot.date_uuid = dt.date_uuid
JOIN dim_products dp ON ot.product_code = dp.product_code
GROUP BY dt.month
ORDER BY total_sales DESC
LIMIT 6;



