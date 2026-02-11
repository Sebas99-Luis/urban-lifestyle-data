WITH source AS (
    SELECT * FROM {{ source('raw_urban_source', 'raw_inventory') }}
),

cleaned AS (
    SELECT
        -- IDs y nombres básicos
        id AS product_id,
        name AS product_name,
        category,
        
        -- El costo estaba fuera del JSON, lo convertimos a número decimal
        CAST(cost AS FLOAT64) AS base_cost,
        
        -- Extraemos los campos que sí están dentro del objeto 'details'
        -- Usamos JSON_EXTRACT_SCALAR para obtener el valor como texto
        JSON_EXTRACT_SCALAR(details, '$.supplier') AS supplier,
        JSON_EXTRACT_SCALAR(details, '$.origin') AS origin,
        
        -- Stock actual (fuera del JSON)
        CAST(stock AS INT64) AS current_stock
    FROM source
)

SELECT * FROM cleaned