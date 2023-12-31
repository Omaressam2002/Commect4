import pygame
import time
import os
from gui_utils import *
from gui_widgets import *
from search_tree import *

# Game window
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.Font(None, 27)

def draw_board(board, current_col, current_player):
    # Draw the black background for the board area
    pygame.draw.rect(screen, DARK_GRAY, (board_x, board_y, WIDTH, HEIGHT))

    # Draw the red border around the board frame
    border_width = 5
    pygame.draw.rect(screen, RED, (board_x - border_width, board_y - border_width,
                                   WIDTH + 2 * border_width, HEIGHT + border_width), border_width)

    for row in range(ROWS):
        for col in range(COLS):
            cell_rect = pygame.Rect(board_x + col * CELL_SIZE, board_y + (row + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            screen.blit(CELL_IMAGE, cell_rect)

            if board[row][col] == 1:
                screen.blit(RED_CHECKER_IMAGE, cell_rect)
            elif board[row][col] == 2:
                screen.blit(YELLOW_CHECKER_IMAGE, cell_rect)

    if current_col is not None:
        # Draw the checker above the selected column with the player color
        checker_image = RED_CHECKER_IMAGE if current_player == 1 else YELLOW_CHECKER_IMAGE
        checker_rect = pygame.Rect(board_x + current_col * CELL_SIZE, board_y, CELL_SIZE, CELL_SIZE)
        screen.blit(checker_image, checker_rect)

    # Draw the bottom border of the board frame
    pygame.draw.rect(screen, RED, (board_x - border_width, board_y + HEIGHT, WIDTH + 2 * border_width, border_width))
    
    # Draw the checkbox
    screen.blit(checkbox_image, (checkbox_x, checkbox_y))
    checkbox_label = font.render("Display Search Tree", True, WHITE)
    checkbox_label_x = checkbox_x + checkbox_image.get_width() + 5
    checkbox_label_y = checkbox_y - (checkbox_label.get_height() - checkbox_image.get_height()) // 2
    screen.blit(checkbox_label, (checkbox_label_x, checkbox_label_y))
    
    # Define the bold and underlined font
    bold_underline_font = pygame.font.Font(None, 34)
    bold_underline_font.set_underline(True)

    # Render the label using the bold and underlined font
    strategy_label = bold_underline_font.render("Game Strategy: ", True, WHITE)
    screen.blit(strategy_label, (strategy_label_x, strategy_label_y))
    
    # Draw the radiobuttons
    screen.blit(radiobutton_image, (radiobutton_x, radiobutton_y))
    radiobutton_label1 = font.render("Alpha-Beta pruning", True, WHITE)
    radiobutton1_label_x = radiobutton_x + radiobutton_image.get_width() + 5
    radiobutton1_label_y = radiobutton_y - (radiobutton_label1.get_height() - radiobutton_image.get_height()) // 2
    screen.blit(radiobutton_label1, (radiobutton1_label_x, radiobutton1_label_y))
    
    screen.blit(radiobutton2_image, (radiobutton_x, radiobutton2_y))
    radiobutton_label2 = font.render("Expected Minimax", True, WHITE)
    radiobutton2_label_x = radiobutton_x + radiobutton2_image.get_width() + 5
    radiobutton2_label_y = (radiobutton2_y) - (radiobutton_label2.get_height() - radiobutton2_image.get_height()) // 2
    screen.blit(radiobutton_label2, (radiobutton2_label_x, radiobutton2_label_y))
    
    # Draw the start game button
    pygame.draw.rect(screen, GRAY, start_game_button_rect, border_radius=5)
    start_text = font.render("Start Game", True, BLACK)
    start_text_rect = start_text.get_rect(center=start_game_button_rect.center)
    screen.blit(start_text, start_text_rect)

    # If the mouse is hovering over the button
    if start_game_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, DARK_GRAY, start_game_button_rect, border_radius=5, width=3)
    
    pygame.display.update()
    
    
def main():
    board = [[0] * COLS for _ in range(ROWS)]
    players = [1, 2]  # Red = Player 1, Yellow = Player 2
    current_player = 1  # Index of the current player
    current_col = None  # Index of the current column where the checker is being selected
    game_over = True
    display_search_tree_flag = False
    alpha_beta_pruning_flag = False
    expected_minimax_flag = False
    global checkbox_image, radiobutton_image, radiobutton2_image
    
    # background image
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
    background_image = pygame.transform.scale(background_image, (WIDTH+700, HEIGHT+200))
    
    screen.blit(background_image, (0, 0))
    
    # wait for the strategy
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 
            
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_x, _ = pygame.mouse.get_pos()
                    
                    # if the checkbox is clicked
                    if checkbox_x <= mouse_x < checkbox_x + checkbox_image.get_width() and checkbox_y <= mouse_y < checkbox_y + checkbox_image.get_height():
                        display_search_tree_flag = toggle_flag(display_search_tree_flag)
                        print("display search tree = ", display_search_tree_flag)
                        checkbox_image = checkbox_checked_image if display_search_tree_flag else checkbox_unchecked_image
                        pygame.display.update()  
                        
                    # if radiobutton1 is clicked
                    if radiobutton_x <= mouse_x < radiobutton_x + radiobutton_image.get_width() and radiobutton_y <= mouse_y < radiobutton_y + radiobutton_image.get_height():
                        alpha_beta_pruning_flag = toggle_flag(alpha_beta_pruning_flag)  # toggle the minimax expected flag
                        print("alpha-beta pruning: ", alpha_beta_pruning_flag)
                        radiobutton_image = radiobutton_checked_image if alpha_beta_pruning_flag else radiobutton_unchecked_image
                        
                        if expected_minimax_flag == True :
                            expected_minimax_flag = toggle_flag(expected_minimax_flag)  # toggle the minimax expected flag
                            print("minimax expected: ", expected_minimax_flag)
                            radiobutton2_image = radiobutton_checked_image if expected_minimax_flag else radiobutton_unchecked_image
                        
                        pygame.display.update()  
                        
                    # if radiobutton2 is clicked
                    if radiobutton_x <= mouse_x < radiobutton_x + radiobutton2_image.get_width() and radiobutton2_y <= mouse_y < radiobutton2_y + radiobutton2_image.get_height():
                        expected_minimax_flag = toggle_flag(expected_minimax_flag)  # toggle the minimax expected flag
                        print("minimax expected: ", expected_minimax_flag)
                        radiobutton2_image = radiobutton_checked_image if expected_minimax_flag else radiobutton_unchecked_image
                        pygame.display.update() 
                        
                        if  alpha_beta_pruning_flag == True :
                            alpha_beta_pruning_flag = toggle_flag(alpha_beta_pruning_flag)  # toggle the alpha-beta expected flag
                            print("alpha-beta pruning: ", alpha_beta_pruning_flag)
                            radiobutton_image = radiobutton_checked_image if alpha_beta_pruning_flag else radiobutton_unchecked_image
                        
                    if start_game_button_rect.collidepoint(event.pos):
                        game_over = False
                        
        # background image
            background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
            background_image = pygame.transform.scale(background_image, (WIDTH+700, HEIGHT+200))
            
            screen.blit(background_image, (0, 0))
            draw_board(board, current_col, players[current_player])

            pygame.display.set_caption("Connect 4")
            pygame.display.flip()
    
    if current_player == 1 : #AI FIRST TURN (MAXIMIZER PLAYER)
        current_player, board , tree = ai_turn(board, current_player, players, alpha_beta_pruning_flag, expected_minimax_flag)
        
        if display_search_tree_flag == True:
                                tree_visualizer = TreeVisualizationGUI()
                                tree_visualizer.draw_tree(tree.root)
                                tree_visualizer.run()
    
    while not game_over:
        winner, score = check_win(board)
        draw_score_label(winner, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the mouse is within the board's boundaries
                if board_x <= mouse_x < board_x + WIDTH:
                    current_col = (mouse_x - board_x) // CELL_SIZE
                else:
                    current_col = None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_x, _ = pygame.mouse.get_pos()
                    
                    # Check if the mouse press position is within the board's boundaries
                    if board_x <= mouse_x < board_x + WIDTH:
                        col = (mouse_x - board_x) // CELL_SIZE

                        # Find the lowest empty row in the column
                        for row in range(ROWS - 1, -1, -1):
                            if board[row][col] == 0:
                                animate_checker_movement(board, row, col, players[current_player])
                                board[row][col] = players[current_player]
                                break

                        # Check the winner
                        # 0 -> withdrawal, 1 -> red, 2 -> yellow
                        if is_board_full(board):
                            # winner,score = check_win(board)
                            # draw_winner_label(winner)
                            # print(str(players[current_player]), " WINS")
                            # GAME OVER -> GAME ENDS BUT NOT EXIT
                            game_over = True
                            break
                        
                        
                        # background image
                        background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
                        background_image = pygame.transform.scale(background_image, (WIDTH+700, HEIGHT+200))
                        
                        screen.blit(background_image, (0, 0))
                        draw_board(board, current_col, players[current_player])
                        winner, score = check_win(board)
                        draw_score_label(winner, score)

                        # Switch to the next player
                        # HERE I WILL ADD THE TURN OF AI BUT NOT IMPLEMENTED YET, BS AKENO 2 USERS DED BA3D
                        current_player = switch_players(current_player, players)
                        
                        if current_player == 1 : #AI turn
                            
                            current_player, board , tree= ai_turn(board, current_player, players, alpha_beta_pruning_flag, expected_minimax_flag)
                            
                            if display_search_tree_flag == True:
                                tree_visualizer = TreeVisualizationGUI()
                                tree_visualizer.draw_tree(tree.root)
                                tree_visualizer.run()
                                
                                
                        current_col = None
                        
                        while game_over:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    return


        # background image
        background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        background_image = pygame.transform.scale(background_image, (WIDTH+700, HEIGHT+200))
        
        screen.blit(background_image, (0, 0))
        draw_board(board, current_col, players[current_player])

        pygame.display.set_caption("Connect 4")
        pygame.display.flip()
        
    winner,score = check_win(board)
    draw_winner_label(winner,score)
    print(str(players[current_player]), " WINS")
    # GAME OVER -> GAME ENDS BUT NOT EXIT
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    main()
