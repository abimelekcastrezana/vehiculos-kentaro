import sqlite3
from pathlib import Path

from flask import g
from werkzeug.security import generate_password_hash

import queries

CARPETA = Path(__file__).parent


def get_db():
    """Una conexión por petición."""
    if "db" not in g:
        g.db = sqlite3.connect(CARPETA / "vehiculos.db")
        g.db.row_factory = sqlite3.Row  # filas accesibles por nombre
        g.db.execute("PRAGMA foreign_keys = ON")  # SQLite no las activa solo
    return g.db


def cerrar_db(error=None):
    conexion = g.pop("db", None)
    if conexion is not None:
        conexion.close()


def crear_tablas():
    conexion = get_db()
    conexion.executescript((CARPETA / "schema.sql").read_text())
    # Usuario de prueba: demo / demo123
    conexion.execute(queries.USUARIO_CREAR, ("demo", generate_password_hash("demo123")))
    conexion.commit()


def init_app(app):
    app.teardown_appcontext(cerrar_db)
    with app.app_context():
        crear_tablas()
