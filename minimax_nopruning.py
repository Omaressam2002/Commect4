import numpy as np
import sys
import time
import random
import numpy as np

DIMENSIONS = (6,7)
MAX_DEPTH = 3
AI_PLAYER = 2
PLAYER = 1


class State:
    def __init__(self):
        self.board = np.zeros((DIMENSIONS[0],DIMENSIONS[1]), dtype=int)
        self.children = []
        self.max = None
        self.max_child = None
        self.min = None
        self.min_child = None
        self.parent = None
        self.level = 0
    
    def __str__(self):
        return str(self.board)
    
    def setParent(self,parent):
        self.parent = parent
        self.parent.children.append(self)
        self.level = self.parent.level + 1


def is_terminal(state):
    if 0 not in state.board[0] or state.level >= MAX_DEPTH:
        return True
    return False


def eval(subarr,turn):
    opponent_turn = PLAYER
    if turn == PLAYER:
        opponent_turn = AI_PLAYER
    score = 0
    if subarr.count(turn) == 4:
        score += 100
    elif subarr.count(turn) == 3 and subarr.count(0) == 1:
        score += 25
    elif subarr.count(turn) == 2 and subarr.count(0) == 2:
        score += 10
    return score  

def heuristic(state,turn):
    score = 0
    board = state.board
    
    center_count = num_center(board,turn)
    score += center_count * 10

    # score horizontal
    for r in range(DIMENSIONS[0]):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(DIMENSIONS[1] - 3):
            subarr = row_array[c:c + 4]
            score += eval(subarr, AI_PLAYER)
            score -= eval(subarr, PLAYER)

    # score vertical
    for c in range(DIMENSIONS[1]):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(DIMENSIONS[0]-3):
            subarr = col_array[r:r+4]
            score += eval(subarr, AI_PLAYER)
            score -= eval(subarr, PLAYER)

    # score positively sloped diagonals
    for r in range(3,DIMENSIONS[0]):
        for c in range(DIMENSIONS[1] - 3):
            subarr = [board[r-i][c+i] for i in range(4)]
            score += eval(subarr, AI_PLAYER)
            score -= eval(subarr, PLAYER)

    # score negatively sloped diagonals
    for r in range(3,DIMENSIONS[0]):
        for c in range(3,DIMENSIONS[1]):
            subarr = [board[r-i][c-i] for i in range(4)]
            score += eval(subarr, AI_PLAYER)
            score -= eval(subarr, PLAYER)

    return score


def num_center(board,turn):
    start_row = DIMENSIONS[0] // 3
    end_row = DIMENSIONS[0] - start_row
    start_col = DIMENSIONS[1] // 3
    end_col = DIMENSIONS[1] - start_col 
    center_elements = board[start_row:end_row, start_col:end_col]
    count_ones = np.count_nonzero(center_elements == AI_PLAYER)
    count_zeros = np.count_nonzero(center_elements == PLAYER)
    return count_ones-count_zeros

def generate_children(state,player):
    children = []
    for j in range(DIMENSIONS[1]):
        for i in range(DIMENSIONS[0]-1 , -1, -1):
            if state.board[i][j] == 0:
                child = State()
                child.board = np.copy(state.board)
                child.board[i][j] = player
                child.setParent(state)
                children.append((child,j))
                break
    return children




# def eval(subarr,turn):
#     opponent_turn = PLAYER
#     if turn == PLAYER:
#         opponent_turn = AI_PLAYER
#     score = 0
#     if subarr.count(turn) == 4:
#         score += 100
#     elif subarr.count(turn) == 3 and subarr.count(0) == 1:
#         score += 25
#     elif subarr.count(turn) == 2 and subarr.count(0) == 2:
#         score += 10

#     # or decrese it if the oponent has 3 in a row
#     if subarr.count(opponent_turn) == 3 and subarr.count(0) == 1:
#         score -= 25
#     elif subarr.count(opponent_turn) == 2 and subarr.count(0) == 2:
#         score -= 10 

#     return score  

# def heuristic(state,turn):
#     score = 0
#     board = state.board
    
#     center_count = num_center(board,turn)
#     score += center_count * 10

#     # score horizontal
#     for r in range(DIMENSIONS[0]):
#         row_array = [int(i) for i in list(board[r,:])]
#         for c in range(DIMENSIONS[1] - 3):
#             subarr = row_array[c:c + 4]
#             score += eval(subarr, turn)

#     # score vertical
#     for c in range(DIMENSIONS[1]):
#         col_array = [int(i) for i in list(board[:,c])]
#         for r in range(DIMENSIONS[0]-3):
#             subarr = col_array[r:r+4]
#             score += eval(subarr, turn)

#     # score positively sloped diagonals
#     for r in range(3,DIMENSIONS[0]):
#         for c in range(DIMENSIONS[1] - 3):
#             subarr = [board[r-i][c+i] for i in range(4)]
#             score += eval(subarr, turn)

#     # score negatively sloped diagonals
#     for r in range(3,DIMENSIONS[0]):
#         for c in range(3,DIMENSIONS[1]):
#             subarr = [board[r-i][c-i] for i in range(4)]
#             score += eval(subarr, turn)

#     if turn == PLAYER :
#         return -score
#     return score


# def num_center(board,turn):
#     start_row = DIMENSIONS[0] // 3
#     end_row = DIMENSIONS[0] - start_row
#     start_col = DIMENSIONS[1] // 3
#     end_col = DIMENSIONS[1] - start_col 
#     center_elements = board[start_row:end_row, start_col:end_col]
#     count_ones = np.count_nonzero(center_elements == turn)
#     return count_ones


