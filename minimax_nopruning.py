import numpy as np
import sys
import time
import random
import numpy as np

DIMENSIONS = (6,7)
MAX_DEPTH = 2
AI_PLAYER = 2
PLAYER = 1


class State:
    def __init__(self,board=):
        if board == None:
            self.board = np.zeros((DIMENSIONS[0],DIMENSIONS[1]), dtype=int)
        else :
            self.board = np.array(board)
        self.children = []
        self.parent = None
        self.level = 0
    
    def __str__(self):
        return str(self.board)
    
    def setParent(self,parent):
        self.parent = parent
        self.parent.children.append(self)
        self.level = self.parent.level + 1

def decision(state,verbose=False):
    # Resetting the state each decision
    state_reset = State()
    state_reset.board = np.copy(state.board)
    visited = dict({})
    child,_ = maximize(state_reset,visited)
    return child

def maximize(state,visited):
    
    visited_nodes = set(visited.keys())
    state_str = state.__str__()
    if state_str in visited_nodes:
        return state,visited[state_str]

    # either the board is full or the level == k
    if is_terminal(state):
        hn = heuristic(state,AI_PLAYER)
        visited[state_str] = hn
        return None, hn
    
    max_child = None
    max_utility = -sys.maxsize
    
    generate_children(state,AI_PLAYER)

    # han add fen we ne update el weights fen??
    for child in state.children:
        _, utility = minimize(child,visited)
        if utility > max_utility:
            max_child = child
            max_utility = utility
    
    visited[state.__str__()] = max_utility
    # 3awzeen max depth+el string el benecreate minno el states tet7at fel header beta3 el function 3ashan hana5odha min el gui
    return max_child, max_utility


def minimize(state,visited):
    visited_nodes = set(visited.keys())
    state_str = state.__str__()
    if state_str in visited_nodes:
        return state,visited[state_str]

    # either the board is full or the level == k
    if is_terminal(state):
        hn = heuristic(state,PLAYER)
        visited[state_str] = hn
        return None, hn

    min_child = None
    min_utility = sys.maxsize
    generate_children(state,PLAYER)

    for child in state.children:
        _, utility = maximize(child,visited)
        if utility < min_utility:
            min_child = child
            min_utility = utility

    visited[state.__str__()] = min_utility
    return min_child, min_utility


def is_terminal(state):
    if state.level == (DIMENSIONS[0]*DIMENSIONS[1]) or state.level >= MAX_DEPTH:
        return True
    return False

def eval(subarr, turn):
    opponent_turn = PLAYER
    if turn == PLAYER:
        opponent_turn = AI_PLAYER

    score = 0

    if subarr.count(turn) == 4:
        score += 100
    elif subarr.count(turn) == 3 and subarr.count(0) == 1:
        score += 5
    elif subarr.count(turn) == 2 and subarr.count(0) == 2:
        score += 2

    # or decrese it if the oponent has 3 in a row
    if subarr.count(opponent_turn) == 3 and subarr.count(0) == 1:
        score -= 4 

    return score  

def heuristic(state,turn):
    score = 0
    board = state.board
    
    center_count = num_center(board,turn)
    score += center_count * 5

    # score horizontal
    for r in range(DIMENSIONS[0]):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(DIMENSIONS[1] - 3):
            subarr = row_array[c:c + 4]
            score += eval(subarr, turn)

    # score vertical
    for c in range(DIMENSIONS[1]):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(DIMENSIONS[0]-3):
            subarr = col_array[r:r+4]
            score += eval(subarr, turn)

    # score positively sloped diagonals
    for r in range(3,DIMENSIONS[0]):
        for c in range(DIMENSIONS[1] - 3):
            subarr = [board[r-i][c+i] for i in range(4)]
            score += eval(subarr, turn)

    # score negatively sloped diagonals
    for r in range(3,DIMENSIONS[0]):
        for c in range(3,DIMENSIONS[1]):
            subarr = [board[r-i][c-i] for i in range(4)]
            score += eval(subarr, turn)

    return score

def num_center(board,turn):
    start_row = DIMENSIONS[0] // 3
    end_row = DIMENSIONS[0] - start_row
    start_col = DIMENSIONS[1] // 3
    end_col = DIMENSIONS[1] - start_col 
    center_elements = board[start_row:end_row, start_col:end_col]
    count_ones = np.count_nonzero(center_elements == turn)
    return count_ones

def generate_children(state,player,verbose=False):
    for j in range(DIMENSIONS[1]):
        for i in range(DIMENSIONS[0]-1 , -1, -1):
            if state.board[i][j] == 0:
                child = State()
                child.board = np.copy(state.board)
                child.board[i][j] = player
                child.setParent(state)
                if verbose:
                    print(child)
                    print()
                    # time.sleep(0.5)
                break
