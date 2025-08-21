"""
A partir del código:
[ ]: cadena = input("Ingresa la clave (debe tener menos de 10 caracteres y no contener los símbolos:@ y !):")
if len(cadena) > 10:
	print("Ingresaste más de 10 carcateres")
cant = 0
for car in cadena:
	if car == "@" or car == "!":
		cant = cant + 1
if cant >= 1:
	print("Ingresaste alguno de estos símbolos: @ o !" )
else:
	print("Ingreoso OK")

Que informa si los caracteres “@” o “!” formaban parte de una palabra ingresada, simplifiquelo
"""

cadena = input("Ingresa la clave (debe tener menos de 10 caracteres y no contener los símbolos:@ y !):")
if len(cadena) > 10:
	print("Ingresaste más de 10 carcateres")
elif any(car in "@!" for car in cadena):
    print("Ingresaste alguno de estos símbolos: @ o !")
else:
    print("Ingreso OK")
		


	
