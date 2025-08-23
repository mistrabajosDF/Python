import pickle
import json

archivo = open("bandas.dat", "wb")
datos = [
	{"nombre": "William Campbell", "ciudad": "La Plata", "ref": "https://www.instagram.com/williamcampbellok"},
	{"nombre": "Buendia", "ciudad": "La Plata", "ref":"https://buendia.bandcamp.com/"},
	{"nombre": "Lúmine", "ciudad": "La Plata", "ref": "https://www.instagram.com/luminelp/"}]
pickle.dump(datos, archivo)
archivo.close()


archivo = open("bandas.dat", "rb")
datos = pickle.load(archivo)

lista_datos_json=[]

for item in datos:	#Imprime los 3
	for item, valor in item.items():
		print(f"{item}: {valor}") #Cada item con su valor
		lista_datos_json.append({f"{item}: {valor}"})
	print("-"*30)
	
archivo.close()

print(lista_datos_json)

archivo_j=open ("bandas.json", "w")
json.dump(datos, archivo_j)
archivo_j.close()




