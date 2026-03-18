import sqlite3

def consultar(sql, params=()):
    conn   = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute(sql, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

'''# Productos más caros primero
print("--- Por precio DESC ---")
for p in consultar("SELECT nombre, precio, stock FROM productos ORDER BY precio DESC"):
    print(f"  {p[0]:<12} ${p[1]:>10,.2f}   stock: {p[2]}")

# Stock crítico
print("\n--- Stock crítico (< 10) ---")
for p in consultar("SELECT nombre, stock FROM productos WHERE stock < 10 ORDER BY stock ASC"):
    print(f"  ⚠️  {p[0]:<12} solo {p[1]} unidades")

# Buscar por nombre
buscar = "si"
print(f"\n--- Búsqueda: '{buscar}' ---")
for p in consultar("SELECT nombre, precio FROM productos WHERE nombre LIKE ?", (f"%{buscar}%",)):
    print(f"  {p[0]:<12} ${p[1]:,.2f}")'''


'''

### Bloque 3 — 30 min | Proyecto del día

Crea una función `reporte_inteligente()` que responda estas 4 preguntas de negocio:
```
========================================
     REPORTE INTELIGENTE
========================================
📦 Producto más caro    : Sillón — $5,356.00
💰 Producto más barato  : Silla  — $1,418.03
⚠️  Productos sin stock  : 0
🔴 Stock crítico (< 10) : 2 productos
----------------------------------------
TOP 3 por valor en inventario:
  1. Sillón     $5,356.00 × 3  = $16,068.00
  2. Archivero  $3,605.00 × 8  = $28,840.00
  3. Mesa       $1,575.00 × 30 = $47,250.00
========================================
'''
def reporte_inteligente():
    print("========================================")
    print("     REPORTE INTELIGENTE")
    print("========================================")
    
    # Producto más caro
    producto_mas_caro = consultar("SELECT nombre, precio FROM productos ORDER BY precio DESC LIMIT 1")[0]
    print(f"📦 Producto más caro    : {producto_mas_caro[0]} — ${producto_mas_caro[1]:,.2f}")
    
    # Producto más barato
    producto_mas_barato = consultar("SELECT nombre, precio FROM productos ORDER BY precio ASC LIMIT 1")[0]
    print(f"💰 Producto más barato  : {producto_mas_barato[0]} — ${producto_mas_barato[1]:,.2f}")
    
    # Productos sin stock
    productos_sin_stock = consultar("SELECT COUNT(*) FROM productos WHERE stock = 0")[0][0]
    print(f"⚠️  Productos sin stock  : {productos_sin_stock}")
    
    # Stock crítico
    stock_critico = consultar("SELECT COUNT(*) FROM productos WHERE stock < 10")[0][0]
    print(f"🔴 Stock crítico (< 10) : {stock_critico} productos")
    
    # TOP 3 por valor en inventario
    print("----------------------------------------")
    print("TOP 3 por valor en inventario:")
    top_3 = consultar("""
        SELECT nombre, precio, stock 
        FROM productos 
        ORDER BY (precio * stock) DESC 
        LIMIT 3
    """)
    for i, (nombre, precio, stock) in enumerate(top_3, 1):
        valor = precio * stock
        print(f"  {i}. {nombre:<12} ${precio:>10,.2f} × {stock}  = ${valor:>10,.2f}")
    
    print("========================================")

# Ejecutar el reporte
reporte_inteligente()