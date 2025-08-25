from flask import render_template
from flask import Blueprint, redirect, url_for
from flask import request
from flask import flash
from flask import session
from src.web import mail
from src.core.usuarios import find_user_by_email, create_user, find_user_by_username, user_register_confirmation
from src.core.usuarios import check_user
from src.web.helpers.site_active import site_active


def validadorCaracteresContraseña(cadena):
    """Método para validar si cumple con las caracteristicas de una contraseña: min. 8 carácteres, al menos 1 letra minúscula, 1 mayúscula, y 1 número. Retorna booleano."""
    # Comprobar si la cadena tiene al menos 8 caracteres
    if len(cadena) < 8:
        return False

    # Inicializar banderas para verificar si hay mayúsculas, minúsculas y números
    tiene_mayuscula = False
    tiene_minuscula = False
    tiene_numero = False

    # Recorrer cada carácter de la cadena
    for caracter in cadena:
        if caracter.isupper():
            tiene_mayuscula = True
        elif caracter.islower():
            tiene_minuscula = True
        elif caracter.isdigit():
            tiene_numero = True

        # Si se cumplen todas las condiciones, podemos salir del bucle temprano
        if tiene_mayuscula and tiene_minuscula and tiene_numero:
            break

    # Comprobar si se cumple al menos una mayúscula, una minúscula y un número
    if tiene_mayuscula and tiene_minuscula and tiene_numero:
        return True
    else:
        return False


register_blueprint = Blueprint("register", __name__, url_prefix="/register")


@register_blueprint.get("/")
@site_active
def show():
    source = request.args.get('source', '')
    return render_template("auth/register.html", source=source)


@register_blueprint.post("/register_user")
@site_active
def register_user():
    params = request.form
    
    # verificar que el user no este ya registrado
    if (find_user_by_username(params["username"])) != None:
        flash("Este nombre de usuario ya se encuentra registrado.", "error")
        return redirect(url_for("register.show"))
    # verificar que el mail no este ya registrado
    if (find_user_by_email(params["email"])) != None:
        flash("Este correo electrónico ya se encuentra registrado.", "error")
        return redirect(url_for("register.show"))
    if not (validadorCaracteresContraseña(params["password"])):
        flash("La contraseña debe tener como mínimo 8 caracteres, al menos una letra mayúscula, una letra minúscula, y un número.", "error")
        return redirect(url_for("register.show"))
    if (params["password"] == params["password2"]):
        # creamos la cuenta
        create_user(nombre=params["name"], apellido=params["surname"], email=params["email"], username=params["username"], password=params["password"], activo=False)
        # enviamos el mail de confirmacion
        if params["source"] == "app-vue":
            mail.send_mail_vue("Confirmación de su registro", params["email"])
        else:
            mail.send_mail("Confirmación de su registro", params["email"])
        flash("Te enviamos un mail, verificalo y segui los pasos para terminar con el registro.", "info")
    else:
        flash("Las contraseñas no coinciden.", "error")
    
    return redirect(url_for("register.show"))


@register_blueprint.get("/confirmation/<string:email>")
@site_active
def confirmation(email):
    user = find_user_by_email(email)
    user_register_confirmation(user.id)
    flash("Tu cuenta ha sido creada correctamente!", "success")
    return redirect(url_for("auth.login"))


@register_blueprint.get("/confirmationVue/<string:email>/")
@site_active
def confirmationVue(email):
    user = find_user_by_email(email)
    user_register_confirmation(user.id)
    flash("Tu cuenta ha sido creada correctamente!", "success")
    return redirect("http://localhost:5173/")
    #return redirect(url_for("https://grupo22.proyecto2023.linti.unlp.edu.ar/"))