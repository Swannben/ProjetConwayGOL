import pygame
import numpy as np
import time

# If skander gave another version of the code, we can use it instead of this one

# Constants  to have the different sizes to test we currently change them directly here 

CELL_SIZE = 10
GRID_WIDTH, GRID_HEIGHT = 64,64
WIDTH, HEIGHT = GRID_WIDTH*CELL_SIZE, GRID_HEIGHT*CELL_SIZE+56
time_seq = 10
RANDOM_MODE = False


# Function to initialize the grid with random values
def initialize_random_grid():
    return np.random.choice([0, 1], size=(GRID_WIDTH, GRID_HEIGHT))

# Function to initialize the grid with user-drawn cells
def initialize_drawn_grid():
    return np.zeros((GRID_WIDTH, GRID_HEIGHT), dtype=int)

# Function to update the grid based on the rules of Conway's Game of Life
def update_grid(grid):
    new_grid = grid.copy()

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            neighbors = [
                grid[(x + i) % GRID_WIDTH, (y + j) % GRID_HEIGHT]
                for i in range(-1, 2)
                for j in range(-1, 2)
            ]

            # Apply Conway's rules
            num_neighbors = sum(neighbors) - grid[x, y]
            if grid[x, y] == 1 and (num_neighbors < 2 or num_neighbors > 3):
                new_grid[x, y] = 0
            elif grid[x, y] == 0 and num_neighbors == 3:
                new_grid[x, y] = 1

    return new_grid

# Function to draw the grid
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
    if pause==False and time_seq<(10000000):
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

# Main function
def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")

    clock = pygame.time.Clock()

    
    drawing = False
    pause=False
    actionEffectue=False
    grid = initialize_drawn_grid()

    running = True
    
    
    
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not RANDOM_MODE:
                    drawing = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drawing = False
            elif event.type == pygame.MOUSEMOTION and drawing:
                x, y = pygame.mouse.get_pos()
                x //= CELL_SIZE
                y //= CELL_SIZE
                grid[x, y] = 1
            elif event.type == pygame.KEYDOWN:
                if event.key== pygame.K_SPACE:
                    if pause==True:
                            pause = False
                    elif pause==False:
                            pause=True
                        
        
        
        
        if drawing==False and pause== False :
            start_time = time.time()
            grid = update_grid(grid)
            end_time = time.time()

        time_seq = end_time - start_time


        draw_grid(screen, grid,time_seq,pause)
        end_time=0
        start_time=0

        pygame.display.flip()
        """clock.tick(time_seq)"""
        end_time = time.time()
        


    pygame.quit()

if __name__ == "__main__":
    main()
