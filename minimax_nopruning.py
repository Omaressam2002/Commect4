import numpy as np
import sys
import time
import random
import numpy as np

DIMENSIONS = (6,7)
# DIMENSIONS = (4,4)
MAX_DEPTH = 5
AI_PLAYER = 2
PLAYER = 1

class State:
    def __init__(self):
        self.board = np.zeros((DIMENSIONS[0],DIMENSIONS[1]), dtype=int)
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
    child,_ = maximize(state_reset,verbose)

    return child

def maximize(state,verbose=False):
    if is_terminal(state):
        return None, heuristic(state)
    
    max_child = None
    max_utility = -sys.maxsize
    generate_children(state,AI_PLAYER,verbose)

    for child in state.children:
        _, utility = minimize(child)
        if utility > max_utility:
            max_child = child
            max_utility = utility
    return max_child, max_utility

def minimize(state,verbose=False):
    if is_terminal(state):
        return None, heuristic(state)
    
    min_child = None
    min_utility = sys.maxsize
    generate_children(state,PLAYER,verbose)

    for child in state.children:
        _, utility = maximize(child)
        if utility < min_utility:
            min_child = child
            min_utility = utility
    
    return min_child, min_utility

def is_terminal(state):
    if 0 not in state.board[0] or state.level >= MAX_DEPTH:
        return True
    return False

def heuristic(state):
    # basic heuristic for now 
    if who_win(state) == 1:
        return 1000
    elif who_win(state) == 2:
        return -1000
    return random.randint(-100,100)

    # center = num_center(state.board)

def num_center(board):
    rows = board.shape[0]
    cols = board.shape[1]
    start_row = rows // 3
    end_row = rows - start_row
    start_col = cols // 3
    end_col = cols - start_col 
    center_elements = board[start_row:end_row, start_col:end_col]
    count_ones = np.count_nonzero(center_elements == 1)
    count_twos = np.count_nonzero(center_elements == 2)
    print(center_elements)
    print(count_ones)
    print(count_twos)
    return count_ones - count_twos


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

def who_win(state):
    '''
    Returns 1 if player 1 wins, 2 if player 2 wins, 0 if no one wins
    '''
    # Check horizontal
    for i in range(DIMENSIONS[0]):
        for j in range(DIMENSIONS[1]-3):
            condition_win = state.board[i][j] == state.board[i][j+1] == state.board[i][j+2] == state.board[i][j+3] == 1
            condition_lose = state.board[i][j] == state.board[i][j+1] == state.board[i][j+2] == state.board[i][j+3] == 2

            if condition_win:
                return 1
            elif condition_lose:
                return 2
            
    # Check vertical
    for i in range(DIMENSIONS[0]-3):
        for j in range(DIMENSIONS[1]):
            condition_win = state.board[i][j] == state.board[i+1][j] == state.board[i+2][j] == state.board[i+3][j] == 1
            condition_lose = state.board[i][j] == state.board[i+1][j] == state.board[i+2][j] == state.board[i+3][j] == 2

            if condition_win:
                return 1
            elif condition_lose:
                return 2
            
    # Check diagonal
    for i in range(DIMENSIONS[0]-3):
        for j in range(DIMENSIONS[1]-3):
            condition_win = state.board[i][j] == state.board[i+1][j+1] == state.board[i+2][j+2] == state.board[i+3][j+3] == 1
            condition_lose = state.board[i][j] == state.board[i+1][j+1] == state.board[i+2][j+2] == state.board[i+3][j+3] == 2
            if condition_win:
                return 1
            elif condition_lose:
                return 2
            
    # Check anti-diagonal
    for i in range(DIMENSIONS[0]-3):
        for j in range(3, DIMENSIONS[1]):
            condition_win = state.board[i][j] == state.board[i+1][j-1] == state.board[i+2][j-2] == state.board[i+3][j-3] == 1
            condition_lose = state.board[i][j] == state.board[i+1][j-1] == state.board[i+2][j-2] == state.board[i+3][j-3] == 2
            
            if condition_win:
                return 1
            elif condition_lose:
                return 2
    
    return 0

def input_array():
    array_4x4 = []
    for i in range(4):
        row = input(f"Enter 4 elements for row {i + 1} separated by spaces: ").split()
        
        # Check if the user entered exactly 4 elements
        if len(row) != 4:
            print("Please enter exactly 4 elements for each row.")
            break
        
        # Convert input elements to integers and append to the array
        row = [int(element) for element in row]
        array_4x4.append(row)
    
    array = np.array(array_4x4)

    return array



if __name__ == "__main__":
    # state.board = np.array([[1,0,0,0],
    #                         [1,1,0,0],
    #                         [1,2,1,0],
    #                         [2,2,0,0]])

    state = State()
    # while(1):
    #     # print(f"{state}")
    #     child = decision(state,verbose=False)
    #     if child is None:
    #         print("Game end")
    #         exit()
    #     print(child)
    #     print()

    #     array = input_array()
    #     # array = np.array([  [0,0,0,0],
    #     #                     [0,0,0,0],
    #     #                     [0,0,0,0],
    #     #                     [1,2,0,0]])
        
    #     print()
    #     time.sleep(0.25)
    #     state.board = np.copy(array)


    # To test generation
    # state.board[5][0] = 1
    # generate_children(state)
    # for child in state.children:
    #     print(child)


    # To test is_terminal
    # state.board = np.array([[1,1,1,1,1,1,1],
    #                         [1,1,1,1,1,1,1],
    #                         [1,1,1,1,1,1,1],
    #                         [1,1,1,1,1,1,1],
    #                         [1,1,1,1,1,1,1],
    #                         [1,1,1,1,1,1,1]])
    # res = is_terminal(state)
    # print(res)


    # To test who_win
    # state.board = np.array([[1,2,0,1],
    #                         [1,2,0,1],
    #                         [1,2,1,1],
    #                         [2,2,2,2]])
    # res = who_win(state)
    # print(res)

    # test num_center centering
    # state.board = np.array([[1,2,3,4,5,6,7],
    #                         [8,9,10,11,12,13,14],
    #                         [15,16,17,18,19,20,21],
    #                         [22,23,24,25,26,27,28],
    #                         [29,30,31,32,33,34,35],
    #                         [36,37,38,39,40,41,42]
    #                         ])
    # res= num_center(state.board)
    # print(res)
    # res =  # 17 18 19 # 24 25 26

    # test num_center counting
    # array = np.random.randint(0, 3, size=(6, 7))
    # print(array)
    # res= num_center(array)
    # print(res)


