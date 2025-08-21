# Solicite por teclado una palabra y calcule su valor según la tabla de valores del Scrabble
	
valores = {
	#** inserta en un diccionario los pares clave-valor de otro diccionario.
    **dict.fromkeys('AEIOULNRST', 1), #hace: {'A': 1, 'E': 1, 'I': 1, 'O': 1, 'U': 1}
    **dict.fromkeys('DG', 2),
    **dict.fromkeys('BCMP', 3),
    **dict.fromkeys('FHVWY', 4),
    'K': 5,
    **dict.fromkeys('JX', 8),
    **dict.fromkeys('QZ', 10)
}

palabra = input("Ingresa la palabra a calcular valor: ").upper()

print(f"La palabra '{palabra}' tiene un valor de {sum(valores.get(c, 0) for c in palabra)}")
