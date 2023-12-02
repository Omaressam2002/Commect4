import networkx as nx
import matplotlib.pyplot as plt

# Function to create the game tree
def create_game_tree(board, depth, maximizing_player):
    if depth == 0:
        return None

    G = nx.Graph()

    # Generate all possible moves for the current board state
    possible_moves = get_possible_moves(board)

    for move in possible_moves:
        new_board = make_move(board, move, maximizing_player)
        child_node = create_game_tree(new_board, depth - 1, not maximizing_player)

        if child_node is not None:
            G.add_edge(board_to_string(board), board_to_string(new_board))

    return G

# Function to get all possible moves for a given board state
def get_possible_moves(board):
    moves = []
    for col in range(7):
        if board[0][col] == 0:
            moves.append(col)
    return moves

# Function to make a move on the board
def make_move(board, col, maximizing_player):
    new_board = [row[:] for row in board]
    for row in range(5, -1, -1):
        if new_board[row][col] == 0:
            new_board[row][col] = 1 if maximizing_player else 2
            break
    return new_board

# Function to convert the board to a string representation
def board_to_string(board):
    return ''.join(str(cell) for row in board for cell in row)

# Function to visualize the game tree
def visualize_game_tree(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=1000, font_size=10)
    plt.show()

# Example usage
board = [[0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [1, 2, 0, 0, 1, 0, 0]]

depth = 7
maximizing_player = True

game_tree = create_game_tree(board, depth, maximizing_player)
visualize_game_tree(game_tree)