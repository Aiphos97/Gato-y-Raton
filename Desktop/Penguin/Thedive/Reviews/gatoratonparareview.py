import os
ubi_raton = (4,7)
ubi_gato = (4,0)
salidas = [(0,1),(7,1)]
tamaño_tablero = 8
max_turns = 30
turn_count = 0
turno_raton = True
print("Posiciones iniciales: \n Raton en", ubi_raton, "Gato en", ubi_gato, "Salidas en", salidas)
# creo una matriz abro parentesis de corchetes y dentro pongo un for para que se repita 8 veces
tablero = [["__" for _ in range(8)] for _ in range(8)]
profundidad = 8
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
# definí ubi gato y ubi raton como globales para que se puedan modificar dentro de la funcion
def actualizar_tablero():
    global ubi_gato, ubi_raton
    for i in range(tamaño_tablero):
        for j in range(tamaño_tablero):
            tablero[i][j] = "__"
    tablero[ubi_gato[0]][ubi_gato[1]] = "🐈"
    tablero[ubi_raton[0]][ubi_raton[1]] = "🐁"
    for s in salidas:
        tablero[s[0]][s[1]] = "🚪"
def imprimir_tablero():
    clear_console()  # limpia la consola para mejor visibilidad
    for row in tablero:
        print(" ".join(row))
        # join row para que se imprima sin los corchetes y comas
    print()
# revisa si es que el raton se escapo o el gato lo atrapo
def se_acabo(ubi_gato, ubi_raton, salidas):
    if ubi_gato == ubi_raton:
        return True, "gato"
    if ubi_raton in salidas:
        return True, "raton"
    return False, None
def evaluar_tablero(ubi_gato, ubi_raton, salidas):
    # condiciones minimax, el gato es negativo y el raton positivo
    if ubi_gato == ubi_raton:
        return -10000  # busca atrapar al raton
    elif ubi_raton in salidas:
        return 10000   # busca escapar
    # hay un for que recorre las salidas 
    # calcula la distancia manhattan entre x e y
    # resta y saca el valor absoluto entre ubi_raton y la salida s
    #     y despues halla la mas corta con min
    distancia_raton_salida = min(abs(ubi_raton[0]-s[0]) + abs(ubi_raton[1]-s[1]) for s in salidas)
    # Distancia del gato a raton, valor absoluto sin necesidad de for
    distancia_gato_raton = abs(ubi_gato[0]-ubi_raton[0]) + abs(ubi_gato[1]-ubi_raton[1])
    # heuristicos: 
    # el puntaje básico es 200 y se va restando , es peor que el 
    # gato atrape al raton, y va a preferir escapar del gato que salir por la puerta
    score = score = -(distancia_raton_salida * 20) + ( distancia_gato_raton * 10)
    return score
def mov_posi(ubi, tipo, ubi_gato, ubi_raton):
    x, y = ubi
    movimientos = []
    if tipo == "raton":
        direcciones = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    else:  # gato
        direcciones = [(1,0),(-1,0),(0,1),(0,-1)]
    # distancia del gato al raton 
    if tipo == "gato":
        distancia_gato_raton = abs(x - ubi_raton[0]) + abs(y - ubi_raton[1])
            # calcula distancia manhattan del gato al raton
    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        # suma los movimintos posibles a la ubicacion actual
        if 0 <= nx < tamaño_tablero and 0 <= ny < tamaño_tablero:
            # si es que el movimiento es dentro del tablero
            if tipo == "raton" and (nx, ny) != ubi_gato:
                movimientos.append((nx, ny))
                # si el raton no se mueve a la posicion del gato
            elif tipo == "gato":
                     movimientos.append((nx, ny))

    return movimientos
# tomo por parametros ubi gato y ubi raton la profundidad, si es el turno del raton y las salidas
def minimax(ubi_gato, ubi_raton, profundidad, es_turno_raton, salidas):
    fin, _ = se_acabo(ubi_gato, ubi_raton, salidas)
    if profundidad == 0 or fin:
        return evaluar_tablero(ubi_gato, ubi_raton, salidas)
# si es que se acabo el juego o si es que no hay mas jugadas va a evaluar tablero
    if es_turno_raton:
        max_eval = -float('inf')
        for mov in mov_posi(ubi_raton, "raton", ubi_gato, ubi_raton):
            # corrre todos los movimietos posibles del raton    
            eval = minimax(ubi_gato, mov, profundidad - 1, False, salidas)
            # va llamando recursivamente a si mismo hasta que no haya mas jugadas posibles
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for mov in mov_posi(ubi_gato, "gato", ubi_gato, ubi_raton):
            # simula que el gato se mueve a una posicion
            eval = minimax(mov, ubi_raton, profundidad - 1, True, salidas)
            # y evalua esa posicion
            min_eval = min(min_eval, eval)
            # retorna el valor mas pequeño, es decir el que mas conviene
        return min_eval
def mejor_movimiento_raton(ubi_gato, ubi_raton, salidas):
    best_score = -float('inf')
    best_move = None
    for mover in mov_posi(ubi_raton, "raton", ubi_gato, ubi_raton):
        score = minimax(ubi_gato, mover, profundidad, False, salidas)
        if best_move is None or score > best_score:
         best_score = score
         best_move = mover
    return best_move
def mejor_movimiento_gato(ubi_gato, ubi_raton, salidas):
    best_score = float('inf')
    best_move = None
    
    for nuevo_gato in mov_posi(ubi_gato, "gato", ubi_gato, ubi_raton):
        score = minimax(nuevo_gato, ubi_raton, profundidad, True, salidas)
        if score < best_score:
            best_score = score
            best_move = nuevo_gato
    return best_move

def mover_raton(ubi_raton, tablero):
    while True:
        mover = input("Ingresa tu movimiento (w/a/s/d q/e/z/c para diagonales, o 'p' para salir): ").strip().lower()
        if mover == 'p':
            return None  # Signal that the player wants to quit
        direcciones = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1),
                       'q': (-1, -1), 'e': (-1, 1), 'z': (1, -1), 'c': (1, 1)}
        if mover in direcciones:
            dx, dy = direcciones[mover]
            nueva_ubicacion = (ubi_raton[0] + dx, ubi_raton[1] + dy)
            if 0 <= nueva_ubicacion[0] < tamaño_tablero and 0 <= nueva_ubicacion[1] < tamaño_tablero:
                if tablero[nueva_ubicacion[0]][nueva_ubicacion[1]] in ["__", "🚪"]:
                    return nueva_ubicacion
        print("Movimiento inválido. Intenta de nuevo.")
def mover_gato(ubi_gato, tablero):
    while True:
        mover = input("Ingresa tu movimiento (w/a/s/d para mover, o 'p' para salir): ").strip().lower()
        if mover == 'p':
            return None  # Signal quit
        direcciones = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if mover in direcciones:
            dx, dy = direcciones[mover]
            nueva_ubicacion = (ubi_gato[0] + dx, ubi_gato[1] + dy)
            if 0 <= nueva_ubicacion[0] < tamaño_tablero and 0 <= nueva_ubicacion[1] < tamaño_tablero:
                if tablero[nueva_ubicacion[0]][nueva_ubicacion[1]] in ["__", "🐁"]:
                    return nueva_ubicacion
        print("Movimiento inválido. Intenta de nuevo.")
# --- Before the loop ---
actualizar_tablero()
imprimir_tablero()
rol = input('Elije que rol quieres jugar (Gato o Raton o nada para que jueguen solos): ').strip().lower()
jugando_gato = rol == "gato"
jugando_raton = rol == "raton"
# --- Main game loop ---
while turn_count < max_turns:
    # Check if game is over before any move
    fin, ganador = se_acabo(ubi_gato, ubi_raton, salidas)
    if fin:
        if ganador == "gato":
            print("El gato ha atrapado al ratón. ¡Fin del juego!")
        elif ganador == "raton":
            print("El ratón ha escapado. ¡Fin del juego!")
        break
    if turno_raton:
        if jugando_raton:
            ubi_raton = mover_raton(ubi_raton, tablero)
        else:
            ubi_raton = mejor_movimiento_raton(ubi_gato, ubi_raton, salidas)
            print("Mouse moves to", ubi_raton)
    else:
        if jugando_gato:
            ubi_gato = mover_gato(ubi_gato, tablero)
        else:
            ubi_gato = mejor_movimiento_gato(ubi_gato, ubi_raton, salidas)
            print("Cat moves to", ubi_gato)
    # Update board after both players have moved
    actualizar_tablero()
    imprimir_tablero()
    turno_raton = not turno_raton
    turn_count += 1
if turn_count == max_turns:
    print("El gato acorraló al ratón. ¡Fin del juego!")