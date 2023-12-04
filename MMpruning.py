import sys
from minimax_nopruning import *

AI_PLAYER = 2
Player = 1

def maximize_alpha_beta(state,visited,visited_nodes,alpha,beta):
    state_str = state.__str__()
    if state_str in visited_nodes:
        return state,visited[state_str],alpha,beta

    # either the board is full or the level == k
    if is_terminal(state):
        hn = heuristic(state,AI_PLAYER)
        visited[state_str] = hn
        state.max = hn
        return None, hn , alpha, beta
    
    max_child = None
    max_utility = -sys.maxsize
    
    generate_children(state,AI_PLAYER)

    # han add fen we ne update el weights fen??
    for child in state.children:
        _, utility , alpha , beta = minimize_alpha_beta(child,visited,visited_nodes,alpha,beta)
        if utility > max_utility:
            max_child = child
            max_utility = utility
        if max_utility >= beta:
            break
        if max_utility > alpha: 
            alpha = max_utility

    # for decision making
    state.max = max_utility
    state.max_child = max_child
    
    visited[state_str] = max_utility
    visited_nodes.add(state_str)
    return max_child, max_utility , alpha , beta


def minimize_alpha_beta(state,visited,visited_nodes,alpha,beta):
    state_str = state.__str__()
    if state_str in visited_nodes:
        return state,visited[state_str],alpha,beta

    # either the board is full or the level == k
    if is_terminal(state):
        hn = heuristic(state,PLAYER)
        visited[state_str] = hn
        state.min = hn
        return None, hn , alpha ,beta

    min_child = None
    min_utility = sys.maxsize
    
    generate_children(state,PLAYER)

    for child in state.children:
        _, utility , alpha , beta = maximize_alpha_beta(child,visited,visited_nodes,alpha,beta)
        if utility < min_utility:
            min_child = child
            min_utility = utility
        if min_utility <= alpha:
            break
        if min_utility < beta: 
            beta = min_utility
    # for decision making
    state.min = min_utility
    state.min_child = min_child

    visited[state_str] = min_utility
    visited_nodes.add(state_str)
    return min_child, min_utility, alpha , beta