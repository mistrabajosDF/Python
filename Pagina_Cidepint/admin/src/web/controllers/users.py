from flask import render_template, g, request, flash
from src.core import usuarios, configuracion, instituciones, rol_y_permiso
from flask import Blueprint
from flask import session
from src.core.bcrypt import bcrypt
from src.web.helpers.auth import login_required
from src.web.helpers.site_active import site_active
import math
from src.core.instituciones import find_institution_by_id
from src.web.helpers import validadores, paginado
from src.web.helpers.permisos import requiere_permisos_superadmin, requiere_permisos_miembros

user_bp = Blueprint("users", __name__, url_prefix="/usuarios")


@user_bp.route("/", methods=["GET", "POST"])
@site_active
@login_required
@requiere_permisos_superadmin
def index():
    """Lista los usuarios de la base de datos"""
    super_admin = rol_y_permiso.es_superadmin(session.get("user"))
    pagina = request.args.get('page', type=int)
    if not pagina or pagina < 0:
        pagina = 1
    inicio, fin = paginado.paginar(pagina)

    users = usuarios.user_index()
    users = users[inicio - 1:fin]

    instis_context = g.instituciones
    return render_template("users/index.html", users=users, instituciones=instis_context, page=pagina, super_admin=super_admin)


def new():
    users = usuarios.create_user()


@user_bp.route("/updatea")
@site_active
@login_required
def updatea():
    """Redirecciona a la pantalla de edicion de usuario"""
    usuario_a_actualizar = usuarios.user_search_email(session.get("user"))
    instituciones = g.instituciones
    super_admin = rol_y_permiso.es_superadmin(session.get("user"))
    return render_template("users/editar_user.html", user=usuario_a_actualizar, instituciones=instituciones, super_admin=super_admin)


@user_bp.route("/update", methods=['POST'])
@site_active
@login_required
def update():
    """Modifica un usuario en la bd"""
    usuario = usuarios.user_search_email(session.get("user"))
    form = request.form

    # --- Campos básicos con validadores ---
    campos_validar = {
        "nombre": [validadores.no_vacio_ni_50, validadores.solo_letras],
        "apellido": [validadores.no_vacio_ni_50, validadores.solo_letras],
        "username": [validadores.no_vacio_ni_50]
    }

    for campo, reglas in campos_validar.items():
        valor = form.get(campo)
        if valor and all(regla(valor) for regla in reglas):
            if campo == "username" and usuarios.find_user_by_username(valor):
                flash("Este nombre de usuario ya se encuentra registrado.", "error")
            else:
                setattr(usuario, campo, valor)

    # --- Campo activo ---
    activo_val = form.get("activo")
    if activo_val != "":
        usuario.activo = activo_val == "True"
        if not usuario.activo:
            flash(
                "Desactivaste tu cuenta. Cuando cierres sesión no podrás volver a ingresar.", "error"
            )

    # --- Actualizar contraseña ---
    new_contra = form.get("new_contra")
    contra_ant = form.get("contra_ant")
    if new_contra:
        if usuarios.check_user(form.get("mail"), contra_ant):
            if validadores.validadorCaracteres(new_contra):
                usuario.password = bcrypt.generate_password_hash(
                    new_contra.encode("utf-8")
                ).decode("utf-8")
            else:
                flash(
                    "La contraseña debe tener como mínimo 8 caracteres, al menos una letra mayúscula, una letra minúscula, y un número",
                    "error"
                )
        else:
            flash("La contraseña actual no coincide, reintente.", "error")

    # --- Guardar cambios ---
    usuarios.user_update(usuario)
    flash(f"Los campos correctos del usuario {usuario.nombre} han sido actualizados", "success")

    super_admin = rol_y_permiso.es_superadmin(session.get("user"))
    return render_template("home.html", instituciones=g.instituciones, super_admin=super_admin)



@user_bp.route('/delete/<int:id>', methods=['GET'])
@site_active
@login_required
@requiere_permisos_superadmin
def delete(id):
    """Elimina un usuario de la bd"""
    if usuarios.get_usuario_id(id) != usuarios.user_search_email(session.get("user")):
        if not rol_y_permiso.es_superadmin(usuarios.get_usuario_id(id).email):
            u = usuarios.user_delete(id)
            try:
                message = "El usuario {} fue eliminado".format(u.nombre)
                flash(message, "success")
            except:
                flash(
                    "El usuario no puede ser eliminado por tener solicitudes pendientes", "error")
        else:
            flash("Este usuario es superadmin, no puede eliminarse", "error")
    else:
        flash("No podés eliminar tu propia cuenta", "error")
    users = usuarios.user_index()
    pagina = int(math.ceil(len(users) / configuracion.item_per_page()))
    inicio, fin = paginado.paginar(pagina)
    users = users[inicio - 1:fin]
    super_admin = rol_y_permiso.es_superadmin(session.get("user"))
    instituciones = g.instituciones
    return render_template("users/index.html", users=users, instituciones=instituciones, page=pagina, super_admin=super_admin)


@user_bp.post("/filtrar")
@site_active
@login_required
@requiere_permisos_superadmin
def filtrar():
    """Filtra usuarios por mail y estado (Activo o no)."""
    instituciones = g.instituciones
    super_admin = rol_y_permiso.es_superadmin(session.get("user"))
    users = usuarios.user_index()
    if request.form.get("filtro_mail") == "":
        filtro_mail = ""
    else:
        filtro_mail = request.form.get("filtro_mail")
    if request.form.get("filtro_activo") == "":
        filtro_activo = ""
    elif request.form.get("filtro_activo") == "True":
        filtro_activo = True
    elif request.form.get("filtro_activo") == "False":
        filtro_activo = False

    users_filtro = []
    for user in users:
        if (filtro_activo == "") or (user.activo == filtro_activo):
            if (filtro_mail == "") or (filtro_mail.lower() in user.email.lower()):
                users_filtro.append(user)

    pagina = 1
    inicio, fin = paginado.paginar(pagina)
    users_filtro = users_filtro[inicio - 1:fin]
    if users_filtro == []:
        flash("No se encontraron usuarios con los criterios solicitados", "error")
    return render_template("users/index.html", users=users_filtro, instituciones=instituciones, page=pagina, super_admin=super_admin)


@user_bp.route("/actualizar_estado/<int:id>", methods=['POST'])
@site_active
@login_required
@requiere_permisos_superadmin
def actualizar_estado(id):
    """Modifica un usuario en la bd"""
    usuario_a_actualizar = usuarios.get_usuario_id(id)
    if request.form.get("activo") != "":
        if request.form.get("activo") == "True":
            usuario_a_actualizar.activo = True
        else:
            usuario_a_actualizar.activo = False

        usuarios.user_update(usuario_a_actualizar)

        message = "El estado del usuario {} ha sido actualizado".format(
            usuario_a_actualizar.nombre)
        flash(message, "success")

    users = usuarios.user_index()
    pagina = int(math.ceil(len(users) / configuracion.item_per_page()))
    inicio, fin = paginado.paginar(pagina)
    users = users[inicio - 1:fin]
    users = usuarios.user_index()
    pagina = int(math.ceil(len(users) / configuracion.item_per_page()))
    inicio, fin = paginado.paginar(pagina)
    users = users[inicio - 1:fin]

    instituciones = g.instituciones
    return render_template("users/index.html", instituciones=instituciones, users=users, page=pagina)
    instituciones = g.instituciones
    return render_template("users/index.html", instituciones=instituciones, users=users, page=pagina)


@user_bp.route("/agregar_rol/<int:id>", methods=["GET", "POST"])
@site_active
@login_required
def agregar_rol(id):
    """Asigna un rol a un usuario en la institución activa"""
    user = usuarios.get_usuario_id(id)
    """Asigna un rol a un usuario en la institución activa"""
    user = usuarios.get_usuario_id(id)

    # Verifica si el rol ya existe
    if not rol_y_permiso.buscar_rol_por_nombre(request.form.get("rol")):
        rol = rol_y_permiso.create_role(name=request.form.get("rol"))
    else:
        rol = rol_y_permiso.buscar_rol_por_nombre(request.form.get("rol"))

    id_institucion = request.args.get('id_institucion', type=int)
    insti1 = find_institution_by_id(id_institucion)

    agregado = usuarios.assign_institution_role(user, insti1, rol)
    if agregado:
        message = "Se le ha asignado el rol seleccionado al usuario {}".format(
            user.nombre)
        flash(message, "success")
    else:
        message = "El usuario {} ya tenia un rol asignado".format(
            user.nombre)
        flash(message, "error")
    users = usuarios.user_index()
    pagina = int(math.ceil(len(users) / configuracion.item_per_page()))
    inicio, fin = paginado.paginar(pagina)
    users = users[inicio - 1:fin]

    instis = g.instituciones
    return render_template("users/users_de_insti.html", users=users, instituciones=instis, page=pagina, institucion_actual=insti1)


@user_bp.route("/lista_insti", methods=["GET", "POST"])
@site_active
@login_required
def lista_insti():
    pagina = request.args.get('page', type=int)
    if not pagina or pagina < 0:
        pagina = 1
    inicio, fin = paginado.paginar(pagina)

    users = usuarios.user_index()
    users = users[inicio - 1:fin]

    id_institucion = request.args.get('id_institucion', type=int)
    institucion_actual = find_institution_by_id(id_institucion)

    instis_context = g.instituciones
    return render_template("users/users_de_insti.html", users=users, instituciones=instis_context, institucion_actual=institucion_actual, page=pagina)


@user_bp.route("/filtrar_insti/<int:id>", methods=["GET", "POST"])
@site_active
@login_required
def filtrar_insti(id):
    """Filtra usuarios por mail y estado (Activo o no)."""
    instituciones = g.instituciones
    # id_institucion = request.args.get('id_institucion', type=int)
    institucion_actual = find_institution_by_id(id)

    users = usuarios.user_index()
    if request.form.get("filtro_mail") == "":
        filtro_mail = ""
    else:
        filtro_mail = request.form.get("filtro_mail")
    if request.form.get("filtro_activo") == "":
        filtro_activo = ""
    elif request.form.get("filtro_activo") == "True":
        filtro_activo = True
    elif request.form.get("filtro_activo") == "False":
        filtro_activo = False

    users_filtro = []
    for user in users:
        if (filtro_activo == "") or (user.activo == filtro_activo):
            if (filtro_mail == "") or (filtro_mail.lower() in user.email.lower()):
                users_filtro.append(user)

    pagina = 1
    inicio, fin = paginado.paginar(pagina)
    users_filtro = users_filtro[inicio - 1:fin]
    if users_filtro == []:
        flash("No se encontraron usuarios con los criterios solicitados", "error")
    return render_template("users/users_de_insti.html", users=users_filtro, instituciones=instituciones, page=pagina, institucion_actual=institucion_actual)
