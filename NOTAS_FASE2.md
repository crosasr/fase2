# NOTAS DE APRENDIZAJE — FASE 2
### SQLite + sqlite3 para PyMEs
> Escrito en lenguaje propio. Para teoría formal consultar documentación oficial.

---

## DÍA 15 — Introducción a SQLite

### Qué es SQLite
Base de datos relacional que vive en un solo archivo `.db`.
No requiere servidor — viene incluida en Python con `import sqlite3`.

```
CSV    → archivo de texto, simple, sin consultas
SQLite → base de datos real, consultas SQL, persistencia profesional
```

### Conexión y cursor
```python
import sqlite3

conn   = sqlite3.connect("inventario.db")  # crea el archivo si no existe
cursor = conn.cursor()                      # ejecuta las consultas
# ... operaciones ...
conn.commit()   # confirma los cambios
conn.close()    # cierra la conexión
```

**Regla:** siempre `commit()` antes de `close()` — sin commit los cambios se pierden.

### CREATE TABLE
```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre   TEXT    NOT NULL,
        precio   REAL    NOT NULL,
        stock    INTEGER NOT NULL DEFAULT 0
    )
""")
```

- `IF NOT EXISTS` → no falla si la tabla ya existe — siempre usarlo
- `PRIMARY KEY AUTOINCREMENT` → ID único generado automáticamente
- `NOT NULL` → campo obligatorio
- `DEFAULT 0` → valor por defecto si no se especifica

### INSERT
```python
# Un registro
cursor.execute(
    "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
    ("Silla", 1350.50, 25)
)

# Múltiples registros — más eficiente
cursor.executemany(
    "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
    [("Silla", 1350.50, 25), ("Mesa", 2800.00, 10)]
)
```

**Regla crítica:** siempre usar `?` como placeholder — nunca concatenar valores en el SQL:
```python
# ❌ vulnerable a SQL injection
f"INSERT INTO productos VALUES ('{nombre}')"

# ✅ seguro
"INSERT INTO productos VALUES (?)", (nombre,)
```

### SELECT
```python
cursor.execute("SELECT * FROM productos")
productos = cursor.fetchall()    # lista de tuplas — todos los registros
producto  = cursor.fetchone()    # solo el primer registro
```

Cada tupla sigue el orden de columnas del SELECT:
```python
# SELECT id, nombre, precio, stock
p = (1, "Silla", 1350.50, 25)
# p[0]=id  p[1]=nombre  p[2]=precio  p[3]=stock
```

### DB Browser for SQLite
Herramienta visual gratuita para ver y editar bases de datos SQLite.
Úsala para verificar que el código guarda bien los datos.
Permite ejecutar SQL de prueba antes de escribirlo en Python.

---

## DÍA 16 — UPDATE y DELETE

### UPDATE — modificar registros
```python
# Modificar un campo
cursor.execute("""
    UPDATE productos
    SET stock = 100
    WHERE id = 1
""")

# Modificar múltiples campos
cursor.execute("""
    UPDATE productos
    SET precio = 1500.00,
        stock  = 30
    WHERE nombre = 'Mesa'
""")
conn.commit()
```

En español:
```
"Actualiza productos,
 establece stock = 100
 donde id = 1"
```

**Regla:** preferir `WHERE id = ?` sobre `WHERE nombre = ?` — el ID es único, el nombre puede repetirse.

### DELETE — eliminar registros
```python
# Eliminar por ID
cursor.execute("DELETE FROM productos WHERE id = ?", (3,))

# Eliminar por condición
cursor.execute("DELETE FROM productos WHERE stock = 0")

conn.commit()
```

**Regla crítica:** SIEMPRE usar WHERE en DELETE:
```sql
DELETE FROM productos               -- ❌ borra TODA la tabla
DELETE FROM productos WHERE id = 3  -- ✅ borra solo ese registro
```

### IDs no se renumeran
Al eliminar un registro el ID no se reasigna:
```
Antes: 1, 2, 3, 4, 5
Borrar ID:3
Después: 1, 2, 4, 5   ← el 3 desaparece para siempre
```
El ID es una llave única permanente, no un número de posición.

### Lógica de negocio en UPDATE
```python
# Actualizar precios por categoría desde Python
for id_prod, nombre, precio in productos:
    if precio < 1000:
        nuevo_precio = precio * 1.10    # +10%
    elif precio < 3000:
        nuevo_precio = precio * 1.05    # +5%
    else:
        nuevo_precio = precio * 1.03    # +3%

    cursor.execute(
        "UPDATE productos SET precio = ? WHERE id = ?",
        (nuevo_precio, id_prod)
    )
conn.commit()
```

---

## DÍA 17 — SELECT avanzado: WHERE, ORDER BY, LIKE

### Estructura completa de SELECT
```sql
SELECT  columnas           -- qué quiero ver
FROM    tabla              -- de dónde
WHERE   condición          -- filtro de filas
ORDER BY columna ASC/DESC  -- cómo ordenar
LIMIT   n                  -- cuántos resultados
```

En español:
```
"Selecciona nombre y precio
 de productos
 donde precio sea mayor a 1000
 ordenado de mayor a menor
 solo los primeros 5"
```

### WHERE con operadores
```sql
WHERE stock < 10
WHERE precio BETWEEN 1000 AND 4000
WHERE stock = 0
WHERE stock > 0 AND precio >= 1000
WHERE stock = 0 OR precio > 5000
```

### LIKE — búsqueda parcial
```sql
WHERE nombre LIKE '%si%'   -- contiene "si"
WHERE nombre LIKE 'si%'    -- empieza con "si"
WHERE nombre LIKE '%si'    -- termina con "si"
```
`%` → cualquier texto (cero o más caracteres)

Equivalente Python: `"si" in nombre.lower()`

### ORDER BY
```sql
ORDER BY precio ASC               -- menor a mayor (default)
ORDER BY precio DESC              -- mayor a menor
ORDER BY precio * stock DESC      -- ordenar por valor calculado
```

### LIMIT
```sql
LIMIT 1    -- solo el primero (MAX o MIN)
LIMIT 3    -- top 3
LIMIT 10   -- primeros 10
```

### Función consultar() — patrón reutilizable
```python
def consultar(sql, params=()):
    conn   = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute(sql, params)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# Sin parámetros
consultar("SELECT * FROM productos ORDER BY precio DESC")

# Con parámetros
consultar("SELECT * FROM productos WHERE stock < ?", (10,))

# Con LIKE dinámico
buscar = "si"
consultar("SELECT * FROM productos WHERE nombre LIKE ?", (f"%{buscar}%",))
```

**Nota:** `(10,)` — la coma es obligatoria para que Python lo lea como tupla y no como número.

### Desempaquetar tuplas en for
```python
# SELECT nombre, precio, stock → 3 elementos por tupla
for nombre, precio, stock in resultado:
    print(f"{nombre} ${precio:,.2f} stock:{stock}")

# Con enumerate
for i, (nombre, precio, stock) in enumerate(resultado, 1):
    print(f"{i}. {nombre}")
```

### Equivalencia pandas ↔ SQL
| pandas | SQL |
|--------|-----|
| `groupby('col')` | `GROUP BY col` |
| `.sum()` | `SUM(col)` |
| `.mean()` | `AVG(col)` |
| `.count()` | `COUNT(*)` |
| `.max()` | `MAX(col)` |
| `.min()` | `MIN(col)` |
| `sort_values()` | `ORDER BY` |
| `.head(5)` | `LIMIT 5` |
| `df[df['col'] > x]` | `WHERE col > x` |
| `pd.merge()` | `JOIN` |

---

## DÍA 18 — GROUP BY y agregaciones

### Para qué sirve GROUP BY
Agrupa filas que comparten un valor y aplica una función sobre cada grupo.
Sin GROUP BY las funciones como SUM o COUNT operan sobre toda la tabla.
Con GROUP BY operan por categoría.

```
Sin GROUP BY → una sola fila con el total global
Con GROUP BY → una fila por cada categoría
```

### Funciones de agregación
```sql
COUNT(*)           -- número de filas en el grupo
SUM(precio*stock)  -- suma de una columna o expresión
AVG(precio)        -- promedio
MAX(precio)        -- valor más alto
MIN(precio)        -- valor más bajo
```

### Sintaxis básica
```sql
SELECT  categoria,
        COUNT(*)              AS total_productos,
        SUM(precio * stock)   AS valor_inventario,
        AVG(precio)           AS precio_promedio,
        MAX(precio)           AS precio_maximo
FROM    productos
GROUP BY categoria
ORDER BY valor_inventario DESC
```

En español:
```
"Para cada categoría distinta,
 cuéntame cuántos productos hay,
 súmame el valor total del stock,
 dime el precio promedio y el máximo,
 ordena de mayor a menor valor"
```

### AS — alias de columna
```sql
COUNT(*) AS total          -- renombra la columna en el resultado
SUM(precio * stock) AS valor_inventario
```
Sin AS el nombre de la columna sería `COUNT(*)` — ilegible en código y en Flet.

### HAVING — filtrar grupos (≠ WHERE)
```sql
-- WHERE filtra filas ANTES de agrupar
-- HAVING filtra grupos DESPUÉS de agrupar

SELECT categoria, COUNT(*) AS total
FROM productos
GROUP BY categoria
HAVING COUNT(*) >= 2        -- solo categorías con 2 o más productos
```

```
WHERE  → filtra filas individuales  → se ejecuta ANTES del GROUP BY
HAVING → filtra grupos              → se ejecuta DESPUÉS del GROUP BY
```

### En Python — leer resultados con alias
```python
# fetchall() devuelve tuplas en el orden del SELECT
for categoria, total, valor, promedio, maximo in resultado:
    print(f"{categoria:<15} {total} productos  ${valor:>12,.2f}")

# Con row_factory los alias se usan como clave de diccionario:
# row["total_productos"], row["valor_inventario"]
```

### Caso de uso real: resumen por categoría
```python
resumen = consultar("""
    SELECT  categoria,
            COUNT(*)            AS total,
            SUM(stock)          AS unidades,
            SUM(precio * stock) AS valor,
            AVG(precio)         AS precio_prom
    FROM    productos
    GROUP BY categoria
    ORDER BY valor DESC
""")
```
Esto es exactamente lo que alimenta un dashboard de inventario por categoría.

---

## DÍA 19 — Mini-proyecto integrador

### Qué cambió respecto a los días anteriores

Hasta el día 17 cada archivo era independiente y usaba conexiones sueltas.
El día 19 introduce una arquitectura de dos capas que se mantiene igual en Fase 3:

```
database.py  ←  toda la lógica SQLite (no cambia en Fase 3)
dia19.py     ←  interfaz CLI (se reemplaza por Flet en Fase 3)
```

La separación es la decisión de diseño más importante de la Fase 2.

### row_factory — acceso por nombre en lugar de índice
```python
# Sin row_factory (días 15-17)
p[0]  # id
p[1]  # nombre
p[2]  # precio   ← frágil: si cambia el orden del SELECT, todo se rompe

# Con row_factory
conn.row_factory = sqlite3.Row
p["id"]
p["nombre"]
p["precio"]   # ← robusto: funciona sin importar el orden del SELECT
```

Se activa en la función de conexión para que aplique a todas las consultas:
```python
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
```

### Context manager — with conn as conn
```python
# Sin context manager (días 15-17) — hay que cerrar manualmente
conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()
cursor.execute(...)
conn.commit()
conn.close()   # si hay error antes de aquí, la conexión queda abierta

# Con context manager — commit y close automáticos
with get_connection() as conn:
    conn.execute(...)
    conn.commit()
# conn.close() se llama automáticamente al salir del bloque
```

### lastrowid — recuperar el ID del INSERT
```python
with get_connection() as conn:
    cursor = conn.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
        (nombre, precio, stock)
    )
    conn.commit()
    return cursor.lastrowid   # ← el ID que AUTOINCREMENT asignó
```
Útil en Flet para mostrar confirmación: "Producto guardado con ID: 7".

### rowcount — verificar si el cambio ocurrió
```python
cursor = conn.execute(
    "UPDATE productos SET precio = ? WHERE id = ?",
    (precio, pid)
)
conn.commit()
return cursor.rowcount > 0   # True si modificó al menos una fila
                              # False si el id no existe
```
Mismo patrón para DELETE. Permite dar feedback real al usuario en lugar de asumir que funcionó.

### dict(row) — convertir Row a diccionario
```python
# Row es conveniente para acceso por nombre pero no es serializable
row = conn.execute("SELECT COUNT(*) AS total ...").fetchone()

# Para pasar datos a Flet o a cualquier función externa:
return dict(row)   # {"total": 5, "valor": 12500.00, ...}
```

### Path para la ruta de la base de datos
```python
from pathlib import Path

DB_PATH = Path(__file__).parent / "tienda.db"
# __file__ → ruta del archivo database.py
# .parent  → carpeta donde vive database.py
# / "tienda.db" → la BD siempre se crea junto al código
```
Sin esto, la BD se crea en el directorio desde donde se ejecuta el script,
que puede variar. Con Path siempre está en el lugar correcto.

### init_db() — patrón de inicialización
```python
def init_db():
    """Crea las tablas si no existen. Llamar al arrancar la app."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS productos (...)
        """)
        conn.commit()
```
Se llama una sola vez al inicio del programa. En Flet irá dentro de `main()`.

### Estructura del database.py
```
get_connection()       → fábrica de conexiones con row_factory
init_db()              → crea tablas al arrancar

agregar_producto()     → INSERT, retorna lastrowid
obtener_todos()        → SELECT *, orden por nombre
obtener_por_id()       → SELECT WHERE id, retorna Row o None
buscar_por_nombre()    → SELECT WHERE LIKE
actualizar_producto()  → UPDATE, retorna rowcount > 0
eliminar_producto()    → DELETE, retorna rowcount > 0

stock_critico()        → SELECT WHERE stock <= umbral
resumen_inventario()   → COUNT, SUM, AVG en una sola query → dict
```

### Transición a Fase 3
```
FASE 2                     FASE 3
─────────────────          ──────────────────────────
database.py          →     database.py  (sin cambios)
dia19.py (CLI)       →     main.py (Flet)
input()              →     ft.TextField
print()              →     ft.Text / ft.DataTable
while True: menú     →     ft.app(target=main)
```
`database.py` no se toca en Fase 3. Solo cambia el frontend.

---

*Fase 2 completada — días 15 al 19.*
