#listar los nombres de juegos que se jueguen con menos de 3 jugadores y seanjuegos de cartas("Card Game" en
#el campo "category").

import csv

archivo= open("bgg_db_1806.csv", "r", encoding="utf8")
csvreader=csv.reader (archivo, delimiter=',')

encabezado=next(csvreader)
#print (encabezado)

print ('-----------------------------------------------------')
print ('Juegos con menos de 3 jugadores como maximo que sean de cartas: ')
print ('-----------------------------------------------------')
for juego in csvreader:
	if "Card Game" in juego[17] and juego[5]<'3':
		print (f"{juego[3]}")

archivo.close()
