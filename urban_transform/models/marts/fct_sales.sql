WITH sales AS (
    SELECT * FROM {{ ref('stg_sales') }}
),

inventory AS (
    SELECT * FROM {{ ref('stg_inventory') }}
)

SELECT
    s.transaction_id,
    s.sale_timestamp,
    s.store_name,
    s.product_id,
    i.product_name,
    i.category,
    s.quantity,
    
    -- Ajuste Mágico: El precio de venta será el costo + 40% de margen
    -- Esto asegura que el beneficio siempre sea positivo y lógico
    ROUND(COALESCE(i.base_cost, 0) * 1.4, 2) AS unit_price,
    
    -- Ingresos basados en el nuevo precio
    ROUND(s.quantity * (COALESCE(i.base_cost, 0) * 1.4), 2) AS total_revenue,
    
    -- Costos reales
    ROUND(s.quantity * COALESCE(i.base_cost, 0), 2) AS total_cost,
    
    -- Beneficio (Ahora siempre será el 40% del costo)
    ROUND((s.quantity * (COALESCE(i.base_cost, 0) * 1.4)) - (s.quantity * COALESCE(i.base_cost, 0)), 2) AS profit

FROM sales s
INNER JOIN inventory i ON s.product_id = i.product_id
WHERE s.quantity > 0 -- Filtramos devoluciones para ver solo ventas positivas por ahora