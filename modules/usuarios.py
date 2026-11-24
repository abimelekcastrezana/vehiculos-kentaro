from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

import queries
from db import get_db
from modules.auth import login_required

bp = Blueprint("usuarios", __name__)


def buscar_usuario(usuario_id):
    usuario = get_db().execute(queries.USUARIO_BUSCAR, (usuario_id,)).fetchone()
    if usuario is None:
        abort(404)
    return usuario


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    db = get_db()

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        password = request.form.get("password", "")

        if not nombre:
            flash("El nombre es obligatorio.", "error")
        elif len(password) < 4:
            flash("La contraseña debe tener al menos 4 caracteres.", "error")
        elif db.execute(queries.USUARIO_POR_NOMBRE, (nombre,)).fetchone():
            flash("Ese nombre ya está en uso.", "error")
        else:
            db.execute(queries.USUARIO_CREAR, (nombre, generate_password_hash(password)))
            db.commit()
            flash("Cuenta creada. Ya puedes iniciar sesión.", "exito")
            return redirect(url_for("auth.login"))

    return render_template("registro.html")


@bp.route("/usuarios")
@login_required
def listado():
    usuarios = get_db().execute(queries.USUARIOS_LISTAR).fetchall()
    return render_template("usuarios.html", usuarios=usuarios)


@bp.route("/usuarios/<int:usuario_id>/editar", methods=["GET", "POST"])
@login_required
def editar(usuario_id):
    db = get_db()
    usuario = buscar_usuario(usuario_id)

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        password = request.form.get("password", "")  # vacía = no cambiarla
        otro = db.execute(queries.USUARIO_POR_NOMBRE, (nombre,)).fetchone()

        if not nombre:
            flash("El nombre es obligatorio.", "error")
        elif otro and otro["id"] != usuario_id:
            flash("Ese nombre ya está en uso.", "error")
        elif password and len(password) < 4:
            flash("La contraseña debe tener al menos 4 caracteres.", "error")
        else:
            db.execute(queries.USUARIO_ACTUALIZAR_NOMBRE, (nombre, usuario_id))
            if password:
                db.execute(queries.USUARIO_ACTUALIZAR_PASSWORD, (generate_password_hash(password), usuario_id))
            db.commit()
            flash("Usuario actualizado.", "exito")
            return redirect(url_for("usuarios.listado"))

    return render_template("usuario_editar.html", usuario=usuario)


@bp.route("/usuarios/<int:usuario_id>/eliminar", methods=["POST"])
@login_required
def eliminar(usuario_id):
    buscar_usuario(usuario_id)  # da 404 si no existe
    db = get_db()
    db.execute(queries.USUARIO_ELIMINAR, (usuario_id,))
    db.commit()

    if usuario_id == session["usuario_id"]:  # se borró a sí mismo: cerrar sesión
        session.clear()
        flash("Tu cuenta fue eliminada.", "exito")
        return redirect(url_for("vehiculos.listado"))

    flash("Usuario eliminado.", "exito")
    return redirect(url_for("usuarios.listado"))
