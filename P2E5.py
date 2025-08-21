#Dada una frase y un string ingresados por teclado, genere una lista de palabras,
#y sobre ella, informe la cantidad de palabras en las que se encuentra el string.
import re

frase = input("Ingresa una frase: ")
busqueda = input("Ingresa un string: ").lower()

#Toma palabras, no signos de puntuacion
lista_palabras = re.findall(r'\w+', frase.lower())

cantidad = sum(1 for palabra in lista_palabras if busqueda in palabra)

print(f'Cantidad de veces que aparece la palabra "{busqueda}" es: {cantidad}')
