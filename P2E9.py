#Solicite un string y determine si es un Heterograma (palabra o frase que no tiene ninguna letra repetida).
		
palabra = input("Ingresa la palabra a verificar si es un heterograma: ").lower()

letras = [c for c in palabra if c.isalpha()]

print(f"La palabra/frase '{palabra}' {'' if len(letras) == len(set(letras)) else 'no'} es un heterograma")
