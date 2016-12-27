# coding=utf-8
import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square

myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")



def move_to_min(sq):
    global game_map
    minimo = 1000
    sqrr = None
    distancia = 1

    if sq.strength < 10:           # El cuadrado está vacío o es demasiado pequeño
        return(Move(sq, STILL))

    radio = int(min((game_map.width, game_map.height)) / 4)

    while minimo == 1000 and distancia < radio :
        vecinos = game_map.neighbors(sq, distancia)
        for sqv in vecinos:
            if sqv.owner != myID:
                if sqv.strength < minimo:
                    minimo = sqv.strength
                    sqrr = sqv
        distancia += 1

    if minimo == 1000 :  # cuadrado demasiado grande, hacemos crecer el centro hacia el vecino más pequeño
        vecinos = game_map.neighbors(sq,3)
        for sqv in vecinos:
            if sqv.strength < minimo:
                minimo = sqv.strength
                sqrr = sqv

    if sqrr.x < sq.x:
        return(Move(sq,WEST))
    if sqrr.x > sq.x:
        return(Move(sq,EAST))
    if sqrr.y < sq.y:
        return(Move(sq,NORTH))
    if sqrr.y > sq.y:
        return(Move(sq,SOUTH))




while True:
    game_map.get_frame()
    moves = []
    for square in game_map:
        if square.owner == myID:
            minimo = 1000
            vecino_valido = False
            sqrr = None
            vecinos = game_map.neighbors(square, 1)
            for sqv in vecinos:
                if sqv.owner != myID:
                    vecino_valido = True
                    if sqv.strength < minimo and sqv.strength <= square.strength:
                        minimo = sqv.strength
                        sqrr = sqv
            if vecino_valido and minimo == 1000:
                moves.append(Move(square, STILL))
            elif vecino_valido and minimo != 1000:
                if sqrr.x < square.x:
                    moves.append(Move(square, WEST))
                if sqrr.x > square.x:
                    moves.append(Move(square, EAST))
                if sqrr.y < square.y:
                    moves.append(Move(square, NORTH))
                if sqrr.y > square.y:
                    moves.append(Move(square, SOUTH))
            else:
                moves.append(move_to_min(square))
    hlt.send_frame(moves)
