
import sys 
N=8
ubi_raton = (3, 7)  
ubi_gato = (4, 0)   
agujeros = [(0,1), (7,1)] 

print("Python version:", sys.version)
print("Starting positions:", "Mouse", ubi_raton, "Cat", ubi_gato)
print("Holes:", agujeros)
tablero = [["__" for _ in range(N)] for _ in range(N)]


def actualizar_tablero():
    # Reset all cells to empty
    for i in range(N):
        for j in range(N):
            tablero[i][j] = "__"
    
    # Place cat
    tablero[ubi_gato[0]][ubi_gato[1]] = "🐈"
    
    # Place mouse
    tablero[ubi_raton[0]][ubi_raton[1]] = "🐁"
    
    # Place holes
    for h in agujeros:
        tablero[h[0]][h[1]] = "🌀"


def imprimir_tablero():
    for row in tablero:
        print(row)
    print()

def se_acabo(ubi_gato, ubi_raton, agujeros):
    if ubi_gato == ubi_raton:
        return True, "Gato"
    elif ubi_raton in agujeros:
        return True, "Raton"
    return False, None

def evaluar_tablero(ubi_gato,ubi_raton,agujeros):
    if ubi_gato==ubi_raton:
        return -1000
    elif ubi_raton in agujeros:
        return 1000
    else:
        distancia_raton_agujero = min(abs(ubi_raton[0]-a[0]) + abs(ubi_raton[1]-a[1]) for a in agujeros)
        distancia_gato_raton = abs(ubi_gato[0]-ubi_raton[0]) + abs(ubi_gato[1]-ubi_raton[1])
        score = 100 - distancia_raton_agujero*5 - max(0,5 - distancia_gato_raton)*10
        return score


def mov_posi(ubi, tablero, tipo):
    x, y = ubi
    moves = []

    if tipo == "raton":
        direcciones = [(-1,0),(1,0),(0,-1),(0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    else:
        direcciones = [(-1,0),(1,0),(0,-1),(0,1)]

    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8:
            if tipo == "raton" and tablero[nx][ny] in ["__", "🌀"]:  # allow holes
                moves.append((nx, ny))
            elif tipo == "gato" and tablero[nx][ny] in ["__","🐁"]:  # allow cat to capture mouse
                moves.append((nx, ny))
    return moves


def minimax(ubi_gato, ubi_raton, agujeros, tablero, is_maximizing, depth=2, max_depth=2):
    fin, ganador = se_acabo(ubi_gato, ubi_raton, agujeros)
    if fin or depth == max_depth:
        return evaluar_tablero(ubi_gato, ubi_raton, agujeros)

    if is_maximizing:  # Mouse
        best_score = -float('inf')
        for move in mov_posi(ubi_raton, tablero, "raton"):
            old_pos = ubi_raton
            ubi_raton = move
            
            score = minimax(ubi_gato, ubi_raton, agujeros, tablero, False, depth+1)
            best_score = max(best_score, score)
            
            ubi_raton = old_pos  # backtrack
        return best_score
    else:  # Cat
        best_score = float('inf')
        for move in mov_posi(ubi_gato, tablero, "gato"):
            old_pos = ubi_gato
            ubi_gato = move
            
            score = minimax(ubi_gato, ubi_raton, agujeros, tablero, True, depth+1)
            best_score = min(best_score, score)
            
            ubi_gato = old_pos  # backtrack
        return best_score

def mejor_movimiento_raton(ubi_gato, ubi_raton, agujeros, tablero):
    best_score = -float('inf')
    best_move = None
    for mover in mov_posi(ubi_raton, tablero, "raton"):
        old_pos = ubi_raton
        ubi_raton = mover
        score = minimax(ubi_gato, ubi_raton, agujeros, tablero, False)
        if score > best_score:
            best_score = score
            best_move = mover
        ubi_raton = old_pos  # backtrack
    return best_move

def mejor_movimiento_gato(ubi_gato, ubi_raton, agujeros, tablero):
    best_score = float('inf')
    best_move = None
    for mover in mov_posi(ubi_gato, tablero, "gato"):
        old_pos = ubi_gato
        ubi_gato = mover
        score = minimax(ubi_gato, ubi_raton, agujeros, tablero, True)  # next is mouse's turn
        if score < best_score:
            best_score = score
            best_move = mover
        ubi_gato = old_pos  # backtrack
    return best_move



# Initialize the board
actualizar_tablero()
imprimir_tablero()

rol=input('Elije que rol quieres jugar (Gato o Raton o nada para que jueguen solos)').strip().lower()
jugando_gato = rol == "gato"
jugando_raton = rol == "raton"

def mover_raton(ubi_raton, tablero, agujeros):
    while True:
        mover = input("Ingresa tu movimiento (w/a/s/d q/e/z/c para diagonales para mover, o 'p' para salir): ").strip().lower()
        if mover == 'p':
            print("Saliendo del juego.")
            sys.exit()
        direcciones = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1),
                       'q': (-1, -1), 'e': (-1, 1), 'z': (1, -1), 'c': (1, 1)}
        if mover in direcciones:
            dx, dy = direcciones[mover]
            nueva_ubicacion = (ubi_raton[0] + dx, ubi_raton[1] + dy)

            if 0 <= nueva_ubicacion[0] < N and 0 <= nueva_ubicacion[1] < N :
                if tablero[nueva_ubicacion[0]][nueva_ubicacion[1]] in ["__", "🌀"]:
                    if nueva_ubicacion in agujeros:
                        print("¡Has encontrado un agujero! ¡Raton gana!")
                        sys.exit()
                return nueva_ubicacion   # ✅ return new position
            else:
                print("Movimiento inválido. Intenta de nuevo.")

def mover_gato(ubi_gato, tablero):
    while True: 
        mover_gato = input("Ingresa tu movimiento (w/a/s/d para mover, o 'p' para salir): ").strip().lower()
        if mover_gato == 'p':
            print("Saliendo del juego.")
            sys.exit()
        direcciones = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if mover_gato in direcciones:
            dx, dy = direcciones[mover_gato]
            nueva_ubicacion = (ubi_gato[0] + dx, ubi_gato[1] + dy)
            if 0 <= nueva_ubicacion[0] < N and 0 <= nueva_ubicacion[1] < N :
                if tablero[nueva_ubicacion[0]][nueva_ubicacion[1]] in ["__", "🐁"]:
                    if nueva_ubicacion == ubi_raton:
                        print("¡Gato ha atrapado al ratón! ¡Gato gana!")
                        sys.exit()
                return nueva_ubicacion   # ✅ return new position
            else:
             print("Movimiento inválido. Intenta de nuevo.")

# Main loop with limited moves
max_turns = 50  # limit total moves
turn_count = 0
turno_raton = True

while turn_count < max_turns:
    fin, ganador = se_acabo(ubi_gato, ubi_raton, agujeros)
    if fin:
        print("Game over! Winner:", ganador)
        break

    if turno_raton:
        if jugando_raton:
            ubi_raton = mover_raton(ubi_raton, tablero, agujeros)
        else:
            ubi_raton = mejor_movimiento_raton(ubi_gato, ubi_raton, agujeros, tablero)
            print("Mouse moves to", ubi_raton)
    else:
        if jugando_gato:
            ubi_gato = mover_gato(ubi_gato, tablero)
        else:
            ubi_gato = mejor_movimiento_gato(ubi_gato, ubi_raton, agujeros, tablero)
            print("Cat moves to", ubi_gato)

    actualizar_tablero()
    imprimir_tablero()

    turno_raton = not turno_raton
    turn_count += 1

  
if turn_count == max_turns:
    print("Game ended due to move limit. No winner.")
