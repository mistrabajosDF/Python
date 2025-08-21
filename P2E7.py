"""
• generar una estructura con los nombres de los estudiantes y la suma de ambas notas.
• Calcular el promedio de las notas totales e informar quiénes obtuvieron menos que el promedio.
"""

nombres1 = """
 'Agustin',
 'Alan',
 'Andrés',
 'Ariadna',
 'Bautista',
 'CAROLINA',
 'CESAR',
 'David',
 'Diego',
 'Dolores',
 'DYLAN',
 'ELIANA',
 'Emanuel',
 'Fabián',
 'Facundo',
 'Facundo',
 'FEDERICO',
 'FEDERICO',
 'GONZALO',
 'Gregorio',
 'Ignacio',
 'Jonathan',
 'Jonathan',
 'Jorge',
 'JOSE',
 'JUAN',
 'Juan',
 'Juan',
 'Julian',
 'Julieta',
 'LAUTARO',
 'Leonel',
 'LUIS',
 'Luis',
 'Marcos',
 'María',
 'MATEO',
 'Matias',
 'Nicolás',
 'NICOLÁS',
 'Noelia',
 'Pablo',
 'Priscila',
 'TOMAS',
 'Tomás',
 'Ulises',
 'Yanina'
"""

num1 = """
81,
 60,
 72,
 24,
 15,
 91,
 12,
 70,
 29,
 42,
 16,
 3,
 35,
 67,
 10,
 57,
 11,
 69,
 12,
 77,
 13,
 86,
 48,
 65,
 51,
 41,
 87,
 43,
 10,
 87,
 91,
 15,
 44,
 85,
 73,
 37,
 42,
 95,
 18,
 7,
 74,
 60,
 9,
 65,
 93,
 63,
 74
 """

num2 = """
 30,
 95,
 28,
 84,
 84,
 43,
 66,
 51,
 4,
 11,
 58,
 10,
 13,
 34,
 96,
 71,
 86,
 37,
 64,
 13,
 8,
 87,
 14,
 14,
 49,
 27,
 55,
 69,
 77,
 59,
 57,
 40,
 96,
 24,
 30,
 73,
 95,
 19,
 47,
 15,
 31,
 39,
 15,
 74,
 33,
 57,
 10
 """

# Le asigno el formato para que queden prolijos los campos
formato = "{:} {:16} {:10}"
formato2 = "{:10} {:10}"
formato3 = "{:>40}"
formato4 = "{:>30}"

nombres1 = nombres1.replace(",","").replace("'","").split()
num1 = num1.replace(",","").split()
num2 = num2.replace(",","").split()

lista=[]
for i in range(len(nombres1)):
    lista.append((nombres1[i].title(), (int(num1[i]) + int(num2[i]))))

promedio = sum(suma for _, suma in lista) / (len(nombres1))
#_ significa que no interesa el primer elemento de la tupla (el nombre), toma el segundo

print("-----------------------------------------------")
print(formato3.format(f"El promedio de las suma de las notas es: {promedio}"))
print("-----------------------------------------------")
print ("Los alumnos con suma de notas por debajo del promedio son: ")
print("-----------------------------------------------")
print(formato.format('', 'Nombre', 'Suma'))
print("-----------------------------------------------")

print(*(formato2.format(nombre, suma) for nombre, suma in lista if suma < promedio), sep="\n")
