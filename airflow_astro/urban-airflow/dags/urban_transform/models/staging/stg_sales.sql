WITH source AS (
    SELECT * FROM {{ source('raw_urban_source', 'raw_sales') }}
),

renamed_and_cleaned AS (
    SELECT
        tx_id AS transaction_id,
        store AS store_name,
        prod AS product_id,
        CAST(qty AS INT64) AS quantity,
        -- Limpieza de precio: quitamos 'kr', 'SEK', etc.
        CAST(REGEXP_REPLACE(price, r'[^\d.]', '') AS FLOAT64) AS sale_amount,
        -- Formateo de fecha
        PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', REPLACE(ts, '/', '-')) AS sale_timestamp,
        pay_type AS payment_method
    FROM source
)

SELECT * FROM renamed_and_cleaned