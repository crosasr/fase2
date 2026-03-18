# dia19.py — Menú CLI del sistema de inventario
# En Fase 3 este archivo se reemplaza por Flet; database.py no cambia.

import database as db


def mostrar_tabla(productos):
    if not productos:
        print("  (sin resultados)")
        return
    print(f"\n  {'ID':<4} {'Nombre':<20} {'Categoría':<15} {'Precio':>10} {'Stock':>6}")
    print("  " + "─" * 60)
    for p in productos:
        alerta = " 🔴" if p["stock"] <= 10 else ""
        print(f"  {p['id']:<4} {p['nombre']:<20} {p['categoria']:<15}"
              f" ${p['precio']:>9,.2f} {p['stock']:>6}{alerta}")


def pedir_float(msg: str) -> float:
    while True:
        try:
            return float(input(msg).replace(",", "."))
        except ValueError:
            print("  ❌ Número inválido.")


def pedir_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("  ❌ Entero inválido.")


# ── Acciones de menú ──────────────────────────────────────────

def accion_listar():
    print("\n── CATÁLOGO ──")
    mostrar_tabla(db.obtener_todos())


def accion_agregar():
    print("\n── AGREGAR PRODUCTO ──")
    nombre = input("  Nombre: ").strip()
    if not nombre:
        print("  ❌ El nombre no puede estar vacío.")
        return
    categoria = input("  Categoría [General]: ").strip() or "General"
    precio    = pedir_float("  Precio: $")
    stock     = pedir_int("  Stock inicial: ")
    nuevo_id  = db.agregar_producto(nombre, categoria, precio, stock)
    print(f"  ✅ Producto agregado — ID: {nuevo_id}")


def accion_buscar():
    print("\n── BUSCAR ──")
    termino = input("  Buscar: ").strip()
    if not termino:
        return
    resultados = db.buscar_por_nombre(termino)
    print(f"  {len(resultados)} resultado(s):")
    mostrar_tabla(resultados)


def accion_editar():
    print("\n── EDITAR PRODUCTO ──")
    pid = pedir_int("  ID a editar: ")
    p   = db.obtener_por_id(pid)
    if not p:
        print(f"  ❌ No existe ID {pid}")
        return

    print("  (Enter para mantener valor actual)")
    nombre    = input(f"  Nombre [{p['nombre']}]: ").strip()    or p["nombre"]
    categoria = input(f"  Categoría [{p['categoria']}]: ").strip() or p["categoria"]
    precio_s  = input(f"  Precio [${p['precio']:,.2f}]: ").strip()
    precio    = float(precio_s.replace(",", ".")) if precio_s else p["precio"]
    stock_s   = input(f"  Stock [{p['stock']}]: ").strip()
    stock     = int(stock_s) if stock_s else p["stock"]

    if db.actualizar_producto(pid, nombre, categoria, precio, stock):
        print("  ✅ Actualizado.")
    else:
        print("  ❌ Sin cambios.")


def accion_eliminar():
    print("\n── ELIMINAR PRODUCTO ──")
    pid = pedir_int("  ID a eliminar: ")
    p   = db.obtener_por_id(pid)
    if not p:
        print(f"  ❌ No existe ID {pid}")
        return
    if input(f"  ¿Eliminar '{p['nombre']}'? (s/n): ").lower() == "s":
        db.eliminar_producto(pid)
        print("  ✅ Eliminado.")
    else:
        print("  ↩️  Cancelado.")


def accion_reporte():
    print("\n── REPORTE DE INVENTARIO ──")
    r = db.resumen_inventario()
    print(f"  Productos    : {r['total_productos']}")
    print(f"  Unidades     : {r['total_unidades']:,}")
    print(f"  Valor total  : ${r['valor_total']:>12,.2f}")
    print(f"  Precio prom. : ${r['precio_promedio']:>12,.2f}")

    criticos = db.stock_critico()
    if criticos:
        print(f"\n  ⚠️  Stock crítico (≤ 10 uds):")
        for p in criticos:
            print(f"     🔴 {p['nombre']:<20} {p['stock']} unidades")
    else:
        print("\n  ✅ Sin stock crítico.")


# ── Menú principal ────────────────────────────────────────────

MENU = [
    ("1", "Listar productos",   accion_listar),
    ("2", "Agregar producto",   accion_agregar),
    ("3", "Buscar producto",    accion_buscar),
    ("4", "Editar producto",    accion_editar),
    ("5", "Eliminar producto",  accion_eliminar),
    ("6", "Reporte inventario", accion_reporte),
    ("0", "Salir",              None),
]


def main():
    db.init_db()
    print("╔════════════════════════════════════╗")
    print("║   SISTEMA DE INVENTARIO — PyME     ║")
    print("║   Día 19 | Mini-proyecto SQLite    ║")
    print("╚════════════════════════════════════╝")

    while True:
        print("\n── MENÚ ───────────────────────────")
        for clave, desc, _ in MENU:
            print(f"  {clave}. {desc}")

        opcion = input("\n  Opción: ").strip()
        match = {c: fn for c, _, fn in MENU}

        if opcion not in match:
            print("  ❌ Opción inválida.")
            continue
        if opcion == "0":
            print("\n  Hasta luego. 👋")
            break

        try:
            match[opcion]()
        except Exception as e:
            print(f"  ❌ Error: {e}")


if __name__ == "__main__":
    main()
'''

## 🧠 Conceptos nuevos en Día 19

| Concepto | Línea clave | Por qué importa |
|---|---|---|
| `row_factory = sqlite3.Row` | `get_connection()` | Acceso `p["nombre"]` en lugar de `p[1]` — Flet lo necesita |
| `with conn as conn:` | toda la capa DB | Context manager — commit/rollback automático |
| `cursor.lastrowid` | `agregar_producto()` | Saber el ID del INSERT para la UI |
| `cursor.rowcount > 0` | `actualizar/eliminar` | Verificar si el cambio ocurrió realmente |
| `dict(row)` | `resumen_inventario()` | Convertir Row a dict — serializable, fácil de pasar a Flet |
| Separación capas | 2 archivos | `database.py` no cambia en Fase 3; solo el "frontend" cambia |



## 🚀 Preview Fase 3 — Qué viene mañana


FASE 2 (hoy)          FASE 3 (mañana)
─────────────         ──────────────────────
database.py    →      database.py  (sin cambios ✅)
dia19.py       →      main.py (Flet) — reemplaza el CLI
input()        →      ft.TextField
print()        →      ft.Text / ft.DataTable
while True:    →      ft.app(target=main)
'''