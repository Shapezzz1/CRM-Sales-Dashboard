import pandas as pd
import sqlite3
import os
import re

# 1. Configuración Dinámica de Rutas
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_dir = os.path.join(project_root, 'data')
db_name = os.path.join(project_root, "crm_database.db")

csv_files = {
    "accounts": os.path.join(data_dir, "accounts.csv"),
    "data_dictionary": os.path.join(data_dir, "data_dictionary.csv"),
    "products": os.path.join(data_dir, "products.csv"),
    "sales_pipeline": os.path.join(data_dir, "sales_pipeline.csv"),
    "sales_teams": os.path.join(data_dir, "sales_teams.csv")
}

def clean_column_names(df):
    """
    Estandariza los nombres usando Regex para eliminar cualquier carácter extraño,
    acentos o espacios, dejándolo perfecto para SQL.
    """
    df.columns = [re.sub(r'[^a-z0-9_]', '_', c.strip().lower()) for c in df.columns]
    # Elimina guiones bajos múltiples si los hay
    df.columns = [re.sub(r'_+', '_', c).strip('_') for c in df.columns]
    return df

def run_etl():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    print(f"🔄 Iniciando proceso ETL Robusto hacia {os.path.basename(db_name)}...")

    for table_name, file_path in csv_files.items():
        if os.path.exists(file_path):
            print(f"   ➡️ Procesando: {table_name}...")
            
            try:
                # EXTRACT con manejo de errores
                df = pd.read_csv(file_path)
                
                # Validación de duplicados (Logging básico)
                duplicados = df.duplicated().sum()
                if duplicados > 0:
                    print(f"      ⚠️ Advertencia: Se encontraron {duplicados} filas duplicadas en {table_name}.")
                    # df = df.drop_duplicates() # Opcional: descomentar si quieres eliminarlos automáticamente

                # TRANSFORM: Limpieza de columnas con Regex
                df = clean_column_names(df)
                
                # TRANSFORM: Limpiar espacios en blanco en columnas de texto (Strip whitespaces)
                cols_texto = df.select_dtypes(include=['object']).columns
                for col in cols_texto:
                    df[col] = df[col].astype(str).str.strip()

                # Transformaciones específicas de la tabla de Hechos
                if table_name == "sales_pipeline":
                    # 1. Manejo de Fechas
                    cols_fecha = [c for c in df.columns if 'date' in c]
                    for col in cols_fecha:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    
                    # 2. Manejo de Nulos Numéricos (Lógica de Negocio)
                    # Si close_value es nulo, asumimos 0 para no sesgar sumatorias en Power BI
                    if 'close_value' in df.columns:
                        df['close_value'] = df['close_value'].fillna(0)
                        
                    # 3. Optimización de Memoria (Categorías)
                    if 'deal_stage' in df.columns:
                        df['deal_stage'] = df['deal_stage'].astype('category')

                # LOAD: Carga a SQLite
                # Nota: Mantenemos 'replace' por ser un proyecto estático, 
                # pero los tipos de datos nativos de pandas ayudan a SQLite.
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"      ✅ Cargadas {len(df)} filas exitosamente.")

            except pd.errors.EmptyDataError:
                print(f"      ❌ Error Crítico: El archivo {table_name}.csv está vacío.")
            except FileNotFoundError:
                print(f"      ❌ Error Crítico: No se pudo leer {table_name}.csv.")
            except Exception as e:
                print(f"      ❌ Error Inesperado al procesar {table_name}: {e}")
        else:
            print(f"      ❌ Archivo no encontrado en la ruta esperada: {file_path}")

    # Indexación para Performance SQL
    print("   🔨 Configurando índices de base de datos...")
    try:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pipeline_account ON sales_pipeline(account)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pipeline_product ON sales_pipeline(product)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pipeline_agent ON sales_pipeline(sales_agent)")
        conn.commit()
    except Exception as e:
        print(f"      ⚠️ No se pudieron crear los índices: {e}")

    conn.close()
    print("🚀 ¡ETL Finalizado con éxito!")

if __name__ == "__main__":
    run_etl()