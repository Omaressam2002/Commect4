import sys
from minimax_nopruning import *

AI_PLAYER = 2
Player = 1

def expecti_maximize(state,visited,visited_nodes): 
    state_str = state.__str__()
    if state_str in visited_nodes:
        return None,visited[state_str] # should we return 

    # either the board is full or the level == k
    if is_terminal(state):
        hn = heuristic(state,AI_PLAYER)
        visited[state_str] = hn
        state.max = hn
        return None, hn
    
    max_child = None
    max_utility = -sys.maxsize
    
    children = generate_children(state,AI_PLAYER)

    # han add fen we ne update el weights fen??
    for i in range(len(children)):
        child , col = children[i]


        if col == 0 :
            _,u0 = expecti_minimize(children[i][0],visited,visited_nodes)
            if i != len(children)-1 and children[i+1][1] == 1: 
                _,u1 = expecti_minimize(children[i+1][0],visited,visited_nodes)
                utility = 0.4*u1 + 0.6*u0
            else :
                utility = u0
        elif col == 6:
            _,u6 = expecti_minimize(children[i][0],visited,visited_nodes)
            if i != 0 and children[i-1][1] == 5: 
                _,u5 = expecti_minimize(children[i-1][0],visited,visited_nodes)
                utility = 0.4*u5 + 0.6*u6
            else :
                utility = u6
        else :
            _,ui = expecti_minimize(children[i][0],visited,visited_nodes)
            ui1,ui2 = None , None
            if i != 0 and children[i-1][1] == col-1:
                _,ui1 = expecti_minimize(children[i-1][0],visited,visited_nodes)
            if i != len(children)-1 and children[i+1][1] == col+1:
                _,ui2 = expecti_minimize(children[i+1][0],visited,visited_nodes)
            
            if ui1 and ui2 : 
                utility = 0.2*ui1 + 0.6*ui + 0.2*ui2
            elif ui1 :
                utility = 0.4*ui1 + 0.6*ui
            elif ui2 :
                utility = 0.4*ui2 + 0.6*ui
            else :
                utility = ui


        if utility > max_utility:
            max_child = child
            max_utility = utility

    # for decision making
    state.max = max_utility
    state.max_child = max_child
    
    visited[state_str] = max_utility
    visited_nodes.add(state_str)
    return max_child, max_utility


def expecti_minimize(state,visited,visited_nodes):
    state_str = state.__str__()
    if state_str in visited_nodes:
        return state,visited[state_str]

    # either the board is full or the level == k
    if is_terminal(state):
        hn = heuristic(state,PLAYER)
        visited[state_str] = hn
        state.min = hn
        return None, hn

    min_child = None
    min_utility = sys.maxsize
    # hina raga3 tuple of (child,coll inserted) 
    children = generate_children(state,PLAYER)

    for i in range(len(children)):
        child , col = children[i]

        if col == 0 :
            _,u0 = expecti_maximize(children[i][0],visited,visited_nodes)
            if i != len(children)-1 and children[i+1][1] == 1: 
                _,u1 = expecti_maximize(children[i+1][0],visited,visited_nodes)
                utility = 0.4*u1 + 0.6*u0
            else :
                utility = u0
        elif col == 6:
            _,u6 = expecti_maximize(children[i][0],visited,visited_nodes)
            if i != 0 and children[i-1][1] == 5: 
                _,u5 = expecti_maximize(children[i-1][0],visited,visited_nodes)
                utility = 0.4*u5 + 0.6*u6
            else :
                utility = u6
        
        else :
            _,ui = expecti_maximize(children[i][0],visited,visited_nodes)
            ui1,ui2 = None , None
            if i != 0 and children[i-1][1] == col-1:
                _,ui1 = expecti_maximize(children[i-1][0],visited,visited_nodes)
            if i != len(children)-1 and children[i+1][1] == col+1:
                _,ui2 = expecti_maximize(children[i+1][0],visited,visited_nodes)
            
            if ui1 and ui2 : 
                utility = 0.2*ui1 + 0.6*ui + 0.2*ui2
            elif ui1 :
                utility = 0.4*ui1 + 0.6*ui
            elif ui2 :
                utility = 0.4*ui2 + 0.6*ui
            else :
                utility = ui
        

        if utility < min_utility:
            min_child = child
            min_utility = utility

    # for decision making
    # keep record of the minimum child
    state.min = min_utility
    state.min_child = min_child

    visited[state_str] = min_utility
    visited_nodes.add(state_str)
    return min_child, min_utility