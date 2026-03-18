import sqlite3
'''
conn   = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# Ver estado actual
cursor.execute("SELECT * FROM productos")
print("--- ANTES ---")
for p in cursor.fetchall():
    print(f"ID:{p[0]}  {p[1]:<12} precio:${p[2]:,.2f}  stock:{p[3]}")

# UPDATE — modificar un registro
cursor.execute("""
    UPDATE productos
    SET stock = 100
    WHERE id = 1
""")
conn.commit()
print("\n✅ Stock de ID:1 actualizado a 100.")

# UPDATE — modificar múltiples campos
cursor.execute("""
    UPDATE productos
    SET precio = 1500.00,
        stock  = 30
    WHERE nombre = 'Mesa'
""")
conn.commit()
print("✅ Precio y stock de Mesa actualizados.")

# Ver estado después
cursor.execute("SELECT * FROM productos")
print("\n--- DESPUÉS ---")
for p in cursor.fetchall():
    print(f"ID:{p[0]}  {p[1]:<12} precio:${p[2]:,.2f}  stock:{p[3]}")

# Agregar al mismo archivo

# DELETE — eliminar por ID
cursor.execute("DELETE FROM productos WHERE id = 3")
conn.commit()
print("\n✅ Producto ID:3 eliminado.")

# DELETE — eliminar por condición
cursor.execute("DELETE FROM productos WHERE stock = 0")
conn.commit()
print("✅ Productos sin stock eliminados.")

# Ver cuántos quedan
cursor.execute("SELECT COUNT(*) FROM productos")
total = cursor.fetchone()[0]
print(f"✅ Quedan {total} productos en BD.")
conn.close()
'''

'''
### Bloque 3 — 30 min | Proyecto del día

Crea una función `actualizar_precios()` que aplique aumentos por categoría:
```
Económico  (precio < 1000)  → +10%
Estándar   (precio < 3000)  → +5%
Premium    (precio >= 3000) → +3%
```

Y muestre este reporte:
```
========================================
   ACTUALIZACIÓN DE PRECIOS
========================================
Producto       Precio ant.   Precio nuevo   Cambio
----------------------------------------------------
Silla          $1,350.50     $1,418.03      +5%
Mesa           $1,500.00     $1,575.00      +5%
Archivero      $3,500.00     $3,605.00      +3%
Sillón         $5,200.00     $5,356.00      +3%
----------------------------------------------------
Valor inventario anterior : $XXX,XXX.XX
Valor inventario nuevo    : $XXX,XXX.XX
========================================
'''
def actualizar_precios():
    conn   = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    
    # Calcular precios nuevos
    cursor.execute("SELECT id, nombre, precio FROM productos")
    productos = cursor.fetchall()
    
    print("========================================")
    print("   ACTUALIZACIÓN DE PRECIOS")
    print("========================================")
    print("Producto       Precio ant.   Precio nuevo   Cambio")
    print("----------------------------------------------------")
    
    total_anterior = 0
    total_nuevo = 0
    
    for id_prod, nombre, precio in productos:
        if precio < 1000:
            nuevo_precio = precio * 1.10
            cambio = "+10%"
        elif precio < 3000:
            nuevo_precio = precio * 1.05
            cambio = "+5%"
        else:
            nuevo_precio = precio * 1.03
            cambio = "+3%"
        
        # Actualizar en BD
        cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, id_prod))
        
        # Mostrar fila
        print(f"{nombre:<12} ${precio:,.2f}     ${nuevo_precio:,.2f}      {cambio}")
        
        total_anterior += precio
        total_nuevo += nuevo_precio
    
    conn.commit()
    
    print("----------------------------------------------------")
    print(f"Valor inventario anterior : ${total_anterior:,.2f}")
    print(f"Valor inventario nuevo    : ${total_nuevo:,.2f}")
    print("========================================")
    
    conn.close()

# Ejecutar
actualizar_precios()