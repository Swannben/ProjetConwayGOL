import threading
import pygame
import numpy as np
import time
import random

CELL_SIZE = 16
GRID_WIDTH, GRID_HEIGHT = 32,32
WIDTH, HEIGHT = GRID_WIDTH*CELL_SIZE, GRID_HEIGHT*CELL_SIZE+56
time_seq = 10
RANDOM_MODE = False
drawing =False
pause =False
global nbColor
global nbCalc
global running
running = False
nbColor =0
nbCalc =0
firstCheck=True
createdThreads=0

NB_THREADS=4


verrouCalc = threading.Lock()
verrouColor = threading.Lock()
debut = threading.Event()
zeroColor=threading.Event()
calcDone =threading.Event()


        
# Function to initialize the grid with random values
def initialize_random_grid():
    return np.random.choice([0, 1], size=(GRID_WIDTH, GRID_HEIGHT))

# Function to initialize the grid with user-drawn cells
def initialize_drawn_grid():
    return np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)

def initialize_spaceShip_grid():
    gridres=np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)
    gridres[0,0] = 1
    gridres[1,1]=1
    gridres[1,2]=1
    gridres[2,1]=1
    gridres[2,0]=1
    return gridres

grid = initialize_spaceShip_grid()



def draw_grid(screen, grid,time_seq,pause):
    police = pygame.font.Font(None, 36)
    screen.fill((0, 0, 0))
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y] == 1:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )
    if pause==False and time_seq==None:
            texte = police.render("Chargement...", True, (100, 222,100))
    elif pause==False and time_seq<(10000000):
            texte = police.render("FPS : " + str(1/time_seq), True, (255, 0,0))
    else:
            texte = police.render("PAUSE", True, (0, 230,230))
    position_texte = (10, HEIGHT+10-56)  # Remplacez par la position souhaitée
    pygame.draw.rect(
                    screen,
                    (100, 100, 100),
                    (0, GRID_HEIGHT*CELL_SIZE, WIDTH, 56),
                )
    screen.blit(texte, position_texte)
    pygame.display.update() 
	
def main():
    global running
    global nbColor
    global nbCalc
    global drawing
    global pause
    global firstCheck
    global debut
    global zeroColor
    running=True
    print("Start")
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")
    draw_grid(screen,grid,None,pause)
    clock = pygame.time.Clock()
    createdThread=0
    for x in range(NB_THREADS//2):
        for y in range(NB_THREADS//2):
            createdThread+=1
            print(createdThread,"/",NB_THREADS)
            threading.Thread(target=cell,args=((GRID_WIDTH//(NB_THREADS//2))*x
                                               ,(GRID_HEIGHT//(NB_THREADS//2))*y
                                               ,(GRID_WIDTH//(NB_THREADS//2))*(x+1)
                                               ,(GRID_HEIGHT//(NB_THREADS//2))*(y+1))).start()
    debut.set()
    start_time = time.time()
    zeroColor.set()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not RANDOM_MODE:
                    drawing = True
                    x, y = pygame.mouse.get_pos()
                    x //= CELL_SIZE
                    y //= CELL_SIZE
                    grid[x, y] = 1
                    draw_grid(screen,grid,100000000000,pause)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drawing = False
            elif event.type == pygame.MOUSEMOTION and drawing:
                x, y = pygame.mouse.get_pos()
                x //= CELL_SIZE
                y //= CELL_SIZE
                grid[x, y] = 1
                draw_grid(screen,grid,100000000000,pause)
            elif event.type == pygame.KEYDOWN:
                if event.key== pygame.K_SPACE:
                    draw_grid(screen,grid,10000000000000,pause)
                    if pause==True:
                            pause = False
                    elif pause==False:
                            pause=True
        if nbCalc==NB_THREADS:
             calcDone.set()
        if nbColor==NB_THREADS:
            if drawing==False and pause== False and firstCheck==True :
                end_time = time.time()
                time_seq=end_time-start_time
                start_time = time.time()
                draw_grid(screen,grid,time_seq,pause)
                nbColor =0
                nbCalc=0
                calcDone.clear()
                zeroColor.set()
                firstCheck=False

                

               
               
          
def cell(xStart,yStart,xEnd,yEnd):
    global running
    global nbColor
    global nbCalc
    global firstCheck
    global debut
    global zeroColor
    debut.wait()
    nextStateGrid = np.zeros((xEnd - xStart, yEnd - yStart))
    while(running):
        zeroColor.wait()
        if not pause and not drawing :
            while pause==True or drawing==True :
                pass
            for x in range(xStart,xEnd):
                 for y in range (yStart,yEnd):
                    neighbors = [
                        grid[(x + i) % GRID_WIDTH, (y + j) % GRID_HEIGHT]
                        for i in range(-1, 2)
                        for j in range(-1, 2)
                        ]
                    num_neighbors = sum(neighbors) - grid[x, y]
                    nextStateGrid[x-xStart,y-yStart]=grid[x, y]
                    if grid[x, y] == 1 and (num_neighbors < 2 or num_neighbors > 3):
                        nextStateGrid[x-xStart,y-yStart] = 0
                    elif grid[x, y] == 0 and num_neighbors == 3:
                        nextStateGrid[x-xStart,y-yStart] = 1
            verrouCalc.acquire()
            nbCalc+=1
            verrouCalc.release()
            calcDone.wait()
            grid[xStart:xEnd,yStart:yEnd]=nextStateGrid
            firstCheck=True
            try:
                verrouColor.acquire()
                zeroColor.clear()
                nbColor+=1
            finally:
                verrouColor.release()

        
          
     
     
if __name__ == "__main__":
    main()

