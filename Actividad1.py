# Variables con los datos

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
   

def option_1():

    ''' Funcion que se encarga de ejecutar la opcion 1 del menu '''


    def prome(lista):   

        ''' Devuelve el promedio total de las notas '''

        cont = 0
        suma = 0
        for elem in lista:
            suma += elem[3]
            cont += 1
        suma = suma / cont
        return suma 


    def sumatot(lista):

        ''' Devuelve la suma de todas las notas '''
    
        nota = 0
        for elem in lista:
            nota += elem[3]
        return nota


    # Nombre de los campos principales
    print("-----------------------------------------------")
    print(formato.format('','Nombre', 'Eval1', 'Eval2', 'Suma'))
    print("-----------------------------------------------")



    # Imprimo cada tupla de la lista
    for elem in lista:
        print(formato2.format(elem[0], elem[1], elem[2], elem[3]))



    #imprimo la suma total y el promedio debajo del diccionario de alumnos.
    print(" ")
    print(format("----------------------------------",">40"))
    print(formato4.format(f" Suma Total: {sumatot(lista)} "))
    print(format("----------------------------------",">40"))
    print(formato3.format(f" Promedio: {prome(lista)} "))
    print(format("----------------------------------",">40"))



def option_2():

    ''' Funcion que se encarga de ejecutar la opcion 2 del menu '''

    def report_values(index):

        ''' Reporta los valores en un rango determinado de la categoria ingresada '''

        lower_end = int(input('Ingrese el extremo inferior del rango de valores a informar(0 minimo) \n'))
        top_end = int(input(f'Ingrese el extremo superior del rango de valores a informar({len(nombres1) - 1} maximo) \n'))

        print("-----------------------------------------------")
        print(f'Valores en un rango de {lower_end} a {top_end}')

        # Se recorre la lista y se imprimen los valores dentro del rango
        for elem in lista:
            if ((elem[index] > lower_end) and (elem[index] < top_end)):
                print(formato2.format(elem[0], elem[1], elem[2], elem[3]))

    print('Seleccione sobre que valor se realizara el reporte: ')
    print('Para realizar reporte de la evaluacion 1, ingrese 1.')
    print('Para realizar reporte de la evaluacion 2, ingrese 2.')
    print('Para realizar reporte de la suma de las evaluaciones, ingrese 3.')
    print('Para salir, ingrese 0.')
    option = int(input('¿Que opcion elige? \n'))
    print('===================================================')

    while (option != 0):

        if (option >= 1) and (option <= 3):
            report_values(option)
            print("-----------------------------------------------")
            option = int(input('Si quiere realizar otro reporte de algun valor ingrese el numero correspondiente, si quiere salir, ingrese 0: \n'))
        else:
            print("-----------------------------------------------")
            option = int(input('El numero ingresado no es correcto. Por favor, ingrese un valor entre 1 y 3 inclusive. \n'))


def option_3():

	''' Funcion que se encarga de ejecutar la opcion 3 del menu '''


	def ord_nombre():

		""" Retorna los alumnos ordenados por nombre """

		return sorted(lista, key = lambda nombre: nombre[0])


	def ord_eval1():

		""" Retorna los alumnos ordenados por la nota en la evaluacion 1 """

		return sorted(lista, key = lambda eval1: eval1[1])


	def ord_eval2():

		""" Retorna los alumnos ordenados por por la nota en la evaluacion 2 """

		return sorted(lista, key = lambda eval2: eval2[2])


	def ord_suma():

		""" Retorna los alumnos ordenados por la suma de las notas en ambas evaluaciones """

		return sorted(lista, key = lambda suma: suma[3])
    

	print('Para ordenar los datos por nombre, ingrese 1.')
	print('Para ordenar los datos por nota en evaluacion 1, ingrese 2.')
	print('Para ordenar los datos por nota en evaluacion 2, ingrese 3.')
	print('Para ordenar los datos por la suma de las notas en ambas evaluaciones, ingrese 4.')
	print('Para salir, ingrese 0.')
	opcion = int(input('¿Que opcion elige? \n'))
	print('===================================================')

	while (opcion != 0):

		if (opcion > 0) and (opcion < 5):

			if (opcion == 1):
				print('Imprimiendo por nombre: ')
				aux = (ord_nombre())
			elif (opcion == 2):
				print('Imprimiendo por evaluacion 1:')
				aux = (ord_eval1())
			elif (opcion == 3):
				print('Imprimiendo por evaluacion 2:')
				aux = (ord_eval2())
			elif (opcion == 4):
				print('Imprimiendo por la suma de las notas en ambas evaluaciones:')
				aux = (ord_suma())

			# Impresión
			print("-----------------------------------------------")
			print(formato.format('', 'Nombre', 'Eval1', 'Eval2', 'Suma'))
			print("-----------------------------------------------")
			for i in range(len(aux)):
				print(formato2.format(aux[i][0], aux[i][1], aux[i][2], aux[i][3]))
			print("-----------------------------------------------")

			opcion = int(input('Si quiere imprimir por otro orden ingrese el numero correspondiente, si quiere salir, ingrese 0: \n'))

		else:
			print("-----------------------------------------------")
			opcion = int(input('El numero ingresado no es correcto. Por favor, ingrese un valor entre 1 y 4 inclusive. \n'))



#  -- Main --


nombres1 = nombres1.title().replace(",","").replace("'","").split()
num1 = num1.replace(",","").split()
num2 = num2.replace(",","").split()


# Carga de los datos en la lista  
lista = [(nombres1[i], int(num1[i]), int(num2[i]), (int(num1[i]) + int(num2[i]))) for i in range(len(nombres1))]


# Formato para que queden prolijos los campos
formato = "{:} {:16} {:10} {:10} {:10}"
formato2 = "{:10} {:10} {:10} {:10}"
formato3 = "{:>40}"
formato4 = "{:>30}"


# Menu
while True:
    print(' ')
    print('===================================================')
    print('MENU DE OPCIONES')
    print('Opcion 1 --> Calcular el promedio y la suma total de las notas finales de los estudiantes')
    print('Opcion 2 --> Realizar un reporte de los datos de una categoria entre un rango seleccionado')
    print('Opcion 3 --> Ordenar los datos de acuerdo a distintos criterios seleccionados')
    number = int(input('Ingrese un numero de opcion (0 para terminar) \n'))
    print('===================================================')
    print(' ')

    if (number == 0):
        print('Finalizado.')
        break
    elif (number == 1):
        option_1()
    elif (number == 2):
        option_2()
    elif (number == 3):
        option_3()
    else:
        print('Opcion invalida - Intente de nuevo')