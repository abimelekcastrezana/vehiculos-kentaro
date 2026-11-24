"""Todas las consultas SQL del proyecto, en un solo lugar.

Los módulos las usan así:  get_db().execute(queries.VEHICULOS_LISTAR).fetchall()
Los "?" se reemplazan por los valores que se pasan como segundo argumento.
"""

# ---------- Usuarios ----------

# Busca un usuario por su nombre (para el login).
USUARIO_POR_NOMBRE = "SELECT * FROM usuarios WHERE nombre = ?"

# Crea un usuario (registro y usuario de prueba); si el nombre ya existe no hace nada.
USUARIO_CREAR = "INSERT OR IGNORE INTO usuarios (nombre, password) VALUES (?, ?)"

# Trae todos los usuarios, sin la contraseña, ordenados por nombre.
USUARIOS_LISTAR = "SELECT id, nombre FROM usuarios ORDER BY nombre"

# Trae un usuario por su id.
USUARIO_BUSCAR = "SELECT * FROM usuarios WHERE id = ?"

# Cambia el nombre de un usuario.
USUARIO_ACTUALIZAR_NOMBRE = "UPDATE usuarios SET nombre = ? WHERE id = ?"

# Cambia la contraseña (ya cifrada) de un usuario.
USUARIO_ACTUALIZAR_PASSWORD = "UPDATE usuarios SET password = ? WHERE id = ?"

# Borra un usuario por su id.
USUARIO_ELIMINAR = "DELETE FROM usuarios WHERE id = ?"


# ---------- Catálogos (llenan los selects del formulario) ----------

# Trae todas las marcas.
MARCAS_LISTAR = "SELECT * FROM marcas"

# Trae todos los tipos.
TIPOS_LISTAR = "SELECT * FROM tipos"

# Trae todos los lotes.
LOTES_LISTAR = "SELECT * FROM lotes"

# Comprueban que el id recibido existe (validación de claves foráneas).
MARCA_EXISTE = "SELECT id FROM marcas WHERE id = ?"
TIPO_EXISTE = "SELECT id FROM tipos WHERE id = ?"
LOTE_EXISTE = "SELECT id FROM lotes WHERE id = ?"


# ---------- Vehículos ----------

# Trae todos los vehículos, del más nuevo al más viejo. El JOIN cambia los
# ids de marca, tipo y lote por sus nombres para poder mostrarlos.
VEHICULOS_LISTAR = """
    SELECT v.*, m.nombre AS marca, t.nombre AS tipo, l.nombre AS lote
    FROM vehiculos v
    JOIN marcas m ON m.id = v.marca_id
    JOIN tipos  t ON t.id = v.tipo_id
    JOIN lotes  l ON l.id = v.lote_id
    ORDER BY v.id DESC
"""

# Trae un solo vehículo por su id, también con los nombres de marca, tipo y lote.
VEHICULO_BUSCAR = """
    SELECT v.*, m.nombre AS marca, t.nombre AS tipo, l.nombre AS lote
    FROM vehiculos v
    JOIN marcas m ON m.id = v.marca_id
    JOIN tipos  t ON t.id = v.tipo_id
    JOIN lotes  l ON l.id = v.lote_id
    WHERE v.id = ?
"""

# Inserta un vehículo nuevo con los datos del formulario de alta.
VEHICULO_CREAR = """
    INSERT INTO vehiculos
        (marca_id, tipo_id, lote_id, modelo, anio, precio, descripcion, imagen_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

# Cambia todos los datos de un vehículo existente (el último ? es su id).
VEHICULO_ACTUALIZAR = """
    UPDATE vehiculos
    SET marca_id = ?, tipo_id = ?, lote_id = ?, modelo = ?,
        anio = ?, precio = ?, descripcion = ?, imagen_url = ?
    WHERE id = ?
"""

# Borra un vehículo por su id.
VEHICULO_ELIMINAR = "DELETE FROM vehiculos WHERE id = ?"
