import pandas as pd
import sqlite3

DB_FILE = "uf.db"
EXCEL_FILE = "UF_IVP_DIARIO (1).xlsx"

def cargar_uf():
    print("Cargando archivo Excel...")
    df_raw = pd.read_excel(EXCEL_FILE, header=None)
    df = df_raw.iloc[2:].copy()
    df.columns = ["periodo", "valor_uf"]
    
    df["periodo"] = pd.to_datetime(df["periodo"], errors="coerce")
    df["valor_uf"] = pd.to_numeric(df["valor_uf"], errors="coerce")

    df = df.dropna()

    print("Datos procesados:")
    print(df.head())

    
    conn = sqlite3.connect(DB_FILE)
    conn.execute("DROP TABLE IF EXISTS uf")
    conn.execute("""
        CREATE TABLE uf (
            periodo TEXT PRIMARY KEY,
            valor_uf REAL
        )
    """)

    df.to_sql("uf", conn, if_exists="append", index=False)
    conn.close()

    print("UF cargada correctamente en uf.db ")









