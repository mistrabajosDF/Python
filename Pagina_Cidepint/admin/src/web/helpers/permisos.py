from functools import wraps
from flask import abort, session, request
from src.core.rol_y_permiso import obtener_lista_permisos, es_superadmin, obtener_permisos, obtener_rol_del_usuario_en_institucion


def permisos_configuracion():
    """Función que retorna un booleano dependiendo si el usuario tiene o no los permisos necesarios"""
    #obtener email
    email= session.get('user')
    if email == None:
        return False
    if es_superadmin(email):
        return True
    else:
        return False

def requiere_permisos_superadmin(f):
    """Decorador, indica que la funcionalidad requiere los permisos del super administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (permisos_configuracion()) == False:
            print("no se dispone del permiso requerido")
            print("decorador= configuracion")
            return abort(401)
        return f(*args, **kwargs)
    return decorated_function


def permisos_servicios():
    """Función que retorna un valor dependiendo si el usuario tiene o no los permisos necesarios, respecto a servicios.
    Si el valor retornado es 0 = no tiene permisos
    Si el valor retornado es 1 = tiene los permisos menos borrar
    Si el valor retornado es 2 = tiene todos los permisos
    """
    #obtener email
    email= session.get('user')
    if email == None:
        return 0
    id_institucion = request.args.get('id_institucion', type=int)
    permisos_del_usuario= obtener_lista_permisos(email, id_institucion)
    todos_permisos_necesarios= ['serv_index', 'serv_show', 'serv_update', 'serv_create', 'serv_destroy']
    parcialmente_permisos_necesarios= ['serv_index', 'serv_show', 'serv_update', 'serv_create']
    if all(string in permisos_del_usuario for string in todos_permisos_necesarios):
        print("Resultado 2")
        return 2
    elif all(string in permisos_del_usuario for string in parcialmente_permisos_necesarios):
        print("Resultado 1")
        return 1
    else:
        print("Resultado 0")
        return 0


def requiere_todos_permisos_servicios(f):
    """Decorador, indica que la funcionalidad de servicios requiere todos los permisos"""
    @wraps(f)
    def funcion_servicios(*args, **kwargs):
        if (permisos_servicios() == 0) or (permisos_servicios() == 1):
            print("no se dispone del permiso requerido")
            print(permisos_servicios())
            print("decorador= todos servicios")
            return abort(401)
        return f(*args, **kwargs)
    return funcion_servicios

def requiere_parcialmente_permisos_servicios(f):
    """Decorador, indica que la funcionalidad de servicios requiere casi todos los permisos"""
    @wraps(f)
    def funcion_servicios2(*args, **kwargs):
        if (permisos_servicios() == 0):
            print("no se dispone del permiso requerido")
            print(permisos_servicios())
            print("decorador= parcial servicios")
            return abort(401)
        return f(*args, **kwargs)
    return funcion_servicios2

def permisos_solicitudes():
    """Función que retorna un valor dependiendo si el usuario tiene o no los permisos necesarios, respecto a solicitudes.
    Si el valor retornado es 0 = no tiene permisos
    Si el valor retornado es 1 = tiene los permisos menos borrar
    Si el valor retornado es 2 = tiene todos los permisos
    """
    #obtener email
    email= session.get('user')
    if email == None:
        return 0
    id_institucion = request.args.get('id_institucion', type=int)
    permisos_del_usuario= obtener_lista_permisos(email, id_institucion)
    todos_permisos_necesarios= ['req_index', 'req_show', 'req_update', 'req_destroy']
    parcialmente_permisos_necesarios= ['req_index', 'req_show', 'req_update']
    if all(string in permisos_del_usuario for string in todos_permisos_necesarios):
        print("Resultado 2")
        return 2
    elif all(string in permisos_del_usuario for string in parcialmente_permisos_necesarios):
        print("Resultado 1")
        return 1
    else:
        print("Resultado 0")
        return 0


def requiere_todos_permisos_solicitudes(f):
    """Decorador, indica que la funcionalidad de solicitudes requiere todos los permisos"""
    @wraps(f)
    def funcion_solicitudes1(*args, **kwargs):
        if (permisos_solicitudes() == 0) or (permisos_solicitudes() == 1):
            print("no se dispone del permiso requerido")
            print(permisos_solicitudes())
            print("decorador= todos solicitudes")
            return abort(401)
        return f(*args, **kwargs)
    return funcion_solicitudes1

def requiere_parcialmente_permisos_solicitudes(f):
    """Decorador, indica que la funcionalidad de solicitudes requiere casi todos los permisos"""
    @wraps(f)
    def funcion_solicitudes2(*args, **kwargs):
        if (permisos_solicitudes() == 0):
            print("no se dispone del permiso requerido")
            print(permisos_solicitudes())
            print("decorador= parcial solicitudes")
            return abort(401)
        return f(*args, **kwargs)
    return funcion_solicitudes2


def permisos_miembros():
    """Función que retorna un booleano dependiendo si el usuario y su rol tienen los permisos respecto a los miembros de la institucion
    """
    #obtener email
    email= session.get('user')
    if email == None:
        return False
    id_institucion = request.args.get('id_institucion', type=int)
    permisos_del_usuario= obtener_lista_permisos(email, id_institucion)
    todos_permisos_necesarios= ['admin_user_index', 'admin_user_create', 'admin_user_destroy', 'admin_user_update']
    if all(string in permisos_del_usuario for string in todos_permisos_necesarios):
        print("Resultado True")
        return True
    else:
        print("Resultado False")
        return False


def requiere_permisos_miembros(f):
    """Decorador, indica que la funcionalidad de miembros de la institucion requiere todos los permisos respectivos"""
    @wraps(f)
    def funcion_miembros(*args, **kwargs):
        if (permisos_miembros() == False) :
            print("no se dispone del permiso requerido")
            print(permisos_miembros())
            print("decorador= miembros institucion")
            return abort(401)
        return f(*args, **kwargs)
    return funcion_miembros