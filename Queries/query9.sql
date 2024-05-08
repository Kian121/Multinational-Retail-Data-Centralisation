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












