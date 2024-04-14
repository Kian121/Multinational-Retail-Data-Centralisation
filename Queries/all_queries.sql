-- Queries

-- How many stores does the business have and in wich countires?

SELECT country_code AS country, COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY country_code
ORDER BY total_no_stores DESC

-- Which locations currently have the most stores?

SELECT locality, COUNT(*) AS total_no_stores
FROM dim_store_details
GROUP BY locality
ORDER BY total_no_stores DESC
LIMIT 7;

-- Which month produced the largest amount of sales?

SELECT SUM(ot.product_quantity * dp.product_price) AS total_sales, dt.month
FROM orders_table ot
JOIN dim_date_times dt ON ot.date_uuid = dt.date_uuid
JOIN dim_products dp ON ot.product_code = dp.product_code
GROUP BY dt.month
ORDER BY total_sales DESC
LIMIT 6;

-- How many sales are coming from online?

SELECT 
    COUNT(*) AS numbers_of_sales, 
    SUM(product_quantity) AS product_quantity_count, 
    CASE 
        WHEN store_code LIKE 'WEB%' THEN 'web'
        ELSE 'offline'
    END AS location
FROM orders_table
GROUP BY 
    CASE 
        WHEN store_code LIKE 'WEB%' THEN 'web'
        ELSE 'offline'
    END;

-- What percentage of sale come through each type of store?

WITH TotalSales AS (
    SELECT
        SUM(ot.product_quantity * dp.product_price) as Total
    FROM
        orders_table ot
    INNER JOIN
        dim_products dp ON ot.product_code = dp.product_code
),
SalesByType AS (
    SELECT
        CASE 
            WHEN ot.store_code LIKE 'WEB%' THEN 'Web portal'
            ELSE dsd.store_type
        END AS store_type,
        SUM(ot.product_quantity * dp.product_price) AS total_sales
    FROM
        orders_table ot
    INNER JOIN
        dim_products dp ON ot.product_code = dp.product_code
    LEFT JOIN
        dim_store_details dsd ON ot.store_code = dsd.store_code
    GROUP BY
        CASE 
            WHEN ot.store_code LIKE 'WEB%' THEN 'Web portal'
            ELSE dsd.store_type
        END
)
SELECT
    sbt.store_type,
    sbt.total_sales,
    TRUNC((sbt.total_sales / (SELECT Total FROM TotalSales) * 100)::numeric, 2) AS percentage_total
FROM
    SalesByType sbt
ORDER BY
    sbt.total_sales DESC;

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

-- What is our staff headcount?

SELECT 
    SUM(staff_numbers) AS total_staff_numbers, 
    country_code
FROM 
    dim_store_details
GROUP BY 
    country_code
ORDER BY 
    total_staff_numbers DESC;

-- Which German store type is selling the most?

SELECT 
    SUM(ot.product_quantity * dp.product_price) AS total_sales, 
    dsd.store_type, 
    dsd.country_code
FROM 
    orders_table ot
JOIN 
    dim_store_details dsd ON ot.store_code = dsd.store_code
JOIN 
    dim_products dp ON ot.product_code = dp.product_code
WHERE 
    dsd.country_code = 'DE'
GROUP BY 
    dsd.store_type, dsd.country_code
ORDER BY 
    total_sales ASC;

-- How quickly is the company making sales?

SELECT
    year,
    CONCAT(
        '"hours": ', ROUND(AVG(diff) / 3600),
        ', "minutes": ', ROUND((AVG(diff) % 3600) / 60),
        ', "seconds": ', ROUND(AVG(diff) % 60),
        ', "milliseconds": ', ROUND(AVG(diff * 1000) % 1000)
    ) AS actual_time_taken
FROM (
    SELECT
        dt.year,
        EXTRACT(EPOCH FROM LEAD(TO_TIMESTAMP(dt.year || '-' || LPAD(dt.month, 2, '0') || '-' || LPAD(dt.day, 2, '0') || ' ' || dt.timestamp, 'YYYY-MM-DD HH24:MI:SS'), 1) OVER (PARTITION BY dt.year ORDER BY TO_TIMESTAMP(dt.year || '-' || LPAD(dt.month, 2, '0') || '-' || LPAD(dt.day, 2, '0') || ' ' || dt.timestamp, 'YYYY-MM-DD HH24:MI:SS'))) - 
        EXTRACT(EPOCH FROM TO_TIMESTAMP(dt.year || '-' || LPAD(dt.month, 2, '0') || '-' || LPAD(dt.day, 2, '0') || ' ' || dt.timestamp, 'YYYY-MM-DD HH24:MI:SS')) AS diff
    FROM
        orders_table ot
    JOIN
        dim_date_times dt ON ot.date_uuid = dt.date_uuid
) AS subquery
WHERE
    subquery.diff IS NOT NULL
GROUP BY
    year
ORDER BY
    AVG(diff) DESC
LIMIT 5;


-- End






