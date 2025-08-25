from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from src.core.usuarios import check_user, find_user_by_email, create_user
from src.core import rol_y_permiso
from flask_session import Session
from jwt import exceptions
from jwt import encode, decode
from src.web.config import Config
from datetime import datetime, timedelta
from flask import jsonify
from src.core import configuracion
from authlib.integrations.flask_client import OAuth


oauth= OAuth()
google= None

def init_app(app):
    """Inicializa la configuracion de OAuth"""
    oauth.init_app(app)
    oauth.register(
        name = 'google',
        client_id = app.config["GOOGLE_CLIENT_ID"],
        client_secret = app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs = {'scope': 'openid email profile'}
    )


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.get("/")
def login():
    """Retorna el html de login"""
    source = request.args.get('source', '')
    return render_template("auth/login.html", source=source)


@auth_blueprint.post("/authenticate")
def authenticate():
    """Autentica al usuario con los datos ingresados por el formulario. Redirecciona dependiendo el resultado."""
    params = request.form
    user = check_user(params["email"], params["password"])
    if not user:
        flash("Email o contraseña incorrectos, o tu cuenta está deshabilitada.", "error")
        return redirect(url_for("auth.login"))

    session["user"] = user.email

    flash("La sesión se inició correctamente", "success")

    if (configuracion.get_configuration().mantenimiento_modo):
        if rol_y_permiso.es_superadmin(session.get("user")):
            return redirect(url_for("configuration.index"))
        else:
            del session["user"]
            session.clear()
            return redirect(url_for("home"))
    return redirect(url_for("home"))


@auth_blueprint.get("/logout")
def logout():
    """Cerrar sesión"""
    source_app = session.get("source-app")
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("La sesion se cerró correctamente.", "info")
    else:
        flash("No hay sesión iniciada.", "info")
    
    if source_app == "app-vue":
        return redirect("http://localhost:5173/")
    else:
        return redirect(url_for("home"))


def expiracion_token(dias):
    """Función que recibe por parametros la cantidad de días que va a tener de vida el token de autenticación"""
    ahora = datetime.now()
    nueva_fecha = ahora + timedelta(dias)
    return nueva_fecha


def generar_token(data):
    """Función para generar un token de autenticación"""
    token = encode(payload={**data, "exp": expiracion_token(1)},
                   key=Config.SECRET_KEY, algorithm="HS256")
    return token.encode("UTF-8")


def validar_token(token="a", salida=False):
    """Función para comprobar que un token es valido. Retorna un json si el parametro salida es falso. Sino retorna el valor del token pero decodificado."""
    try:
        if salida:
            return decode(token, key=Config.SECRET_KEY, algorithms=["HS256"])
        decode(token, key=Config.SECRET_KEY, algorithms=["HS256"])
    except exceptions.DecodeError:
        return jsonify({"error": "token inválido"}), 401
    except exceptions.ExpiredSignatureError:
        return jsonify({"error": "token expirado"}), 401


def validar_token_no_json(token):
    """Retorna un booleano que indica si el token es valido o no"""
    try:
        decode(token, key=Config.SECRET_KEY, algorithms=["HS256"])
        return True
    except exceptions.DecodeError:
        return False
    except exceptions.ExpiredSignatureError:
        return False


@auth_blueprint.post("/google")
def login_with_google():
    """Crea el cliente y redirecciona a la ventana de google para la seleccion de cuenta de google"""
    google= oauth.create_client('google')
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_blueprint.get("/google/authorize")
def authorize():
    """Función que crea el token de google y busca al usuario: si existe crea la sesión, si no, crea al usuario y crea la sesión"""
    google= oauth.create_client('google')
    token = google.authorize_access_token()
    print(token['userinfo'])

    user = find_user_by_email(token['userinfo'].email)
    if not user:
        nombre= token['userinfo'].given_name
        apellido= token['userinfo'].family_name
        email= token['userinfo'].email
        username= token['userinfo'].name
        new_user= create_user(nombre=nombre, apellido=apellido, email=email, username=username, password=username+email, activo=True)
        print('Registrado'+ new_user.email)

    session["user"] = token['userinfo'].email

    flash("La sesión se inició correctamente", "success")
    return redirect(url_for("home"))
