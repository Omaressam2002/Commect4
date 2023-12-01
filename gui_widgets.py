import pygame, os

# Set up the dimensions of the game board
CELL_SIZE = 80
ROWS = 6
COLS = 7
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * (ROWS + 1)  

# Set up the colors
WHITE = (255, 255, 255)
RED = (238, 30, 35)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
DARK_GRAY = (29, 29, 29)

# Images
CELL_IMAGE = pygame.image.load("Commect4/assets/board_cell.png")
RED_CHECKER_IMAGE = pygame.image.load("Commect4/assets/red_chip.png")
YELLOW_CHECKER_IMAGE = pygame.image.load("Commect4/assets/yellow_chip.png")
BACKGROUND_IMAGE_PATH = os.path.join("Commect4/assets", "game_page_background.png")

screen_width = WIDTH + 700
screen_height = HEIGHT + 200

# X and Y coordinates of the center of the board
board_x = (screen_width - WIDTH) // 2 + 20
board_y = (screen_height - HEIGHT) // 2

# Set up the button dimensions and position
# button_width = 200
# button_height = 50
# button_x = 15
# button_y = (screen_height - button_height) // 4

# Checkbox dimensions and position
checkbox_x = 50 
checkbox_y = screen_height // 4

checkbox_checked_image = pygame.image.load("Commect4/assets/checkbox_checked2.png")
checkbox_unchecked_image = pygame.image.load("Commect4/assets/checkbox_unchecked2.png")
checkbox_image = checkbox_unchecked_image

strategy_label_x = 50
strategy_label_y = checkbox_y + 70

radiobutton_x = 50
radiobutton_y = strategy_label_y + 40
radiobutton2_y = radiobutton_y + 60

radiobutton_checked_image = pygame.image.load("Commect4/assets/radiobutton_checked.png")
radiobutton_unchecked_image = pygame.image.load("Commect4/assets/radiobutton_unchecked.png")
radiobutton_image = radiobutton_unchecked_image
radiobutton2_image = radiobutton_unchecked_image
