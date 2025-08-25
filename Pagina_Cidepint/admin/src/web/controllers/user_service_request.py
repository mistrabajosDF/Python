from flask import render_template, g, redirect, url_for
from flask import Blueprint
from flask import request
from flask import jsonify, flash
from datetime import datetime
from src.core.database import db
import math
from src.core.instituciones import find_institution_by_id
from src.core.solicitudes import list_services_requests, get_solicitud_id
from src.core.solicitudes import list_notes_by_request_id
from src.core.solicitudes import get_request_by_id
from src.core.solicitudes import create_note
from src.core.solicitudes import solicitud_delete, eliminar_notas

from src.web.helpers.auth import login_required
from src.web.helpers.user_inst_rol import get_filtered_service_requests

from src.web.helpers.site_active import site_active
from src.web.helpers.permisos import requiere_parcialmente_permisos_solicitudes, requiere_todos_permisos_solicitudes
# cuando este el delete/destroy, usar decorador requiere_todos_permisos_solicitudes. Igual tambien fijarse como obtener id de la institucion porque por alguna extraña razon lo perdemos
from src.core import configuracion
from src.web.helpers import paginado, validadores

services_request_bp = Blueprint(
    "solicitudes", __name__, url_prefix="/solicitudes")


@services_request_bp.get("/")
@site_active
@login_required
def index():
    """Listas las solicitudes de una institucion dada"""
    instituciones = g.instituciones
    id_institucion = request.args.get('id_institucion', type=int)
    institucion_actual = find_institution_by_id(id_institucion)
    req = list_services_requests(id_institucion)

    pagina = request.args.get('page', type=int)
    if not pagina or pagina < 0:
        pagina = 1
    inicio, fin = paginado.paginar(pagina)
    req = req[inicio - 1:fin]

    return render_template("user_service_request/index.html", solicitudes=req, instituciones=instituciones, institucion_actual=institucion_actual, page=pagina)


@services_request_bp.get("/notas/<int:id_solicitud>")
@site_active
@login_required
def obtener_notas(id_solicitud):
    """Devuelve las notas de una solicitud"""
    print("==============================================")
    print(id_solicitud)
    notas = list_notes_by_request_id(id_solicitud)
    if notas is not None:
        notas_serializadas = [nota.as_dict() for nota in notas]
        return jsonify(notas_serializadas)
    else:
        return []


@services_request_bp.post("/actualizar")
@site_active
@login_required
def actualizar_estado():
    """Actualiza el estado de una solicitud y permite ingresar una observacion de estado"""
    inst_actual = int(request.form.get("id_institucion"))
    id = int(request.form.get("id_solicitud"))
    solicitud = get_request_by_id(int(request.form.get("id_solicitud")))
    if (request.form.get("status")) != "":
        if validadores.no_vacio_ni_100(request.form.get("obs_est_act")):
            solicitud.obs_est_act = request.form.get('obs_est_act')
        solicitud.status = request.form.get('status')
        solicitud.change_status_date = datetime.utcnow()
        db.session.commit()
    else:
        flash("Tenés que seleccionar un estado válido", "error")
    return redirect(url_for('solicitudes.detalle', id_institucion=inst_actual, id=id))


@services_request_bp.post("/filtrar")
@site_active
@login_required
def filtrar_solicitudes():
    """
        Filtra las solicitudes de acuerdo a los parámetros recibidos.
    """
    instituciones = g.instituciones
    id_institucion = int(request.form.get('id_institucion'))
    institucion_actual = find_institution_by_id(id_institucion)

    solicitudes = list_services_requests(id_institucion)

    type_filter = request.form.get('filtro_tipo')
    status_filter = request.form.get('filtro_estado')
    client_filter = request.form.get('filtro_cliente')
    start_date = request.form.get('fecha_inicio')
    end_date = request.form.get('fecha_fin')
    solicitudes_filtradas = get_filtered_service_requests(
        solicitudes, type_filter, status_filter, client_filter, start_date, end_date)
    # Paginado
    pagina = request.args.get('page', type=int)
    if not pagina or pagina < 0:
        pagina = 1
    inicio, fin = paginado.paginar(pagina)
    solicitudes_filtradas = solicitudes_filtradas[inicio - 1:fin]
    return render_template("user_service_request/index.html", solicitudes=solicitudes_filtradas, instituciones=instituciones, institucion_actual=institucion_actual, page=pagina)


@services_request_bp.post("/agregar_nota")
@site_active
@login_required
def agregar_nota():
    """Agrega una nota a una solicitud"""
    inst_actual = int(request.form.get("id_institucion"))
    id = int(request.form.get("id_solicitud"))
    solicitud = get_request_by_id(int(request.form.get("id_solicitud")))
    if validadores.no_vacio_ni_250(request.form.get("nota_nueva")):
        n = create_note(request_id=solicitud.id,
                        description=request.form.get("nota_nueva"))

    return redirect(url_for('solicitudes.detalle', id_institucion=inst_actual, id=id))


@services_request_bp.route('/delete/<int:id>', methods=['GET'])
@site_active
@login_required
def delete(id):
    """Elimina una solicitud de la bd"""
    id_institucion = request.args.get('id_institucion', type=int)
    inst_actual = find_institution_by_id(id_institucion)
    solicitud = get_request_by_id(id)
    notas = eliminar_notas(id)
    s = solicitud_delete(id)
    message = "La solicitud {} fue eliminada".format(s.id)
    flash(message, "success")
    req = list_services_requests(id_institucion)
    pagina = int(math.ceil(len(req) / configuracion.item_per_page()))
    inicio, fin = paginado.paginar(pagina)
    req = req[inicio - 1:fin]
    instituciones = g.instituciones
    return render_template("user_service_request/index.html", solicitudes=req, instituciones=instituciones,
                           institucion_actual=inst_actual, page=pagina)


@services_request_bp.route('/detalle/<int:id>', methods=['GET'])
@site_active
@login_required
def detalle(id):
    """Redirecciona a la pantalla de detalle de una solicitud de la bd"""
    solicitud = get_solicitud_id(id)
    id_institucion = request.args.get('id_institucion', type=int)
    institucion_actual = find_institution_by_id(id_institucion)
    instituciones_context = g.instituciones
    notas = list_notes_by_request_id(id)
    return render_template("user_service_request/detalle_solicitud.html", solicitud=solicitud,
                           institucion_actual=institucion_actual, instituciones=instituciones_context, notas=notas)

