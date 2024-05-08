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


