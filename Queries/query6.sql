-- Which month in each year produced the highest cost of sales?

SELECT 
    CAST(SUM(dp.product_price * ot.product_quantity) AS NUMERIC(10, 2)) AS total_sales, 
    ddt.year, 
    ddt.month
FROM 
    orders_table ot
JOIN 
    dim_products dp ON ot.product_code = dp.product_code
JOIN 
    dim_date_times ddt ON ot.date_uuid = ddt.date_uuid
GROUP BY 
    ddt.year, ddt.month
ORDER BY 
    total_sales DESC
LIMIT 10;
