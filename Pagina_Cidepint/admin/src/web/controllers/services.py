from flask import render_template, request, flash, g
from src.core import servicios, instituciones, configuracion
from flask import Blueprint
from src.core.instituciones import find_institution_by_id
import math
from src.web.helpers.auth import login_required
from src.web.helpers.site_active import site_active
from src.web.helpers import validadores, paginado
from src.web.helpers.permisos import requiere_parcialmente_permisos_servicios, requiere_todos_permisos_servicios

service_bp = Blueprint("services", __name__, url_prefix="/servicios")


@service_bp.route("/", methods=["GET", "POST"])
@site_active
@login_required
def index():
    """Lista los servicios de la bd"""
    pagina = request.args.get('page', type=int)
    if not pagina or pagina < 0:
        pagina = 1

    inicio, fin = paginado.paginar(pagina)

    services = list(servicios.listar_con_palabras_centros())
    services = services[inicio - 1:fin]

    instituciones = g.instituciones
    id_institucion = request.args.get('id_institucion', type=int)
    institucion_actual = find_institution_by_id(id_institucion)
    return render_template("services/index.html", services=services, instituciones=instituciones, institucion_actual=institucion_actual, page=pagina)


@service_bp.route("/add", methods=["POST"])
@site_active
@login_required
@requiere_parcialmente_permisos_servicios
def add():
    """Agrega un servicio en la bd"""
    if not (servicios.buscar_servicio_por_nombre(request.form.get("nombre"))):
        if request.form.get("habilitado") == "True":
            hab = True
        else:
            hab = False
        if validadores.no_vacio_ni_50(request.form.get("nombre")):
            s1 = servicios.create_service(
                nombre=request.form.get("nombre"),
                descripcion=request.form.get("descripcion"),
                tipo=request.form.get("tipo"),
                habilitado=hab, )

            # Centros a cargo
            if request.form.get("centro") != "":
                i = instituciones.get_institucion_id(
                    request.form.get("centro"))
                servicios.assign_institution_service(s1, [i])

            # Palabras clave
            if request.form.get("palabrasclave") != "":
                palabrasclave = (request.form.get("palabrasclave")).replace(
                    " ", "").upper().split(sep=",")
                for palabra in palabrasclave:
                    if validadores.no_vacio_ni_50(palabra):
                        if not (servicios.buscar_palabra_por_nombre(palabra)):
                            p = servicios.create_key_word_serv(name=palabra)
                        else:
                            p = servicios.buscar_palabra_por_nombre(palabra)
                        servicios.assign_keyword_serv(s1, [p])
        else:
            flash("Ingrese un nombre para el servicio", "error")
    else:
        flash("Ya existe un servicio con ese nombre, por favor, agregele su centro o use otro nombre", "error")

    id_institucion = request.args.get('id_institucion', type=int)
    institucion_actual = find_institution_by_id(id_institucion)

    services = list(servicios.list_services())
    pagina = int(math.ceil(len(services) / configuracion.item_per_page()))
    inicio, fin = paginado.paginar(pagina)
    services = services[inicio - 1:fin]

    instituciones_context = g.instituciones
    return render_template("services/index.html", services=services, institucion_actual=institucion_actual, page=pagina, instituciones=instituciones_context)


@service_bp.route('/delete/<int:id>', methods=['GET'])
@site_active
@login_required
@requiere_todos_permisos_servicios
def delete(id):
    """Elimina un servicio de la bd"""
    centros = servicios.get_centros_a_cargo(id)

    id_institucion = request.args.get('id_institucion', type=int)
    institucion_actual = find_institution_by_id(id_institucion)
    i = [institucion_actual]
    if centros == i or centros == []:
        s = servicios.delete_service(id)
        try:
            message = "Servicio {} eliminado".format(s.nombre)
            flash(message, "success")
        except:
            flash(
                "El servicio no pudo ser eliminado por tener solicitudes pendientes.", "error")
    else:
        flash("El servicio no pudo ser eliminado por pertenecer a otros centros.", "error")
    services = list(servicios.list_services())
    pagina = int(math.ceil(len(services) / configuracion.item_per_page()))
    inicio, fin = paginado.paginar(pagina)
    services = services[inicio - 1:fin]

    instituciones_context = g.instituciones
    return render_template("services/index.html", services=services, institucion_actual=institucion_actual, instituciones=instituciones_context, page=pagina)


@service_bp.route('/updatea/<int:id>', methods=['GET'])
@site_active
@login_required
def updatea(id):
    """Redirecciona a la pantalla de edicion de servicios"""
    servicio_a_actualizar = servicios.get_servicio_id(id)

    id_institucion = request.args.get('id_institucion', type=int)
    institucion_actual = find_institution_by_id(id_institucion)
    instituciones_context = g.instituciones
    return render_template("services/update_serv.html", service=servicio_a_actualizar, institucion_actual=institucion_actual, instituciones=instituciones_context)


@service_bp.route("/update", methods=['POST'])
@site_active
@login_required
def update():
    """Modifica un servicio en la bd"""
    servicio = servicios.get_servicio_id(request.form.get("id"))
    form = request.form

    # --- Campos básicos con validadores ---
    campos = {
        "nombre": (validadores.no_vacio_ni_50, lambda val: not servicios.buscar_servicio_por_nombre_repetido(val, exclude_id=servicio.id),
                   "Error, ya existe otro servicio con ese nombre"),
        "descripcion": (validadores.no_vacio_ni_100, None, None),
        "tipo": (validadores.no_vacio_ni_50, None, None)
    }

    for campo, (validador, condicion, msg_error) in campos.items():
        valor = form.get(campo)
        if valor and validador(valor):
            if condicion and not condicion(valor):
                flash(msg_error, "error")
            else:
                setattr(servicio, campo, valor)

    # --- Campo habilitado ---
    habilitado = form.get("habilitado")
    if habilitado != "":
        servicio.habilitado = habilitado == "True"

    # --- Centros a cargo ---
    centro = form.get("centro")
    if centro and not servicios.buscar_palabra_por_nombre(centro):
        i = instituciones.buscar_institucion_por_nombre(centro)
        servicios.assign_institution_service(servicio, [i])

    # --- Palabras clave ---
    palabras = form.get("palabrasclave")
    if palabras:
        for palabra in palabras.replace(" ", "").upper().split(","):
            if validadores.no_vacio_ni_50(palabra):
                p = servicios.buscar_palabra_por_nombre(palabra) or servicios.create_key_word_serv(name=palabra)
                servicios.assign_keyword_serv(servicio, [p])

    # --- Desvincular palabra clave ---
    palabra_elim = form.get("palabra_eliminada")
    if palabra_elim:
        try:
            palabra = servicios.buscar_palabra_por_nombre(palabra_elim.upper())
            servicios.desvincular_palabra_clave(servicio, palabra)
        except:
            flash("Error, la palabra que quiere eliminar no existe o no está vinculada", "error")

    # --- Desvincular centro a cargo ---
    if form.get("centro_eliminado") == "Si":
        try:
            centro = instituciones.buscar_institucion_por_nombre(form.get("centro"))
            servicios.desvincular_centro(servicio, centro)
        except:
            flash("Error, el centro que quiere eliminar no existe o no está vinculado", "error")

    # --- Guardar cambios ---
    servicios.update_service(servicio)
    flash(f"Los campos correctos del servicio {servicio.nombre} han sido actualizados", "success")

    id_institucion = request.args.get('id_institucion', type=int)
    institucion_actual = find_institution_by_id(id_institucion)

    services = list(servicios.list_services())
    pagina = int(math.ceil(len(services) / configuracion.item_per_page()))
    inicio, fin = paginado.paginar(pagina)
    services = services[inicio - 1:fin]
    instituciones_context = g.instituciones

    return render_template(
        "services/index.html",
        services=services,
        institucion_actual=institucion_actual,
        instituciones=instituciones_context,
        page=pagina
    )
