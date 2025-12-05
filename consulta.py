import sqlite3

DB_FILE = "uf.db"

def obtener_uf_por_fecha(fecha):
    fecha = fecha + " 00:00:00"
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT valor_uf FROM uf WHERE periodo = ?", (fecha,))
    resultado = c.fetchone()
    conn.close()
    return resultado[0] if resultado else None








