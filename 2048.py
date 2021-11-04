import pygame
import random
import sys

pygame.init()

HEIGHT, WIDTH = 600,600
T_HEIGHT, T_WIDTH = HEIGHT//4, WIDTH//4
T_DIM = 4

surface = pygame.display.set_mode((HEIGHT,WIDTH),0,32)  # width, height, flags, depth (bits per pixel)
pygame.display.set_caption("2048")   # Title on the popup window


font = pygame.font.SysFont("monospace",40)
fontofscore = pygame.font.SysFont("monospace",30)

score = 0
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
    for i in range(T_DIM):
        for k in range(T_DIM):
            if tiles[i][k] == tiles[i][k+1] and tiles[i][k] != 0:
                tiles[i][k] = tiles[i][k]*2
                tiles[i][k+1] = 0 
                score += tiles[i][k]
                moveRight()


####################################################
#                   Move Tiles                     #
####################################################
def moveRight():
    for x in range(T_DIM-2,-1,-1):
        for y in range(T_DIM):
            for z in range(T_DIM-1-x):
                if not tiles[x+z+1][y]:
                    tiles[x+z+1][y] = tiles[x+z][y]
                    tiles[x+z][y] = 0
def moveLeft():
    for x in range(1,T_DIM):
        for y in range(T_DIM):
            for z in range(x):
                if not tiles[x-1-z][y] and tiles[x-z][y]:
                    tiles[x-z-1][y] = tiles[x-z][y]
                    tiles[x-z][y] = 0
def moveUp():
    for x in range(T_DIM):
        for y in range(1,T_DIM):
            for z in range(y):
                if not tiles[x][y-1-z] and tiles[x][y-z]:
                    tiles[x][y-1-z] = tiles[x][y-z]
                    tiles[x][y-z] = 0
def moveDown():
    for x in range(T_DIM):
        for y in range(T_DIM-2,-1,-1):
            for z in range(T_DIM-1-y):
                if not tiles[x][y+1+z]:
                    tiles[x][y+1+z] = tiles[x][y+z]
                    tiles[x][y+z] = 0

            
####################################################
#                  Evaluate Move                   #
####################################################
# def canMove():
#     for x in range(T_DIM):
#         for y in range(T_DIM):
#             if tiles[x][y-1] == 0 and tiles[x][y] > 0:
#                 return True 
#             elif (tiles[x][y-1] == tiles[x][y]) and tiles[x][y-1] != 0:
#                 return True
#     return False


####################################################
#                   Random Tile                    #
####################################################
def addRandomTile():
    a,b = random.randint(0,3), random.randint(0,3)
    if tiles[a][b]:
        addRandomTile()
    tiles[a][b] = 2
    return


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
        
        if not canMove():
            print("you lost")
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                moveRight()
                lost = canMove()
                print('right')
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                moveLeft()
                print('left')
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                moveUp()
                print('up')
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                moveDown()
                print('down')
            addRandomTile()

        printBoard()
        pygame.display.update()
