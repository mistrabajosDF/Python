from flask import render_template, request, flash, g, session
from src.core import configuracion, rol_y_permiso
from flask import Blueprint
from src.web.helpers.auth import login_required
from src.web.helpers.permisos import requiere_permisos_superadmin
from src.web.helpers import validadores


configuration_bp = Blueprint(
    "configuration", __name__, url_prefix="/configuracion")


@configuration_bp.get("/")
@login_required
@requiere_permisos_superadmin
def index():
    """Lista la configuracion de la bd"""
    super_admin = request.args.get('super_admin')
    config = configuracion.get_configuration()
    instituciones_context = g.instituciones
    return render_template("configuration/edit_config.html", configuration=config, instituciones=instituciones_context, super_admin=super_admin)


@configuration_bp.route("/update", methods=["POST"])
@login_required
@requiere_permisos_superadmin
def update():
    """Modifica la configuracion en la bd"""
    config = configuracion.get_configuration()
    if request.form.get("items") != "" and validadores.solo_numeros(request.form.get("items")):
        config.items_por_pagina = request.form.get("items"),
    if validadores.no_vacio_ni_50(request.form.get("contacto")):
        config.info_contacto = request.form.get("contacto"),
    if validadores.no_vacio_ni_100(request.form.get("mensaje")):
        config.mantenimiento_mensaje = request.form.get("mensaje"),
    if request.form.get("mantenimiento") != "":
        if request.form.get("mantenimiento") == "True":
            config.mantenimiento_modo = True
        else:
            config.mantenimiento_modo = False
    super_admin = rol_y_permiso.es_superadmin(session.get("user"))
    configuracion.update(config)
    message = "Los campos correctos han sido actualizados"
    flash(message, "success")

    return render_template("configuration/edit_config.html", configuration=config, super_admin=super_admin)
