import pygame
import random
import sys

from math import floor


pygame.init()

HEIGHT, WIDTH = 600,600
T_HEIGHT, T_WIDTH = HEIGHT//4, WIDTH//4
T_DIM = 4

surface = pygame.display.set_mode((HEIGHT,WIDTH),0,32)  # width, height, flags, depth (bits per pixel)
pygame.display.set_caption("2048")   # Title on the popup window


font = pygame.font.SysFont("monospace",40)
fontofscore = pygame.font.SysFont("monospace",30)

tiles = [[0,0,0,0],  # Holds values of tiles on the board
         [0,0,0,0],
         [0,0,0,0],
         [0,0,0,0]]
undomatrix = []

colors = {
    0:   (255,255,255),
    2:   (255,247,204),
    4:   (255,238,153),
    8:   (156,39,176),
    16:  (103,58,183),
    32:  (255,87,34),
    64:  (0,150,136),
    128: (139,195,74),
    256: (234,30,99),
    512: (255,152,0),
    1024:(0,0,0),
    2048:(121,85,72),
}

####################################################
#                   Summation                      #
####################################################
def mergetiles():
    for x in range(T_DIM):
        for y in range(T_DIM-1):
            if tiles[x][y] == tiles[x][y+1] and tiles[x][y] != 0:
                tiles[x][y] = tiles[x][y]*2
                tiles[x][y+1] = 0 
                # points += tiles[x][y]
                moveTiles()


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
    a,b = random.randint(0,T_DIM-1),random.randint(0,T_DIM-1)
    if not tiles[a][b]:
        tiles[a][b] = 2
        return True
    elif depth == 16:
        return False
    addRandomTile(depth+1)



####################################################
#                     GameOver                     #
####################################################
def gameover():
    surface.fill((0,0,0))

    label = font.render("gameover",1,(255,255,255))

    surface.blit(label,(50,100))
    pygame.display.update()


####################################################
#                    Print Board                   #
####################################################
def printBoard():
    border = 2
    surface.fill((240,240,240))

    for i in range(T_DIM):
        for j in range(T_DIM):
            # Draw a rectangle on 'surface' with color based on tile value
            # Third Arg: (top left x, top left y, width, height)
            pygame.draw.rect(surface, colors[tiles[i][j]], (i*T_HEIGHT+i*border, j*T_WIDTH+j*border, T_HEIGHT-2*border, T_WIDTH-2*border))

            # Label for Tile Values
            if tiles[i][j]:
                label = font.render(str(tiles[i][j]),1,(94,94,94))
                surface.blit(label,((i*T_HEIGHT)+T_HEIGHT//2,j*(T_WIDTH)+ T_WIDTH//2))
dw
            # label2 = fontofscore.render("YourScore:"+str(score),1,(255,255,255))
    return


####################################################
#                     MAIN LOOP                    #
####################################################
addRandomTile()
addRandomTile()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close window if someone clicks the X
            pygame.quit()
            sys.exit()

        if checkIfCanGo() == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    for _ in range(3):
                        rotate()
                    if canMove():
                        moveTiles()
                        mergetiles()
                    for _ in range(1):
                        rotate()
                    print('right')
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    for _ in range(1):
                        rotate()
                    if canMove():
                        moveTiles()
                        mergetiles()
                    for _ in range(3):
                        rotate()
                    print('left')
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    for _ in range(0):
                        rotate()
                    if canMove():
                        moveTiles()
                        mergetiles()
                    for _ in range(4):
                        rotate()
                    print('up')
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    for _ in range(2):
                        rotate()
                    if canMove():
                        moveTiles()
                        mergetiles()
                    for _ in range(2):
                        rotate()
                    print('down')
                addRandomTile()
        else:
            print("You lose")
            gameover()
            pygame.quit()


        printBoard()
        pygame.display.update()
