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
DELETE FROM productos           -- ❌ borra TODA la tabla
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
SELECT  columnas        -- qué quiero ver
FROM    tabla           -- de dónde
WHERE   condición       -- filtro de filas
ORDER BY columna ASC/DESC  -- cómo ordenar
LIMIT   n               -- cuántos resultados
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
ORDER BY precio ASC    -- menor a mayor (default)
ORDER BY precio DESC   -- mayor a menor
ORDER BY precio * stock DESC  -- ordenar por valor calculado
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

*Actualizar con días 18-20 al completarlos.*
