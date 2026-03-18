'''
import sqlite3

# Conectar — crea el archivo .db si no existe
conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# Crear tabla productos
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre   TEXT    NOT NULL,
        precio   REAL    NOT NULL,
        stock    INTEGER NOT NULL DEFAULT 0
    )
""")

conn.commit()
print("✅ Base de datos y tabla creadas.")
conn.close()

import sqlite3

conn   = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# INSERT — agregar productos
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
               ("Silla", 1350.50, 25))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
               ("Mesa", 2800.00, 10))
cursor.execute("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
               ("Lámpara", 450.00, 50))
conn.commit()
print("✅ Productos insertados.")

# SELECT — leer todos los productos
cursor.execute("SELECT * FROM productos")
productos = cursor.fetchall()

print("\n--- Productos en BD ---")
for p in productos:
    print(f"ID:{p[0]}  {p[1]:<12} ${p[2]:>10,.2f}   stock: {p[3]}")

conn.close()
'''
import sqlite3

'''
# ❌ vulnerable a SQL injection
cursor.execute(f"INSERT INTO productos VALUES ('{nombre}')")

# ✅ siempre con placeholders
cursor.execute("INSERT INTO productos VALUES (?)", (nombre,))
```

---

### Bloque 3 — 30 min | Proyecto del día

Crea una función `poblar_bd()` que inserte 5 productos y luego muestre este reporte:
```
========================================
     PRODUCTOS EN BASE DE DATOS
========================================
ID  Nombre         Precio        Stock
----------------------------------------
 1  Silla        $1,350.50        25
 2  Mesa         $2,800.00        10
 3  Lámpara        $450.00        50
 4  Archivero    $3,500.00         8
 5  Sillón       $5,200.00         3
----------------------------------------
Total registros: 5
========================================
'''
import sqlite3

conn   = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# ======================
# Crear tabla
# ======================
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre   TEXT    NOT NULL,
        precio   REAL    NOT NULL,
        stock    INTEGER NOT NULL DEFAULT 0
    )
""")
conn.commit()
print("✅ Base de datos y tabla listas.")

# ======================
# Insertar productos
# ======================
productos_a_insertar = [
    ("Silla",      1350.50, 25),
    ("Mesa",       2800.00, 10),
    ("Lámpara",     450.00, 50),
    ("Archivero",  3500.00,  8),
    ("Sillón",     5200.00,  3),
]

cursor.executemany(
    "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
    productos_a_insertar
)
conn.commit()
print("✅ 5 productos insertados.")

# ======================
# Reporte
# ======================
cursor.execute("SELECT * FROM productos")
productos = cursor.fetchall()

print("\n========================================")
print("     PRODUCTOS EN BASE DE DATOS")
print("========================================")
print(f"{'ID':<4} {'Nombre':<14} {'Precio':>12} {'Stock':>8}")
print("-" * 42)
for p in productos:
    print(f"{p[0]:<4} {p[1]:<14} ${p[2]:>10,.2f} {p[3]:>8}")
print("-" * 42)

cursor.execute("SELECT COUNT(*) FROM productos")
total = cursor.fetchone()[0]
valor = sum(p[2] * p[3] for p in productos)

print(f"Total registros      : {total}")
print(f"Valor del inventario : ${valor:,.2f}")
print("========================================")

conn.close()