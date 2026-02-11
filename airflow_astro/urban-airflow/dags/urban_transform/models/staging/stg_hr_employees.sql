WITH source AS (
    SELECT * FROM {{ source('raw_urban_source', 'raw_hr_master') }}
)

SELECT
    Employee_ID AS employee_id,
    -- Unimos nombre y apellido
    CONCAT(First_Name, ' ', Last_Name) AS employee_name,
    Role AS role,
    Department_Store AS store_name,
    CAST(Contracted_Hours AS INT64) AS contracted_hours,
    CAST(Hourly_Base_Wage AS FLOAT64) AS hourly_wage
FROM source