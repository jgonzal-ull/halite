import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square

centro_x = -1
centro_y = -1

myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBotCanion")

# Primera vez, averiguamos dónde está centrado nuestro objeto
game_map.get_frame()
moves = []
for square in game_map:
    if square.owner == myID:
        centro_x = square.x
        centro_y = square.y
        moves.append(Move(square, STILL))
hlt.send_frame(moves)

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
                moves.append(Move(square, STILL))
    hlt.send_frame(moves)
