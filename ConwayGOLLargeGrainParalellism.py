import threading
import numpy as np
import time
import random

CELL_SIZE = 16
GRID_WIDTH, GRID_HEIGHT = 4,4
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

grid = initialize_random_grid()



	
def main():
    global running
    global nbColor
    global nbCalc
    global drawing
    global pause
    global firstCheck
    global debut
    global zeroColor
    howManyTime=0
    running=True
    print("Start")
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
    while running  and howManyTime<100:
        if nbCalc==NB_THREADS:
             calcDone.set()
        if nbColor==NB_THREADS:
            if drawing==False and pause== False and firstCheck==True :
                end_time = time.time()
                time_seq=end_time-start_time
                start_time = time.time()
                print(str(1/time_seq)+",")
                nbColor =0
                nbCalc=0
                calcDone.clear()
                zeroColor.set()
                howManyTime+=1
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

