WITH source AS (
    SELECT * FROM {{ source('raw_urban_source', 'raw_hr_payroll') }}
)

SELECT
    Employee_ID AS employee_id,
    Payment_Date AS payroll_date,
    Payroll_Period AS payroll_period,
    CAST(Total_Hours AS FLOAT64) AS hours_worked,
    CAST(Gross_Salary AS FLOAT64) AS gross_salary,
    -- Usamos backticks para la columna con guion
    CAST(Total_Cost_Company AS FLOAT64) AS total_company_cost
FROM source