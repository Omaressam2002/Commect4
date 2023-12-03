import pygame
import sys
import subprocess
import os
from gui_widgets import *

# Start window
pygame.init()
screen = pygame.display.set_mode((START_PAGE_WIDTH, START_PAGE_HEIGHT))
clock = pygame.time.Clock()

start_button_rect = pygame.Rect(START_PAGE_WIDTH // 2 - 75, START_PAGE_HEIGHT // 2 + 150, 150, 50)

def draw_start_page():
    # Draw the background image
    background_path = os.path.join("assets", "start_page_background.png")
    background_image = pygame.image.load(background_path)
    background_image = pygame.transform.scale(background_image, (START_PAGE_WIDTH, START_PAGE_HEIGHT))
    screen.blit(background_image, (0, 0))

    # Draw the logo image
    logo_path = os.path.join("assets", "game_logo.png")
    logo_image = pygame.image.load(logo_path)
    logo_rect = logo_image.get_rect(center=(START_PAGE_WIDTH // 2, START_PAGE_HEIGHT // 2 - 50))
    screen.blit(logo_image, logo_rect)

    # Draw the start button
    pygame.draw.rect(screen, GRAY, start_button_rect, border_radius=10)
    font = pygame.font.Font(None, 32)
    start_text = font.render("Start", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    screen.blit(start_text, start_text_rect)

    # If the mouse is hovering over the button
    if start_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, DARK_GRAY, start_button_rect, border_radius=10, width=3)

    pygame.display.flip()

def game_page():
    pygame.quit()  # Close the Pygame window
    # FOR LINUX USERS CHANGE python WITH python3
    subprocess.call(["python", "game_page.py"])
    sys.exit()  # Exit the current Python script

def main():
    start = True

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start = False

        draw_start_page()
        clock.tick(60)

    game_page()

if __name__ == "__main__":
    main()
