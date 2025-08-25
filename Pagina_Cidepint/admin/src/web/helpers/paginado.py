from src.core import configuracion


def paginar(pagina):
	"""Recibe la primera pagina y, de acuerdo al valor de configuracion, establece el limite superior e inferior de
	los elementos a mostrar """
	por_pagina = configuracion.item_per_page()
	inicio = int(por_pagina * (pagina - 1) + 1)
	fin = int(por_pagina * pagina)

	return inicio, fin