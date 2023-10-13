import pygame
import numpy as np
import time

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
FPS = 10

# Function to initialize the grid with random values
def initialize_grid():
    return np.random.choice([0, 1], size=(GRID_WIDTH, GRID_HEIGHT))

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

    grid = initialize_grid()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        grid = update_grid(grid)
        draw_grid(screen, grid)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
