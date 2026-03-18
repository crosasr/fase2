import sqlite3

# ======================
# Crear BD y poblar datos
# ======================
conn   = sqlite3.connect("inventario.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre    TEXT    NOT NULL,
        precio    REAL    NOT NULL,
        stock     INTEGER NOT NULL DEFAULT 0,
        categoria TEXT    DEFAULT 'General'
    )
""")

cursor.executemany(
    "INSERT INTO productos (nombre, precio, stock, categoria) VALUES (?, ?, ?, ?)",
    [
        ("Silla",     1418.03, 100, "Mobiliario"),
        ("Mesa",      1575.00,  30, "Mobiliario"),
        ("Archivero", 3605.00,   8, "Mobiliario"),
        ("Sillón",    5356.00,   3, "Premium"),
    ]
)
conn.commit()
conn.close()
print("✅ BD lista con categorías.")

# ======================
# Función reutilizable
# ======================
def consultar(sql, params=()):
    conn   = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute(sql, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# ======================
# Estadísticas generales
# ======================
stats = consultar("""
    SELECT COUNT(*), SUM(precio*stock), AVG(precio),
           MAX(precio), MIN(precio)
    FROM productos
""")[0]

print("\n========================================")
print("     ESTADÍSTICAS GENERALES")
print("========================================")
print(f"Total productos  : {stats[0]}")
print(f"Valor inventario : ${stats[1]:,.2f}")
print(f"Precio promedio  : ${stats[2]:,.2f}")
print(f"Precio máximo    : ${stats[3]:,.2f}")
print(f"Precio mínimo    : ${stats[4]:,.2f}")

# ======================
# Reporte por categoría
# ======================
print("\n========================================")
print("     REPORTE POR CATEGORÍA")
print("========================================")
print(f"{'Categoría':<12} {'Productos':>9} {'Valor':>14} {'Promedio':>12}")
print("-" * 50)

categorias = consultar("""
    SELECT   categoria,
             COUNT(*)            as productos,
             SUM(precio * stock) as valor,
             AVG(precio)         as promedio
    FROM     productos
    GROUP BY categoria
    ORDER BY valor DESC
""")

for cat, total, valor, promedio in categorias:
    print(f"{cat:<12} {total:>9} ${valor:>12,.2f} ${promedio:>10,.2f}")

print("========================================")
