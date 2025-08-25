import re
from flask import flash

def coordenadas(cadena):
	"""Devuele true si el string recibido tiene el formato de coordenada"""
	coordenadas = re.compile('^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$')
	return not ((coordenadas.match(cadena)) is None)


def validadorCaracteres(cadena):
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


def no_vacio_ni_100(cadena):
	"""Devuele true si un valor recibido no es vacío ni de long mayor a 50"""
	if cadena != "":
		if len(cadena) <= 100:
			return True
		else:
			message = "Ups, {} es demasiado largo, intenta escribiendo algo mas corto.".format(cadena)
			flash(message, "error")
		return False


def no_vacio_ni_50(cadena):
	"""Devuele true si un valor recibido no es vacío ni de long mayor a 50"""
	if cadena != "":
		if len(cadena) <= 50:
			return True
		else:
			message = "Ups, {} es demasiado largo, intenta escribiendo algo mas corto.".format(cadena)
			flash(message, "error")
		return False


def solo_letras(cadena):
	"""Retorna true si la cadena solo contiene letras"""
	if cadena.replace(" ", "").isalpha():
		return True
	else:
		flash("Ups, tu nombre y apellido solo pueden contener letras y espacios.", "error")
		return False


def solo_numeros(cadena):
	"""Retorna true si la cadena solo contiene numeros mayores a 0"""
	if cadena.isdigit() and int(cadena) > 0:
		return True
	else:
		message = "Ups, {} no es un valor valido, debe ser un número mayor a 0.".format(cadena)
		flash(message, "error")
		return False


def no_vacio_ni_250(cadena):
	"""Devuele true si un valor recibido no es vacío ni de long mayor a 250"""
	if cadena != "":
		if len(cadena) <= 250:
			return True
		else:
			message = "Ups, {} es demasiado largo, intenta escribiendo algo mas corto.".format(cadena)
			flash(message, "error")
		return False