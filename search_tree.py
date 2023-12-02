import pygame
import math
import random

# Constants for GUI visualization
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
NODE_RADIUS = 20
LEVEL_HEIGHT = 100
LEVEL_WIDTH = WINDOW_WIDTH // 7

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Function to draw a node
def draw_node(x, y, color):
    pygame.draw.circle(window, color, (x, y), NODE_RADIUS)
    pygame.display.update()

# Function to draw an edge between two nodes
def draw_edge(x1, y1, x2, y2, color):
    pygame.draw.line(window, color, (x1, y1), (x2, y2), 2)
    pygame.display.update()

# Function to calculate the x-coordinate of a node based on its level and position in the level
def get_node_x(level, position):
    return (WINDOW_WIDTH // 2) + ((position - 3) * LEVEL_WIDTH)

# Function to calculate the y-coordinate of a node based on its level
def get_node_y(level):
    return level * LEVEL_HEIGHT

# Function to draw the minimax tree
def draw_tree(states):
    num_levels = math.ceil(math.log(len(states), 7)) + 1

    for level in range(1, num_levels + 1):
        num_nodes_in_level = 7 ** (level - 1)

        for position in range(num_nodes_in_level):
            node_x = get_node_x(level, position)
            node_y = get_node_y(level)
            node_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            draw_node(node_x, node_y, node_color)

            if level > 1:
                parent_level = level - 1
                parent_position = (position - 1) // 7
                parent_x = get_node_x(parent_level, parent_position)
                parent_y = get_node_y(parent_level)

                draw_edge(node_x, node_y, parent_x, parent_y, (255, 255, 255))

# Generate random objects as states of the 2D board
states = [random.randint(0, 100) for _ in range(7 ** 3)]

# Call the draw_tree function to visualize the minimax tree
draw_tree(states)

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()