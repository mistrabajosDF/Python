from flask import session, abort
from functools import wraps

def user_is_login():
    """Función que retorna una sesión, o None si no existe"""
    return session.get('user') is not None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (session.get("user")) == None:
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function

