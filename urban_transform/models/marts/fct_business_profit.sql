WITH store_sales AS (
    -- Sumamos el beneficio por tienda
    SELECT 
        store_name,
        SUM(total_revenue) AS total_revenue,
        SUM(profit) AS sales_profit
    FROM {{ ref('fct_sales') }}
    GROUP BY 1
),

store_payroll AS (
    -- Sumamos el costo de personal por tienda
    -- Unimos el payroll con employees para saber de qué tienda es cada pago
    SELECT 
        e.store_name,
        SUM(p.total_company_cost) AS total_hr_cost
    FROM {{ ref('stg_hr_payroll') }} p
    JOIN {{ ref('stg_hr_employees') }} e ON p.employee_id = e.employee_id
    GROUP BY 1
)

SELECT
    s.store_name,
    s.total_revenue,
    s.sales_profit,
    COALESCE(p.total_hr_cost, 0) AS hr_expenses,
    -- El beneficio neto real del negocio
    (s.sales_profit - COALESCE(p.total_hr_cost, 0)) AS final_net_profit
FROM store_sales s
LEFT JOIN store_payroll p ON s.store_name = p.store_name
ORDER BY final_net_profit DESC