import pygame
import time
import game_page
from gui_widgets import *
from minimax_nopruning import *
from MM import *
from MMpruning import *
from expectiMM import *
from Tree import *
import timeit

count = 0
its_tree_timee = [4]

def toggle_flag (flag):
    flag = not flag
    return flag 

def switch_players (player, players):
    current_player = (player + 1) % len(players)
    return current_player

def ai_turn (board, current_player, players, alpha_beta_pruning_flag, expected_minimax_flag):
    global count
    
    state = State()
    state.board = np.copy(board)
    prev_board=board
    visited = dict({})
    visited_nodes = set()

    if alpha_beta_pruning_flag :
        start = timeit.timeit()
        alpha = -sys.maxsize
        beta = sys.maxsize
        child,util,_,_ = maximize_alpha_beta(state,visited,visited_nodes,alpha,beta)
        state.max = util
        end = timeit.timeit()
        #print(end - start)
        tree = MMTree(state)
    elif expected_minimax_flag :
        start = timeit.timeit()
        child,util = expecti_maximize(state,visited,visited_nodes)
        state.max = util
        end = timeit.timeit()
        #print(end - start)
        tree = MMTree(state)   
    else :
        start = timeit.timeit()
        child,util = maximize(state,visited,visited_nodes)
        state.max = util
        end = timeit.timeit()
        #print(end,start)
        tree = MMTree(state)


    count +=1
    if count in its_tree_timee :
        tree.tree_traverse(state)
    row, col = find_inserted_checker(prev_board, child.board)
    animate_checker_movement(prev_board, row, col, current_player + 1)
    current_player = switch_players(current_player, players)
    return current_player, child.board , tree


def find_inserted_checker(prev_board, current_board):
    for col in range(len(prev_board[0])):
        for row in range(len(prev_board)):
            if prev_board[row][col] != current_board[row][col]:
                return row, col

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
    
def draw_winner_label(player, score):
    # Determine the player color and text
    color = RED if player == 1 else YELLOW if player == 2 else WHITE
    
    text = f"Player {player} wins! "
    
    if color == WHITE:
        text = f"Withdrawal!"
    
    font = pygame.font.Font(None, 42)

    label_surface = font.render(text, True, color)

    label_x = (screen_width - label_surface.get_width()) // 2
    label_y = board_y - label_surface.get_height() - 20

    game_page.screen.blit(label_surface, (label_x, label_y))
    pygame.display.update()
    draw_score_label(player, score)
    
    
def draw_score_label(player, score):
    color = RED if score[0] > score[1] else YELLOW if score[0] < score[1] else WHITE
    text1 = f"Score:"
    text2 = f"Player : {score[0]} - AI : {score[1]}"
    font = pygame.font.Font(None, 42)

    # Render text1
    label_surface1 = font.render(text1, True, color)
    label_x1 = (board_x + WIDTH + 100)
    label_y1 = checkbox_y + 70

    # Render text2
    label_surface2 = font.render(text2, True, color)
    label_x2 = label_x1 - 50
    label_y2 = label_y1 + label_surface1.get_height() + 20 # Adjusted position for text2

    # Blit both surfaces
    game_page.screen.blit(label_surface1, (label_x1, label_y1))
    game_page.screen.blit(label_surface2, (label_x2, label_y2))
    pygame.display.update()

def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True 

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
    
    score = (player1_count,player2_count)
    if player1_count > player2_count:
        return 1,score
    elif player2_count > player1_count:
        return 2,score
    else:
        return 0,score



