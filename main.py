import pygame
import numpy as np

# Constants

CELL_SIZE = 3
GRID_WIDTH, GRID_HEIGHT =200,200
WIDTH, HEIGHT = GRID_WIDTH*CELL_SIZE, GRID_HEIGHT*CELL_SIZE
FPS = 10
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
def draw_grid(screen, grid):
    screen.fill((0, 0, 0))
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y] == 1:
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )

# Main function
def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")

    clock = pygame.time.Clock()

    
    drawing = False
    grid = initialize_drawn_grid()

    running = True
    import time

    
    
    police = pygame.font.Font(None, 36)
    while running:
        start_time = time.time()
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

        
        if drawing==False:
            grid = update_grid(grid)
        draw_grid(screen, grid)

        pygame.display.flip()
        """clock.tick(FPS)"""
        end_time = time.time()
        time_seq = end_time - start_time
        texte = police.render("FPS : " + str(1/time_seq), True, (255, 0,0))
        position_texte = (10, 10)  # Remplacez par la position souhaitée
        screen.blit(texte, position_texte)
        pygame.display.update() 

    pygame.quit()

if __name__ == "__main__":
    main()
