# las imágenes(OPCIONAL en formato imagen, sino la url - "image_url") de los 10 juegos
# más votados(num_votes). (Posicion 12)
import csv

archivo= open("bgg_db_1806.csv", "r", encoding="utf8")
csvreader=csv.reader (archivo, delimiter=',')

encabezado=next(csvreader)
print (encabezado)

lista=[]
for juego in csvreader:
	lista.append(juego[12])

lista.sort(reverse=True)
print(lista)

archivo.close()
archivo= open("bgg_db_1806.csv", "r", encoding="utf8")
csvreader=csv.reader (archivo, delimiter=',')

cont=0
for i in range(10):
	for juego in csvreader:
		if lista[i]==juego[12] and cont<10:
			print (juego[3], juego[12])
			cont=cont+1
	archivo.close()
	archivo = open("bgg_db_1806.csv", "r", encoding="utf8")
	csvreader = csv.reader(archivo, delimiter=',')

archivo.close()






