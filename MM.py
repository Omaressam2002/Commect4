import sys
from minimax_nopruning import *

AI_PLAYER = 2
Player = 1

def maximize(state,visited,visited_nodes):
    state_str = state.__str__()
    if state_str in visited_nodes:
        return state,visited[state_str]

    # either the board is full or the level == k
    if is_terminal(state):
        hn = heuristic(state,AI_PLAYER)
        visited[state_str] = hn
        return state, hn
    
    max_child = None
    max_utility = -sys.maxsize
    
    generate_children(state,AI_PLAYER)

    # han add fen we ne update el weights fen??
    for child in state.children:
        _, utility = minimize(child,visited,visited_nodes)
        if utility > max_utility:
            max_child = child
            max_utility = utility
    
    state.max_utility = max_utility
    state.max_child = max_child

    visited[state_str] = max_utility
    visited_nodes.add(state_str)
    return max_child, max_utility


def minimize(state,visited,visited_nodes):
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
        _, utility = maximize(child,visited,visited_nodes)
        if utility < min_utility:
            min_child = child
            min_utility = utility

    state.min = min_utility
    state.min_child = min_child

    visited[state_str] = min_utility
    visited_nodes.add(state)
    return min_child, min_utility

