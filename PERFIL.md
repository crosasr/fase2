# PERFIL DE DESARROLLO — CONTEXTO PARA WINDSURF

## Quién soy
Desarrollador de aplicaciones para PyMEs mexicanas.
Actualmente en aprendizaje activo de Python + Flet + SQLite.
Experiencia previa en otro lenguaje de programación.
Enfoque: traducir datos en decisiones de negocio prácticas.

---

## Stack tecnológico
- **Lenguaje:** Python 3.12+
- **Gestor de entornos:** UV (uv init, uv add, uv run)
- **Interfaz gráfica:** Flet (apps de escritorio y web)
- **Base de datos:** SQLite con módulo sqlite3
- **IDE:** Windsurf
- **Control de versiones:** Git + GitHub

---

## Perfil de mis apps
- Dirigidas a dueños de PyMEs mexicanas sin conocimientos técnicos
- Casos de uso: inventario, ventas, clientes, facturación simple
- Lenguaje de la interfaz: español, términos de negocio (no técnicos)
- UI simple, limpia, colores neutros, fácil de usar
- El usuario final nunca debe ver un error técnico en pantalla

---

## Estilo de código que prefiero
- Código limpio y legible sobre código "inteligente"
- Comentarios en español
- Funciones pequeñas con una sola responsabilidad
- Código organizado en módulos separados (UI, lógica, base de datos)
- Manejo de errores con try/except en toda entrada de usuario
- Variables y funciones con nombres descriptivos en español
  - ✅ `calcular_total_venta()`
  - ❌ `calc()` o `fn1()`

---

## Cómo quiero que Windsurf me ayude
- **Explicar antes de corregir:** si hay un error, explícamelo línea por línea antes de darme la solución
- **No hacer el trabajo completo:** dame pistas o la estructura, no el código terminado
- **Refinar mis prompts:** si mi pregunta es confusa, ayúdame a reformularla mejor
- **Alternativas con contexto:** si me sugieres algo, dime por qué es mejor para mi perfil
- **Íconos y componentes Flet:** verificar siempre en la documentación oficial antes de sugerir (ejemplo: Icons.RESET no existe en Flet)

---

## Ruta de aprendizaje actual
| Fase | Contenido | Estado |
|------|-----------|--------|
| Fase 0 | Setup: Python, UV, Windsurf, Flet | ✅ Completada |
| Fase 1 | Fundamentos Python (15 días) | 🔄 En progreso |
| Fase 2 | SQLite + sqlite3 | ⬜ Pendiente |
| Fase 3 | Flet básico + conexión SQLite | ⬜ Pendiente |
| Fase 4 | App completa para PyME | ⬜ Pendiente |
| Fase 5 | Empaquetado .exe + despliegue web | ⬜ Pendiente |

---

## Proyecto objetivo al terminar la ruta
App de escritorio funcional para una PyME con:
- Módulo de productos (CRUD completo)
- Módulo de clientes
- Módulo de ventas con control de stock automático
- Reportes básicos exportables a CSV
- Empaquetada como .exe para entregar sin instalar Python

---

## Notas personales
- Aprendo mejor con ejemplos de negocio reales, no ejercicios abstractos
- Prefiero entender el "por qué" antes de aplicar el "cómo"
- Cada proyecto terminado se sube a GitHub con commit descriptivo
- Repositorio actual: github.com/crosasr/fase1

## Meta de aprendizaje
- Cada ejercicio debe resolver un problema de negocio real
- El código debe ser entendible por otro programador junior
- Priorizar funcionalidad sobre elegancia técnica