import pygame
import random
import sys

pygame.init()

HEIGHT, WIDTH = 600,600
T_HEIGHT, T_WIDTH = HEIGHT//4, WIDTH//4

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

    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
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
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # if valid_move('right'):
                #     movetiles('right')
                print('right')
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                print('left')
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                print('up')
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                print('down')


    printBoard()
    pygame.display.update()