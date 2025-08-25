from flask import render_template
from src.core import configuracion


def not_found_error(e):
    kwargs = {
        'eror_name': '404 Not Found Error',
        'error_description': 'La página que estás buscando no existe.'
    }
    return render_template('error.html', **kwargs), 404

def unauthorized(e):
    kwargs = {
        'eror_name': '401 Unauthorized',
        'error_description': 'Ups, no iniciaste sesión o no tenés permiso para esta acción.'
    }
    return render_template('error_401.html', **kwargs), 401

def service_unavailable(e):
    kwargs = {
        'eror_name': '503 Service Unavailable',
        'mensaje': configuracion.get_configuration().mantenimiento_mensaje,
        'contacto': configuracion.get_configuration().info_contacto,
    }
    return render_template('error_503.html', **kwargs), 503


def method_not_allowed(e):
    kwargs = {
        'eror_name': '405 Method not allowed',
        'error_description': 'Ups, parece que intentaste hacer o ingresar a algo no habilitado.'
    }
    return render_template('error_405.html', **kwargs), 401