import random
import sys
from math import floor


HEIGHT, WIDTH = 600,600
T_HEIGHT, T_WIDTH = HEIGHT//4, WIDTH//4
T_DIM = 4

tiles = [[0,0,0,0],  # Holds values of tiles on the board
         [0,0,0,0],
         [0,0,0,0],
         [0,0,0,0]]

score = 0


####################################################
#                   Summation                      #
####################################################
def mergetiles(score):
    for x in range(T_DIM):
        for y in range(T_DIM-1):
            if tiles[x][y] == tiles[x][y+1] and tiles[x][y] != 0:
                tiles[x][y] = tiles[x][y]*2
                tiles[x][y+1] = 0 
                score += tiles[x][y]
                moveTiles()
    return score

####################################################
#                   Move Tiles                     #
####################################################
def moveTiles():
    for x in range(0,T_DIM):
        for y in range(0,T_DIM-1):
            while tiles[x][y] == 0 and sum(tiles[x][y:]) > 0:
                for z in range(y,T_DIM-1):
                   tiles[x][z] = tiles[x][z+1]
                tiles[x][T_DIM-1] = 0


####################################################
#                 Rotate Matrix                    #
####################################################
def rotate():
    for x in range(0,int(T_DIM/2)):
        for y in range(x,T_DIM-x-1):
            temp1 = tiles[x][y]
            temp2 = tiles[T_DIM-1-y][x]
            temp3 = tiles[T_DIM-1-x][T_DIM-1-y]
            temp4 = tiles[y][T_DIM-1-x]

            tiles[T_DIM-1-y][x] = temp1
            tiles[T_DIM-1-x][T_DIM-1-y] = temp2
            tiles[y][T_DIM-1-x] = temp3
            tiles[x][y] = temp4


####################################################
#                  Evaluate Move                   #
####################################################
def checkIfCanGo():
    for x in range(T_DIM**2): 
        if tiles[floor(x/T_DIM)][x%T_DIM] == 0:
            return True
    
    for x in range(T_DIM):
        for y in range(T_DIM-1):
            if tiles[x][y] == tiles[x][y+1]:
                return True
            elif tiles[y][x] == tiles[y+1][x]:
                return True
    return False


def canMove():
    for x in range(0,T_DIM):
        for y in range(1,T_DIM):
            if tiles[x][y-1] == 0 and tiles[x][y] > 0:
                return True 
            elif (tiles[x][y-1] == tiles[x][y]) and tiles[x][y-1] != 0:
                return True
    return False


####################################################
#                   Random Tile                    #
####################################################
def addRandomTile(depth=0):
    # At a higher score, random tile can be 2 or 4
    rand_tile = 2*random.randint(1,2) if score >= 100 else 2

    # Pick a random location, 
    a,b = random.randint(0,T_DIM-1),random.randint(0,T_DIM-1)   
    if not tiles[a][b]:
        tiles[a][b] = rand_tile
        return True
    elif depth == 30:
        return False
    addRandomTile(depth+1)


####################################################
#                     MAIN LOOP                    #
####################################################
def game():
    addRandomTile()
    addRandomTile()
    score = 0
    while True:
            if checkIfCanGo() == True:
                if event.type == pygame.KEYDOWN:
                    if ait:
                        for _ in range(3):
                            rotate()
                        if canMove():
                            moveTiles()
                            score = mergetiles(score)
                            addRandomTile()
                        for _ in range(1):
                            rotate()
                        print('right')
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        for _ in range(1):
                            rotate()
                        if canMove():
                            moveTiles()
                            score = mergetiles(score)
                            addRandomTile()
                        for _ in range(3):
                            rotate()
                        print('left')
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        for _ in range(0):
                            rotate()
                        if canMove():
                            moveTiles()
                            score = mergetiles(score)
                            addRandomTile()
                        for _ in range(4):
                            rotate()
                        print('up')
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        for _ in range(2):
                            rotate()
                        if canMove():
                            moveTiles()
                            score = mergetiles(score)
                            addRandomTile()
                        for _ in range(2):
                            rotate()
                        print('down')
            else:
                print("You lose")
                pygame.quit()
                return score

            printBoard()
            pygame.display.update()

test = game()
print("Score: ", test)