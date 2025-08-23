def minas_vecinas(tablero):
    """
    Dado un tablero de Buscaminas con '*' representando minas y '-' celdas vacías,
    devuelve un nuevo tablero donde cada celda vacía contiene la cantidad de minas
    que la rodean.
    
    Parámetros:
    tablero (list de str): Lista de strings que representan el tablero.
    
    Retorna:
    list de str: Nuevo tablero con números en las celdas vacías.
    """
    filas = len(tablero)
    cols = len(tablero[0])
    resultado = []

    for i in range(filas):
        fila_nueva = ''
        for j in range(cols):
            if tablero[i][j] == '*':
                fila_nueva += '*'
            else:
                # Contar minas alrededor
                contador = 0
                for x in range(max(0, i-1), min(filas, i+2)):
                    for y in range(max(0, j-1), min(cols, j+2)):
                        if tablero[x][y] == '*':
                            contador += 1
                fila_nueva += str(contador)
        resultado.append(fila_nueva)
    
    return resultado

# Ejemplo de uso
tablero_inicial = [
    '-*-*-',
    '--*--',
    '----*',
    '*----',
]

tablero_resultado = minas_vecinas(tablero_inicial)
for fila in tablero_resultado:
    print(fila)
