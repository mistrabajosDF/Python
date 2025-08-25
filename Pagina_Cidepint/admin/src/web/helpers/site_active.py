from flask import session, abort
from functools import wraps
from src.core import configuracion
from flask import abort


def site_is_active():
	"""Retorna si true si el sitio esta activo, o false si esta en modo mantenimiento"""
	return not(configuracion.get_configuration().mantenimiento_modo)


def site_active(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if (configuracion.get_configuration().mantenimiento_modo):
			return abort(503)
		return f(*args, **kwargs)
	return decorated_function
