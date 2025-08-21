#Dada una frase donde las palabras pueden estar repetidas e indistintamente en mayúsculas y
#minúsculas, imprimir una lista con todas las palabras sin repetir y en letra minúscula.
import re

frase = """
Si trabajás mucho CON computadoras, eventualmente encontrarás que te gustaría
automatizar alguna tarea. Por ejemplo, podrías desear realizar una búsqueda y
reemplazo en un gran número DE archivos de texto, o renombrar y reorganizar
un montón de archivos con fotos de una manera compleja. Tal vez quieras
escribir alguna pequeña base de datos personalizada, o una aplicación
especializada con interfaz gráfica, o UN juego simple.
"""

palabras = sorted(set(re.findall(r'\w+', frase.lower())))

print("Listado de palabras:")
print(*palabras, sep="\n")

#*palabras_sin_repetir → desempaqueta la lista.
#sep="\n" → separa cada elemento con un salto de línea.
 

