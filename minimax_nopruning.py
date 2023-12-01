import numpy as np
import sys

DIMENSIONS = (6,7)
MAX_DEPTH = 5

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

def decision(state):
    child,_ = maximize(state)

    return child

def maximize(state):
    if is_terminal(state):
        return None, heuristic(state)
    
    max_child = None
    max_utility = -sys.maxsize
    generate_children(state)

    for child in state.children:
        _, utility = minimize(child)
        if utility > max_utility:
            max_child = child
            max_utility = utility
    
    return max_child, max_utility

def minimize(state):
    if is_terminal(state):
        return None, heuristic(state)
    
    min_child = None
    min_utility = sys.maxsize
    generate_children(state)

    for child in state.children:
        _, utility = maximize(child)
        if utility < min_utility:
            min_child = child
            min_utility = utility
    
    return min_child, min_utility

def is_terminal(state):
    if 0 not in state.board or state.level >= MAX_DEPTH:
        return True
    return False

def heuristic(state):
    return 1

def generate_children(state):
    for j in range(DIMENSIONS[1]):
        for i in range(DIMENSIONS[0]-1 , -1, -1):
            if state.board[i][j] == 0:
                child = State()
                child.board = np.copy(state.board)
                child.board[i][j] = 1
                print(child)
                child.setParent(state)
                break


state = State()
decision(state)

# To test generation
# state.board[5][0] = 1
# generate_children(state)
# for child in state.children:
#     print(child)



# To test is_terminal
# state.board = np.array([[1,1,1,1,1,1,1],
#                         [1,1,1,1,1,1,1],
#                         [1,1,1,0,1,1,1],
#                         [1,1,1,1,1,1,1],
#                         [1,1,1,1,1,1,1],
#                         [1,1,1,1,1,1,1]])
# res = is_terminal(state)
# print(res)