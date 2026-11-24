from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

import queries
from db import get_db

bp = Blueprint("auth", __name__)


def login_required(vista):
    """Protege una ruta: si no hay sesión, manda a /login."""

    @wraps(vista)
    def envuelta(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Inicia sesión para continuar.", "error")
            return redirect(url_for("auth.login"))
        return vista(*args, **kwargs)

    return envuelta


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        password = request.form.get("password", "")
        usuario = get_db().execute(queries.USUARIO_POR_NOMBRE, (nombre,)).fetchone()
        if usuario and check_password_hash(usuario["password"], password):
            session.clear()
            session["usuario_id"] = usuario["id"]
            flash("Sesión iniciada.", "exito")
            return redirect(url_for("vehiculos.listado"))
        flash("Usuario o contraseña incorrectos.", "error")
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("vehiculos.listado"))
