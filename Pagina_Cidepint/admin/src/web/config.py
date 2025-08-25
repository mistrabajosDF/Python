from os import environ
import secrets


class Config (object):
    """Configuracion base"""

    SECRET_KEY = secrets.token_hex(32)
    TESTING = False
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False

    #Aca van los datos de auth google, no deja pushear con esto


    # Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    #MAIL_USERNAME = No deja subir con esto
    #MAIL_PASSWORD = No deja subir con esto


class ProductionConfig(Config):
    """Configuracion de produccion"""
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")


class DevelopmentConfig(Config):
    """Configuracion de desarrollo"""

    DB_USER = "postgres"
    #DB_PASS = "admin"
    DB_PASS = "postgres"
    DB_HOST = "localhost"
    #DB_NAME = "grupo22_pruebaPr"
    DB_NAME = "grupo22"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")


class TestingConfig(Config):
    """Configuracion de testing"""
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "test": TestingConfig,
}
