import pygame
import time
import game_page
from gui_widgets import *
from minimax_nopruning import *

def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True 

def toggle_flag (flag):
    flag = not flag
    return flag 

def switch_players (player, players):
    current_player = (player + 1) % len(players)
    return current_player

def decision_maker(board):
    # HASSANOLA ALGO GOES HERE
    # MAKE SURE TO RETURN THE 2D MATRIX AS FOLLOWS :)
    # return [[0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0],
    #         [2, 0, 0, 0, 0, 0, 0],
    #         [1, 0, 0, 0, 0, 0, 0],]
    state = State(board)
    child = decision(state)
    print(child)
    return child.board
     

def ai_turn (board, current_player, players, alpha_beta_pruning_flag, expected_minimax_flag):
    prev_board = board
    if alpha_beta_pruning_flag == False and expected_minimax_flag == False: #Normal mode
        print("normal mode")
        
        
        # NORMAL MODE ALGORITHM
        
        
    elif alpha_beta_pruning_flag == True: #Alpha-beta pruning mode
        print("alpha-beta pruning")
        
        
        # ALPHA BETA PRUNING ALGORITHM
        
        
    else: #Expectiminimax mode
        print("expectiminimax")
        
        
        # EXPECTIMINIMAX ALGORITHM
        
    board = decision_maker(board) #HASSAN'S HEURTISTIC FUNCTION
    row, col = find_inserted_checker(prev_board, board)
    animate_checker_movement(prev_board, row, col, current_player + 1)
    current_player = switch_players(current_player, players)
    return current_player, board

def find_inserted_checker(prev_board, current_board):
    for col in range(len(prev_board[0])):
        for row in range(len(prev_board)):
            if prev_board[row][col] != current_board[row][col]:
                return row, col

def count_connected_fours(board, player):
    
    count = 0
    
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and board[row][col + 3] == player:
                count += 1

    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and board[row + 3][col] == player:
                count += 1

    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                count += 1

    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if board[row][col] == player and board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and board[row + 3][col - 3] == player:
                count += 1

    return count


def check_win(board):
    player1_count = count_connected_fours(board, 1)
    player2_count = count_connected_fours(board, 2)

    if player1_count > player2_count:
        return 1
    elif player2_count > player1_count:
        return 2
    else:
        return 0

def animate_checker_movement(board, row, col, player):
    target_x = board_x + col * CELL_SIZE + (CELL_SIZE // 2) - (RED_CHECKER_IMAGE.get_width() // 2)
    target_y = board_y + (row + 1) * CELL_SIZE
    target_pos = (target_x, target_y)
    checker_image = RED_CHECKER_IMAGE if player == 1 else YELLOW_CHECKER_IMAGE
    current_pos = (board_x + col * CELL_SIZE, board_y)
    step = 20

    while current_pos[1] < target_pos[1]:

        game_page.draw_board(board, None, None)

        current_pos = (current_pos[0], current_pos[1] + step)
        game_page.screen.blit(checker_image, current_pos)

        pygame.display.update()
        time.sleep(0.0005)

    # Draw the checker at the target position
    game_page.screen.blit(checker_image, target_pos)
    pygame.display.update()
    

def draw_winner_label(player):
    # Determine the player color and text
    color = RED if player == 1 else YELLOW if player == 2 else WHITE
    text = f"Player {player} wins!"
    font = pygame.font.Font(None, 42)

    label_surface = font.render(text, True, color)

    label_x = (screen_width - label_surface.get_width()) // 2
    label_y = board_y - label_surface.get_height() - 20

    game_page.screen.blit(label_surface, (label_x, label_y))
    pygame.display.update()