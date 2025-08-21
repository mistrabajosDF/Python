#Dado un texto solicite por teclado una letra e imprima las palabras que comienzan con dicha
#letra. En caso que no se haya inrgesado un letra, indique el error. Ver: módulo string

import string

lista_palabras = "los las gato perro loro canario los gatos".lower().split()

letra = input("Ingresa la letra para buscar palabras que empiecen con esta: ").lower()
if len(letra) != 1: exit("Debe ingresar exactamente una letra.")

coincidencias = [p for p in lista_palabras if p.startswith(letra)]
print("\n".join(f'Palabra que comienza con {letra}: {p}' for p in coincidencias) 
      or f"No se encontró ninguna palabra que empiece con '{letra}'.")

