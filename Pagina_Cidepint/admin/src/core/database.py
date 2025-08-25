from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

def init_db(app):
    """Inicializacion de la app"""
    db.init_app(app)
    ma.init_app(app)
    create_tables(app)


def create_tables(app):
    """Crea las tablas de la bd"""
    with app.app_context():
        db.create_all()


def close_session(exception=None):
    """Cierra la conexion con la bd cuando se termina un request"""
    db.session.remove()


def reset_db():
    print("Eliminando la BD")
    db.drop_all()
    print("Creando la BD")
    db.create_all()
    print("Listo!")
