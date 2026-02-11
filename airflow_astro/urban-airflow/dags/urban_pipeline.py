from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configuración básica
default_args = {
    'owner': 'urban_lifestyle',
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Definición del DAG
with DAG(
    dag_id='urban_lifestyle_v3',  # Cambié el nombre a v3 para forzar que aparezca
    default_args=default_args,
    description='Pipeline ETL Moderno',
    # --- CAMBIO CRÍTICO: Usamos 'schedule', NUNCA 'schedule_interval' ---
    schedule='@daily', 
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['dbt'],
) as dag:

    # Tarea 1: Ejecutar dbt run
    t1 = BashOperator(
        task_id='dbt_run',
        bash_command='cd /usr/local/airflow/dags/urban_transform && dbt run --profiles-dir .',
    )

    # Tarea 2: Ejecutar dbt test
    t2 = BashOperator(
        task_id='dbt_test',
        bash_command='cd /usr/local/airflow/dags/urban_transform && dbt test --profiles-dir .',
    )

    # Orden de ejecución
    t1 >> t2