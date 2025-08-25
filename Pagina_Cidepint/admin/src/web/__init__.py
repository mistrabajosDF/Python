from flask import Flask, render_template, session, g, abort
from flask_session import Session
from flask_cors import CORS
from src.web import error
from src.web.controllers.auth import auth_blueprint
from src.web.controllers.register import register_blueprint
from src.web.api.api_methods import api_issue_bp
from src.web.controllers.users import user_bp
from src.web.controllers.services import service_bp
from src.web.controllers.institutions import institution_bp
from src.web.controllers.configuration import configuration_bp
from src.web.controllers.user_service_request import services_request_bp
from src.web.config import config
from src.core import database
from src.core import seeds
from src.core import configuracion
from src.web.helpers.auth import user_is_login
from src.web.helpers import user_inst_rol
from src.web import mail
from src.web.controllers import auth
from src.core import rol_y_permiso

def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)
    CORS(app,  supports_credentials=True, origins=['https://grupo22.proyecto2023.linti.unlp.edu.ar', '*'])
    app.config.from_object(config[env])

    @app.before_request
    def before_request():
        if not hasattr(g, 'instituciones'):
            g.instituciones = user_inst_rol.user_instis()

    auth.init_app(app)
    mail.init_app(app)
    database.init_db(app)

    # Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(institution_bp)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(services_request_bp)
    app.register_blueprint(api_issue_bp)
    app.register_blueprint(configuration_bp)

    @app.get("/")
    @user_inst_rol.add_instis_context
    def home(instituciones):
        super_admin = rol_y_permiso.es_superadmin(session.get("user"))
        if (configuracion.get_configuration().mantenimiento_modo):
            return abort(503)
        else:
            config = configuracion.get_configuration()
            return render_template("home.html", instituciones=instituciones, config=config, super_admin=super_admin)

    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(503, error.service_unavailable)
    app.register_error_handler(405, error.method_not_allowed)

    app.jinja_env.globals.update(user_is_login=user_is_login)


    # Comandos flask añadidos
    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seedsdb")
    def seedsdb():
        seeds.run()

    app.teardown_request(database.close_session)

    return app
