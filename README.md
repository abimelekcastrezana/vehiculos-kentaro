# Vehículos

Proyecto didáctico: publicar, editar y eliminar vehículos. Flask + SQLite + plantillas Jinja.

```
app.py             arranque de la app
db.py              conexión a SQLite y creación de tablas
schema.sql         tablas y datos iniciales (marcas, tipos, lotes)
modules/
  auth.py          login y decorador login_required
  vehiculos.py     listado, detalle, nuevo, editar, eliminar
templates/         HTML (nuevo.html y editar.html comparten _campos.html)
static/style.css
```

## Ejecutar

```bash
uv run python app.py     # http://127.0.0.1:5000
```

Usuario de prueba: `demo` / `demo123`

## Rutas

| Ruta | Qué hace |
|---|---|
| `GET /` | listado |
| `GET /vehiculos/<id>` | detalle |
| `GET/POST /vehiculos/nuevo` | alta (requiere sesión) |
| `GET/POST /vehiculos/<id>/editar` | edición (requiere sesión) |
| `POST /vehiculos/<id>/eliminar` | eliminación (requiere sesión) |
| `GET/POST /registro` | crear cuenta (público) |
| `GET /usuarios` | listado de usuarios (requiere sesión) |
| `GET/POST /usuarios/<id>/editar` | editar nombre y/o contraseña (requiere sesión) |
| `POST /usuarios/<id>/eliminar` | eliminar usuario (requiere sesión) |

## Licencia

MIT. Ver [LICENSE](LICENSE).
