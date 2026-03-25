# Dashboard de Ventas B2B y Análisis de CRM

## De qué trata este proyecto
Básicamente, armé un proyecto de Business Intelligence (End-to-End) para evaluar cómo viene rindiendo la fuerza de ventas y monitorear la salud del pipeline comercial. 

El problema que resuelve es el clásico de cualquier empresa: transformar datos crudos del CRM en decisiones de negocio reales. En lugar de tener planillas sueltas o datos sucios, este sistema toma la información, la limpia, la guarda de forma estructurada y la muestra en un panel interactivo. Esto le permite a cualquier stakeholder ver tasas de conversión precisas, identificar a los managers que mejor rinden y analizar las tendencias de facturación.

## Cómo funciona

El flujo del proyecto simula un entorno de datos profesional y se divide en tres partes:

1. Data Engineering (ETL con Python): Armé un script que se encarga de la extracción y transformación de datos. Usa Pandas y Expresiones Regulares (Regex) para limpiar el texto, normalizar las columnas y atajar los valores nulos de los archivos crudos.
2. Data Warehousing (SQLite): Los datos limpios no quedan en el aire, se cargan en una base de datos relacional. La diseñé optimizada con índices para que las consultas vuelen.
3. Modelado y Visualización (Power BI): Conecté la base de datos a Power BI armando un modelo de Estrella (conectando la tabla de hechos del pipeline con las dimensiones de cuentas, productos y equipos). Sobre eso, metí medidas DAX avanzadas para calcular los KPIs dinámicos.

## Stack Tecnológico

* Lenguaje ETL: Python (Pandas, re)
* Base de Datos: SQLite
* Visualización y Modelado: Power BI (DAX, Star Schema)

## Archivos del repo

* /data: Carpeta con los archivos CSV originales crudos.
* /script/etl_pipeline.py: El script de Python que hace toda la magia de limpieza y transformación.
* crm_database.db: La base de datos SQLite ya consolidada y lista para usar.
* Dashboard_Ventas.pbix: El archivo de Power BI con el panel interactivo.
* Dashboard_Preview.pdf: Una captura estática por si querés ver cómo quedó el dashboard sin tener que abrir Power BI.
