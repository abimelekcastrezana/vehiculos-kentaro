from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import queries
from db import get_db
from modules.auth import login_required

bp = Blueprint("vehiculos", __name__)


def validar(form):
    """Revisa el formulario y devuelve una lista con los errores encontrados."""
    db = get_db()
    errores = []

    if not form.get("modelo", "").strip():
        errores.append("El modelo es obligatorio.")
    if not form.get("descripcion", "").strip():
        errores.append("La descripción es obligatoria.")

    anio = form.get("anio", "")
    if not anio.isdigit() or not 1990 <= int(anio) <= 2027:
        errores.append("El año no es válido.")

    try:
        if float(form.get("precio", "")) <= 0:
            errores.append("El precio debe ser mayor que cero.")
    except ValueError:
        errores.append("El precio no es válido.")

    # Marca, tipo y lote deben existir en la base de datos
    if db.execute(queries.MARCA_EXISTE, (form.get("marca_id"),)).fetchone() is None:
        errores.append("Selecciona una marca válida.")
    if db.execute(queries.TIPO_EXISTE, (form.get("tipo_id"),)).fetchone() is None:
        errores.append("Selecciona un tipo válido.")
    if db.execute(queries.LOTE_EXISTE, (form.get("lote_id"),)).fetchone() is None:
        errores.append("Selecciona un lote válido.")

    url = form.get("imagen_url", "").strip()
    if url and not url.startswith(("http://", "https://")):
        errores.append("La URL de la imagen debe empezar con http:// o https://")

    return errores


def buscar_vehiculo(vehiculo_id):
    vehiculo = get_db().execute(queries.VEHICULO_BUSCAR, (vehiculo_id,)).fetchone()
    if vehiculo is None:
        abort(404)
    return vehiculo


@bp.route("/")
def listado():
    vehiculos = get_db().execute(queries.VEHICULOS_LISTAR).fetchall()
    return render_template("listado.html", vehiculos=vehiculos)


@bp.route("/vehiculos/<int:vehiculo_id>")
def detalle(vehiculo_id):
    return render_template("detalle.html", vehiculo=buscar_vehiculo(vehiculo_id))


@bp.route("/vehiculos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    db = get_db()

    if request.method == "POST":
        form = request.form
        errores = validar(form)

        if errores:
            for error in errores:
                flash(error, "error")
        else:
            cursor = db.execute(
                queries.VEHICULO_CREAR,
                (form["marca_id"], form["tipo_id"], form["lote_id"], form["modelo"].strip(),
                 form["anio"], form["precio"], form["descripcion"].strip(), form["imagen_url"].strip()),
            )
            db.commit()
            flash("Vehículo publicado.", "exito")
            return redirect(url_for("vehiculos.detalle", vehiculo_id=cursor.lastrowid))

    # GET, o POST con errores: se vuelve a mostrar el formulario
    return render_template(
        "nuevo.html",
        datos=request.form,  # vacío en GET; conserva lo escrito si hubo errores
        marcas=db.execute(queries.MARCAS_LISTAR).fetchall(),
        tipos=db.execute(queries.TIPOS_LISTAR).fetchall(),
        lotes=db.execute(queries.LOTES_LISTAR).fetchall(),
    )


@bp.route("/vehiculos/<int:vehiculo_id>/editar", methods=["GET", "POST"])
@login_required
def editar(vehiculo_id):
    db = get_db()
    vehiculo = buscar_vehiculo(vehiculo_id)
    datos = vehiculo  # en GET el formulario se llena con los datos guardados

    if request.method == "POST":
        form = request.form
        datos = form  # si hay errores, se conserva lo que escribió el usuario
        errores = validar(form)

        if errores:
            for error in errores:
                flash(error, "error")
        else:
            db.execute(
                queries.VEHICULO_ACTUALIZAR,
                (form["marca_id"], form["tipo_id"], form["lote_id"], form["modelo"].strip(),
                 form["anio"], form["precio"], form["descripcion"].strip(), form["imagen_url"].strip(),
                 vehiculo_id),
            )
            db.commit()
            flash("Vehículo actualizado.", "exito")
            return redirect(url_for("vehiculos.detalle", vehiculo_id=vehiculo_id))

    return render_template(
        "editar.html",
        vehiculo=vehiculo,
        datos=datos,
        marcas=db.execute(queries.MARCAS_LISTAR).fetchall(),
        tipos=db.execute(queries.TIPOS_LISTAR).fetchall(),
        lotes=db.execute(queries.LOTES_LISTAR).fetchall(),
    )


@bp.route("/vehiculos/<int:vehiculo_id>/eliminar", methods=["POST"])
@login_required
def eliminar(vehiculo_id):
    buscar_vehiculo(vehiculo_id)  # da 404 si no existe
    db = get_db()
    db.execute(queries.VEHICULO_ELIMINAR, (vehiculo_id,))
    db.commit()
    flash("Vehículo eliminado.", "exito")
    return redirect(url_for("vehiculos.listado"))
