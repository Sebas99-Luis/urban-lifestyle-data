# 🏢 Urban Lifestyle AB: Modern Data Stack Project

Este proyecto representa una solución integral de **Ingeniería de Datos (End-to-End)** diseñada para automatizar el análisis financiero y operativo de la empresa Urban Lifestyle AB. El objetivo principal es transformar datos crudos de Ventas, Inventario y Recursos Humanos en un **Dashboard de Rentabilidad Operativa (P&L)** dinámico.

---

## 🚀 1. Arquitectura del Proyecto

El proyecto utiliza un enfoque **ELT (Extract, Load, Transform)** moderno, integrando herramientas líderes en la industria para garantizar escalabilidad, calidad y automatización.



### 🛠️ Tech Stack
* **Data Warehouse:** [Google BigQuery](https://cloud.google.com/bigquery) (Cloud Storage & Compute).
* **Transformación de Datos:** [dbt (data build tool)](https://www.getdbt.com/) - Lógica de negocio y calidad.
* **Orquestación:** [Apache Airflow](https://airflow.apache.org/) (vía Astro CLI) - Automatización de procesos.
* **Contenedores:** [Docker](https://www.docker.com/) - Entorno de desarrollo aislado.
* **Visualización:** [Google Looker Studio](https://lookerstudio.google.com/) - BI & Reporting.

---

## 📊 2. Flujo de Datos (Data Pipeline)

El pipeline de datos está diseñado en capas para asegurar la integridad de la información:

1.  **Capa Bronze (Raw):** Ingesta de datos crudos en formato CSV/JSON a BigQuery.
2.  **Capa Silver (Staging):** Limpieza, normalización de tipos de datos y renombrado de columnas mediante dbt.
3.  **Capa Gold (Marts):** Aplicación de lógica de negocio compleja para el cálculo de márgenes, costos de nómina y beneficio neto final (`fct_business_profit`).



---

## ⚙️ 3. Instalación y Configuración

Siga estos pasos para replicar el entorno de desarrollo local:

### Requisitos Previos
* Docker Desktop.
* Astro CLI.
* Cuenta en Google Cloud Platform (GCP).

### Paso a Paso
1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/urban-lifestyle-data.git](https://github.com/tu-usuario/urban-lifestyle-data.git)
   cd urban-airflow

   Configurar Credenciales:

Coloque su archivo gcp_key.json (Service Account de GCP) en la carpeta dags/.

El proyecto está configurado para leer las credenciales desde la ruta interna de Docker: /usr/local/airflow/dags/gcp_key.json.

Levantar el Orquestador:

PowerShell
astro dev start
Acceder a las interfaces:

Airflow: http://localhost:8080 (User: admin / Pass: admin)

BigQuery: Consola de GCP.

## 📈 4. Visualización y Business Intelligence
El resultado final es un Dashboard interactivo que permite a la gerencia monitorear:

KPIs Globales: Ingresos Totales, Margen Bruto y Beneficio Neto.

Análisis por Tienda: Comparativa de rentabilidad real (Ventas vs Costos Operativos).

Tendencias: Evolución temporal de ingresos frente a gastos de personal.

## 🔒 5. Seguridad y Calidad
Tests de dbt: Se ejecutan validaciones automáticas de unicidad, valores no nulos y relaciones de integridad referencial.

Seguridad: El archivo de credenciales gcp_key.json está excluido del control de versiones mediante .gitignore.

Desarrollado por: [Tu Nombre/Empresa] Estado del Proyecto: ✅ Desplegado y Operativo


---

### 💡 Próximo Paso:
Este es el **Punto 1** del checklist. ¿Te gustaría que preparemos ahora el **Punto 2: El Diccionario de Datos y Lineage de dbt**? (Este es fundamental para que el cliente entienda exactamente de dónde sale cada número del P&L).
