# NOTAS DE APRENDIZAJE — FASE 1
### Python + Flet + SQLite para PyMEs
> Escrito en lenguaje propio. Para teoría formal consultar documentación oficial.

---

## DÍA 1 — Variables, Tipos de Datos y f-strings

### Variables
Contenedores que guardan un valor. Python detecta el tipo automáticamente.
```python
nombre  = "Silla"      # str   → texto, siempre entre comillas
stock   = 25           # int   → número entero, sin punto
precio  = 1350.50      # float → número decimal, con punto
activo  = True         # bool  → solo True o False, con mayúscula
```

### Tipos de datos clave
| Tipo | Ejemplo | Uso en PyME |
|------|---------|-------------|
| str | "Silla" | Nombres, descripciones, categorías |
| int | 25 | Stock, cantidades, unidades |
| float | 1350.50 | Precios, totales, porcentajes |
| bool | True | Disponible, activo, pagado |

### f-strings
Mezclan texto y variables en una sola línea. La `f` va antes de las comillas y las variables entre `{}`.
```python
print(f"Producto: {nombre}")
print(f"Precio: ${precio:.2f}")      # 2 decimales siempre
print(f"Precio: ${precio:,.2f}")     # separador de miles + 2 decimales
```

**Regla:** nunca mostrar precios con `print(precio)` directo. Siempre `{precio:,.2f}`.

### Modificadores de formato útiles
```python
{precio:,.2f}    # $1,350.50  → dinero
{texto:<12}      # alinea texto a la izquierda en 12 espacios
{numero:>10}     # alinea número a la derecha en 10 espacios
```

### Operador ternario
Condicional en una sola línea. Para valores simples es más limpio que un if/else completo.
```python
estado = "Sí" if disponible else "No"
```

---

## DÍA 2 — Listas

### Qué es una lista
Colección ordenada de elementos. El índice empieza en 0.
```python
productos = ["Silla", "Mesa", "Lámpara"]
productos[0]    # → "Silla"   (primero)
productos[-1]   # → "Lámpara" (último siempre es -1)
len(productos)  # → 3
```

### Métodos clave
```python
productos.append("Archivero")   # agrega al final
productos.remove("Mesa")        # elimina por nombre exacto
productos.sort()                # ordena alfabéticamente (modifica la lista original)
```

**Nota:** `.sort()` modifica la lista original. Nunca confiar en que los datos llegan ordenados — aplicar `.sort()` siempre es programación defensiva.

### Recorrer una lista
```python
for producto in productos:
    print(f"- {producto}")

# Con número de posición
for i, producto in enumerate(productos, start=1):
    print(f"{i}. {producto}")
```

**Nota:** `start=1` para que la numeración sea natural para el usuario. Sin él empieza en 0.

### Tip avanzado
Para continuar la numeración desde otra lista:
```python
enumerate(lista_nueva, start=len(lista_previa) + 1)
```

---

## DÍA 3 — Diccionarios

### Qué es un diccionario
Como una lista pero con índices con nombre (claves) en lugar de números.
```python
# Lista → índice numérico
producto[0]          # ¿qué es esto? no dice nada

# Diccionario → clave descriptiva
producto["nombre"]   # claro e inmediato
```

### Estructura básica
```python
producto = {
    "nombre"   : "Silla de oficina",
    "precio"   : 1350.50,
    "stock"    : 25,
    "disponible": True
}

producto["nombre"]          # leer valor
producto["stock"] = 20      # modificar valor
producto["proveedor"] = "X" # agregar clave nueva
```

### Lista de diccionarios = tabla de base de datos
```python
productos = [
    {"nombre": "Silla",   "precio": 1350.50, "stock": 25},
    {"nombre": "Mesa",    "precio": 2800.00, "stock": 10},
]
```
Cada diccionario = una fila. Cada clave = una columna. La lista = la tabla completa.
Cuando llegue SQLite los datos vendrán exactamente así.

### Generator expression
Calcular un valor recorriendo una lista en una sola línea:
```python
# Valor total del inventario
sum(p["precio"] * p["stock"] for p in productos)
```

---

## DÍA 4 — if / elif / else + Operadores

### Estructura básica
```python
if condicion_1:
    # se ejecuta si condicion_1 es True
elif condicion_2:
    # se ejecuta si condicion_1 es False y condicion_2 es True
else:
    # se ejecuta si ninguna condición anterior fue True
```

**Regla crítica:** el orden importa. Python evalúa de arriba hacia abajo y se detiene en el primero que se cumpla.
```python
# ✅ Correcto — el caso más específico primero
if stock == 0:
    estado = "Sin stock"
elif stock <= 10:
    estado = "Stock bajo"
else:
    estado = "OK"

# ❌ Incorrecto — stock == 0 nunca se alcanza porque <= 10 lo atrapa antes
elif stock <= 10:
    ...
if stock == 0:
    ...
```

### Operadores de comparación
```python
==   # igual
!=   # diferente
>    # mayor que
<    # menor que
>=   # mayor o igual
<=   # menor o igual
```

### Operadores lógicos
```python
and  # ambas condiciones True
or   # al menos una True
not  # invierte el resultado
```

### Rango en una sola línea
Python permite esto — muy útil para rangos de precio o stock:
```python
if 1000 <= precio <= 3000:   # equivale a precio >= 1000 and precio <= 3000
```

### Operador ternario encadenado
Para clasificaciones de 3+ valores sin escribir if/elif/else completo:
```python
categoria = "Premium" if precio >= 3000 else "Estándar" if precio >= 1000 else "Económico"
```
Usar solo cuando la lógica es simple. Si es compleja, mejor if/elif/else por legibilidad.

---

## DÍA 5 — for, while, break y continue

### for — recorrer colecciones
```python
for p in productos:
    if p["stock"] > 0:         # filtro dentro del for
        print(p["nombre"])
```

### while — repetir mientras se cumpla una condición
```python
contador = 1
while contador <= 5:
    print(contador)
    contador += 1    # ⚠️ sin esto → bucle infinito (Ctrl+C para salir)
```

**Regla:** siempre debe existir algo dentro del while que eventualmente haga falsa la condición.

### while True — menú interactivo
El patrón más usado en apps de consola:
```python
while True:
    opcion = input("Elige opción: ")
    if opcion == "5":
        break    # el break es el que controla la salida
```

### break — salir del bucle completamente
```python
for p in productos:
    if p["nombre"] == buscar:
        print("Encontrado")
        break    # ya no necesito seguir buscando
```

### continue — saltar esta vuelta y seguir con la siguiente
```python
for p in productos:
    if p["stock"] == 0:
        continue       # salta el print de abajo para este producto
    print(p["nombre"]) # solo se ejecuta si stock > 0
```

### Diferencia clave
```
break    → sale del bucle completamente
continue → salta solo esta vuelta, el bucle sigue
```

---

## DÍAS 6-7 — Mini-proyecto: Menú interactivo

### Patrón de menú de consola
Estructura base reutilizable para cualquier app de consola:
```python
productos = []

def mostrar_menu():
    print("1. Agregar")
    print("2. Eliminar")
    print("3. Listar")
    print("4. Buscar")
    print("5. Salir")

while True:
    mostrar_menu()
    opcion = input("Elige: ")
    if opcion == "1":
        ...
    elif opcion == "5":
        break
    else:
        print("⚠️ Opción no válida")
```

### .lower() — búsqueda insensible a mayúsculas
```python
if p["nombre"].lower() == nombre.lower():
    # "Silla" == "silla" == "SILLA" → True
```
Sin `.lower()` la comparación es exacta y falla si el usuario escribe diferente.

### Búsqueda parcial con in
```python
resultados = [p for p in productos if buscar.lower() in p["nombre"].lower()]
# buscar = "si" → encuentra "Silla", "Sillón", "Sillas"
```

### Verificar lista vacía
```python
if not productos:           # más pythónico que len(productos) == 0
    print("Lista vacía")
```

### Variable bandera (flag)
Para saber si se encontró algo dentro de un bucle:
```python
encontrado = False
for p in productos:
    if condicion:
        encontrado = True
        break
if not encontrado:
    print("No encontrado")
```

---

## CONCEPTOS TRANSVERSALES

### Programación defensiva
Asumir que los datos pueden llegar sucios, desordenados o incorrectos y protegerse antes de procesarlos.
- Aplicar `.sort()` aunque la lista parezca ordenada
- Usar `.lower()` en comparaciones de texto
- Validar que la lista no esté vacía antes de recorrerla

### List comprehension
Filtrar o transformar una lista en una sola línea:
```python
# Solo productos con stock
disponibles = [p for p in productos if p["stock"] > 0]

# Solo nombres de productos económicos
economicos = [p["nombre"] for p in productos if p["precio"] < 1000]
```

### Herramientas del entorno
| Herramienta | Uso |
|-------------|-----|
| `uv run python archivo.py` | Ejecutar script en el entorno virtual |
| `uv add nombre_paquete` | Instalar dependencia |
| `git commit -m "mensaje"` | Guardar versión con descripción clara |
| Windsurf | Copiloto — explicar errores, no escribir el código |

---

## DÍA 8 — Funciones: parámetros y return

### Estructura básica
```python
def nombre_funcion(parametro1, parametro2):
    return resultado
```

- `def` → declara la función
- parámetros → identificadores (los nombres)
- argumentos → valores reales que se pasan al llamarla
- `return` → el valor que entrega de vuelta, puede operarse

### Regla clave
Separar lógica en funciones evita repetir código y hace que
funcione con 5 o 500 productos sin cambiar nada.
```python
def aplicar_descuento(precio, descuento):
    return precio - (precio * descuento / 100)

def clasificar_producto(precio):
    if precio >= 3000:
        return "Premium"
    elif precio >= 1000:
        return "Estándar"
    else:
        return "Económico"

def estado_stock(stock):
    if stock == 0:
        return "❌ Sin stock"
    elif stock <= 10:
        return "⚠️  Stock bajo"
    else:
        return "✅ OK"
```

---

## DÍA 9 — Funciones con valores por defecto

### Parámetros opcionales
```python
def calcular_precio(precio, descuento=0):
    return precio - (precio * descuento / 100)

calcular_precio(1350.50)        # → 1350.50 (usa default)
calcular_precio(1350.50, 10)    # → 1215.45 (sobreescribe default)
```

### Regla crítica
Parámetros opcionales siempre al final — si van primero Python
no sabe a qué parámetro asignar cada argumento → SyntaxError.
```python
def funcion(obligatorio, opcional=valor):   # ✅
def funcion(opcional=valor, obligatorio):   # ❌ SyntaxError
```

### Función que se adapta sola
```python
def resumen_venta(cliente, items, vendedor="Sin asignar", descuento=0):
    subtotal        = sum(p["precio"] * p["cantidad"] for p in items)
    monto_descuento = subtotal * descuento / 100
    total           = subtotal - monto_descuento
```

Una función puede recibir una lista como parámetro y recorrerla
internamente con for — no necesita saber cuántos elementos tiene.

---

## DÍA 10 — Scope y try/except

### Scope — dónde viven las variables

```python
impuesto = 0.16          # variable GLOBAL — vive en todo el programa

def calcular_precio(precio):
    resultado = precio * impuesto   # usa la global ✅
    return resultado                # resultado solo existe aquí adentro

print(impuesto)     # ✅ accesible — es global
print(resultado)    # ❌ NameError — resultado es local, ya no existe
```

**Regla:**
```
Variable global  → declarada fuera de funciones → accesible desde cualquier lado
Variable local   → declarada dentro de una función → desaparece al terminar
```

La única forma de sacar un valor de una función es con `return`.

---

### try/except — programa que nunca se rompe

Sin manejo de errores un input inválido mata el programa:
```python
stock = int(input("Stock: "))   # usuario escribe "abc" → crash 💀
```

Con try/except el programa atrapa el error y sigue vivo:
```python
try:
    valor = int(input("Stock: "))   # intenta esto
except ValueError:
    print("⚠️  Ingresa solo números enteros.")   # si falla, ejecuta esto
```

### Patrón completo para validar inputs

Combina `while True` + `try/except` + validación de negativos:

```python
def pedir_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("⚠️  El valor no puede ser negativo.")
                continue        # pide de nuevo
            return valor        # solo sale si el valor es válido
        except ValueError:
            print("⚠️  Ingresa solo números enteros.")

def pedir_flotante(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("⚠️  El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("⚠️  Ingresa solo números.")
```

Estas dos funciones se reutilizan en cualquier app — son las primeras candidatas a vivir en un módulo `validaciones.py`.

### Errores comunes que atrapa ValueError
```
int("abc")      → ValueError
int("12.5")     → ValueError  (int no acepta decimales)
float("xyz")    → ValueError
```

### Programación defensiva aplicada
Nunca confiar en que el usuario ingresará datos correctos.
Siempre validar: tipo de dato, rango permitido, campos vacíos.
El usuario nunca debe ver un traceback en pantalla.

*Actualizar con cada fase completada.*
