import os
import glob
import json
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# --- CONFIGURACIÓN ---
# Ajusta esto si tu archivo se llama diferente
KEY_PATH = "gcp_credentials.json"
PROJECT_ID = "urban-lifestyle-data"
DATASET_ID = "raw_data_urban"

print(f"🔑 Iniciando cliente BigQuery...")

# Verificar credenciales
if not os.path.exists(KEY_PATH):
    print(f"❌ ERROR: No encuentro {KEY_PATH}. Asegúrate de estar en la carpeta raíz.")
    exit()

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)


def upload_to_bq(df, table_name):
    """
    Sube un DataFrame a BigQuery como STRING (Raw Data).
    """
    try:
        # Forzamos todo a string para evitar errores de tipo ahora.
        # La limpieza de tipos (INT, DATE) se hará luego con SQL/DBT.
        df = df.astype(str)

        table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",  # Borra y escribe de nuevo
            source_format=bigquery.SourceFormat.CSV,
            autodetect=True,
        )

        print(f"   ⬆️ Subiendo {table_name} ({len(df)} filas)...")
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

        job.result()  # Esperar a que termine
        print(f"   ✅ Tabla creada exitosamente: {table_id}")

    except Exception as e:
        print(f"   ❌ Error subiendo {table_name}: {e}")


# ==========================================
# 1. VENTAS (Miles de CSVs)
# ==========================================
print("\n📦 PROCESANDO VENTAS...")
sales_files = glob.glob("data/raw/sales/*.csv")

if sales_files:
    # Leemos solo los primeros 5 archivos para probar (o quita [:5] para leer todos)
    # Recomendación: Lee todos, tardará unos segundos.
    df_list = [pd.read_csv(f) for f in sales_files]
    df_total_sales = pd.concat(df_list, ignore_index=True)

    print(
        f"   -> Unificados {len(sales_files)} archivos. Total filas: {len(df_total_sales)}"
    )
    upload_to_bq(df_total_sales, "raw_sales")
else:
    print("   ⚠️ No se encontraron archivos de ventas.")

# ==========================================
# 2. INVENTARIO (JSON)
# ==========================================
print("\n📦 PROCESANDO INVENTARIO...")
json_path = "data/raw/inventory/products.json"

if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    df_inv = pd.DataFrame(data)
    upload_to_bq(df_inv, "raw_inventory")
else:
    print("   ⚠️ No existe products.json")

# ==========================================
# 3. FINANZAS (CSV)
# ==========================================
print("\n📦 PROCESANDO GASTOS...")
fin_path = "data/raw/finances/expenses_2024.csv"
if os.path.exists(fin_path):
    df_fin = pd.read_csv(fin_path)
    upload_to_bq(df_fin, "raw_expenses")

# ==========================================
# 4. RRHH (Excel)
# ==========================================
print("\n📦 PROCESANDO RRHH...")
# Master
master_path = "data/raw/hr/employee_master_list.xlsx"
if os.path.exists(master_path):
    df_master = pd.read_excel(master_path)
    upload_to_bq(df_master, "raw_hr_master")

# Nóminas
payroll_files = glob.glob("data/raw/hr/*_payroll/*.xlsx")
if payroll_files:
    df_pay_list = [pd.read_excel(f) for f in payroll_files]
    df_total_pay = pd.concat(df_pay_list, ignore_index=True)
    upload_to_bq(df_total_pay, "raw_hr_payroll")

print("\n🎉 ¡CARGA COMPLETA! Revisa BigQuery.")
