import sqlite3

conn = sqlite3.connect("uf.db")
cursor = conn.cursor()

print("Antes de limpiar:")
rows = cursor.execute("SELECT * FROM uf LIMIT 5").fetchall()
print(rows)
cursor.execute("DELETE FROM uf WHERE periodo IS NULL OR uf IS NULL OR periodo = 'Periodo';")

conn.commit()
print("\nDespués de limpiar:")
rows = cursor.execute("SELECT * FROM uf LIMIT 5").fetchall()
print(rows)

conn.close()

print("\nBase de datos limpiada correctamente.")
