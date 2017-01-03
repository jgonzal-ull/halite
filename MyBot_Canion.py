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

rotando4 = 0
rotando2 = 0
rotando3 = 0

umbral = 10
umbralsuperior = 100

while True:
    game_map.get_frame()
    moves = []
    for square in game_map:
        if square.owner == myID:
            if square.strength <= umbral:
                moves.append(Move(square, STILL))
            elif square.strength >= umbralsuperior:
                moves.append(Move(square, WEST))
            elif square.x == centro_x and square.y == centro_y:
                if rotando3 == 0:
                    moves.append(Move(square, WEST))
                elif rotando3 == 1:
                    moves.append(Move(square, EAST))
                elif rotando3 == 2:
                    moves.append(Move(square, SOUTH))
                rotando3 = (rotando3 + 1) % 3
            else:
                moves.append(Move(square, SOUTH))
    hlt.send_frame(moves)
