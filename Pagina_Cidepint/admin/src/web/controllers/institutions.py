from flask import render_template, request, flash, g, session
from src.core import instituciones, configuracion, rol_y_permiso
from flask import Blueprint
from src.core.instituciones import find_institution_by_id, buscar_institucion_por_nombre_repetido
import re
import math
from src.web.helpers.auth import login_required
from src.web.helpers.site_active import site_active
from src.web.helpers import validadores, paginado
from src.web.helpers.permisos import requiere_permisos_superadmin, requiere_todos_permisos_servicios

institution_bp = Blueprint("institutions", __name__,
                           url_prefix="/instituciones")


@institution_bp.route("/", methods=["GET", "POST"])
@site_active
@login_required
@requiere_permisos_superadmin
def index():
    """Lista las instituiones de la bd"""
    super_admin = rol_y_permiso.es_superadmin(session.get("user"))
    pagina = request.args.get('page', type=int)
    if not pagina or pagina < 0:
        pagina = 1
    inicio, fin = paginado.paginar(pagina)

    institutions = list(instituciones.listar_con_palabras())
    institutions = institutions[inicio - 1:fin]

    instituciones_context = g.instituciones
    return render_template("institutions/index.html", institutions=institutions, instituciones=instituciones_context, page=pagina, super_admin=super_admin)


@institution_bp.get("/<int:id_institucion>")
@site_active
@login_required
def home(id_institucion):
    instituciones = g.instituciones
    institucion_actual = find_institution_by_id(id_institucion)

    return render_template("institutions/home_inst.html", instituciones=instituciones, institucion_actual=institucion_actual)


@institution_bp.route("/add", methods=["POST"])
@site_active
@login_required
@requiere_permisos_superadmin
def add():
    """Agrega una institucion en la bd"""
    if not (instituciones.buscar_institucion_por_nombre(request.form.get("nombre"))):
        if request.form.get("habilitada") == "True":
            hab = True
        else:
            hab = False
        if validadores.coordenadas(request.form.get("localizacion")):
            if validadores.no_vacio_ni_50(request.form.get("nombre")):
                i1 = instituciones.create_institution(
                    nombre=request.form.get("nombre"),
                    informacion=request.form.get("informacion"),
                    direccion=request.form.get("direccion"),
                    localizacion=request.form.get("localizacion"),
                    paginaweb=request.form.get("paginaweb"),
                    diasyhorarios=request.form.get("diasyhorarios"),
                    contacto=request.form.get("contacto"),
                    habilitada=hab, )

                # Palabras clave
                if request.form.get("palabrasclave") != "":
                    palabrasclave = (request.form.get("palabrasclave")).replace(
                        " ", "").upper().split(sep=",")
                    for palabra in palabrasclave:
                        if not (instituciones.buscar_palabra_por_nombre(palabra)):
                            p = instituciones.create_key_word(name=palabra)
                        else:
                            p = instituciones.buscar_palabra_por_nombre(
                                palabra)
                        instituciones.assign_keyword(i1, [p])
            else:
                flash("Debes ingresar un nombre", "error")
        else:
            flash("Las coordenadas ingresadas no son válidas. Ejemplo de formato correcto: -34.91, -57.94", "error")
    else:
        flash("Ya existe una institucion con ese nombre", "error")

    institutions = list(instituciones.listar_con_palabras())
    pagina = int(math.ceil(len(institutions) / configuracion.item_per_page()))
    inicio, fin = paginado.paginar(pagina)
    institutions = institutions[inicio - 1:fin]
    super_admin = rol_y_permiso.es_superadmin(session.get("user"))
    instituciones_context = g.instituciones
    return render_template("institutions/index.html", institutions=institutions, instituciones=instituciones_context, page=pagina, super_admin=super_admin)


@institution_bp.route('/delete/<int:id>', methods=['GET'])
@site_active
@login_required
@requiere_permisos_superadmin
def delete(id):
    """Elimina una institucion de la bd"""
    i = instituciones.delete_insitutution(id)
    try:
        message = "Institucion {} eliminada".format(i.nombre)
        flash(message, "success")
    except:
        flash(
            "La institucion no pudo ser eliminada por tener solicitudes pendientes", "error")
    institutions = list(instituciones.listar_con_palabras())
    pagina = int(math.ceil(len(institutions) / configuracion.item_per_page()))
    inicio, fin = paginado.paginar(pagina)
    institutions = institutions[inicio - 1:fin]
    super_admin = rol_y_permiso.es_superadmin(session.get("user"))
    instituciones_context = g.instituciones
    return render_template("institutions/index.html", institutions=institutions, instituciones=instituciones_context, page=pagina, super_admin=super_admin)


@institution_bp.route('/updatea', methods=['GET'])
@site_active
@login_required
def updatea():
    """Redirecciona a la pantalla de edicion de instituciones"""
    id_institucion = request.args.get('id_institucion', type=int)
    institucion_a_actualizar = instituciones.get_institucion_id(id_institucion)
    institucion_actual = find_institution_by_id(id_institucion)
    instituciones_context = g.instituciones
    return render_template("institutions/update_inst.html", institution=institucion_a_actualizar, institucion_actual=institucion_actual, instituciones=instituciones_context)


@institution_bp.route("/update", methods=["POST"])
@site_active
@login_required
def update():
    """Modifica una institucion en la bd"""
    institucion = instituciones.get_institucion_id(request.form.get("id"))
    form = request.form

    # --- Campos simples con validadores ---
    campos = {
        "nombre": (validadores.no_vacio_ni_50, lambda val: not buscar_institucion_por_nombre_repetido(val, exclude_id=institucion.id),
                   "El nombre no se ha podido editar, ya existe otra institucion con el mismo"),
        "informacion": (validadores.no_vacio_ni_100, None, None),
        "direccion": (validadores.no_vacio_ni_100, None, None),
        "paginaweb": (validadores.no_vacio_ni_50, None, None),
        "diasyhorarios": (validadores.no_vacio_ni_100, None, None),
        "contacto": (validadores.no_vacio_ni_50, None, None)
    }

    for campo, (validador, condicion, msg_error) in campos.items():
        valor = form.get(campo)
        if valor and validador(valor):
            if condicion and not condicion(valor):
                flash(msg_error, "error")
            else:
                setattr(institucion, campo, valor)

    # --- Campo localizacion ---
    loc = form.get("localizacion")
    if loc and validadores.no_vacio_ni_100(loc):
        if validadores.coordenadas(loc):
            institucion.localizacion = loc
        else:
            flash("Las coordenadas ingresadas no son válidas. Ejemplo de formato correcto: -34.91, -57.94", "error")

    # --- Campo habilitada ---
    habilitada = form.get("habilitada")
    if habilitada != "":
        institucion.habilitada = habilitada == "True"

    # --- Palabras clave ---
    palabras = form.get("palabrasclave")
    if palabras:
        for palabra in palabras.replace(" ", "").upper().split(","):
            if validadores.no_vacio_ni_50(palabra):
                p = instituciones.buscar_palabra_por_nombre(palabra) or instituciones.create_key_word(name=palabra)
                instituciones.assign_keyword(institucion, [p])

    # --- Desvincular palabra clave ---
    palabra_elim = form.get("palabra_eliminada")
    if palabra_elim:
        try:
            palabra = instituciones.buscar_palabra_por_nombre(palabra_elim.upper())
            instituciones.desvincular_palabra_clave(institucion, palabra)
        except:
            flash("Error, la palabra que quiere eliminar no existe o no está vinculada", "error")

    # --- Guardar cambios ---
    instituciones.update_institution(institucion)
    flash(f"Los campos correctos de la institución {institucion.nombre} han sido actualizados", "success")

    id_institucion = request.args.get('id_institucion', type=int)
    institucion_actual = find_institution_by_id(id_institucion)
    return render_template(
        "institutions/update_inst.html",
        institution=institucion,
        institucion_actual=institucion_actual,
        instituciones=g.instituciones
    )
