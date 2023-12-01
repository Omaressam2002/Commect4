import tkinter as tk

# Define the tree structure
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H', 'I'],
    'E': [],
    'F': [],
    'G': ['J', 'K'],
    'H': [],
    'I': [],
    'J': [],
    'K': []
}

# Initialize the tkinter window
window = tk.Tk()
window.title("Minimax Search Tree Visualization")

# Create a canvas to draw the tree
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()

# Define the coordinates of the root node
root_x = 400
root_y = 50

# Define the spacing between nodes
level_spacing = 100
sibling_spacing = 50

# Define the radius of the nodes
node_radius = 20

# Define the function to draw the tree
def draw_tree(node, x, y, level):
    # Draw the current node
    canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill='lightblue')
    canvas.create_text(x, y, text=node)

    # Calculate the x-coordinate of the first child node
    first_child_x = x - (level_spacing * (len(tree[node]) - 1) / 2)

    # Draw the child nodes recursively
    for i, child in enumerate(tree[node]):
        child_x = first_child_x + i * level_spacing
        child_y = y + level_spacing
        canvas.create_line(x, y + node_radius, child_x, child_y - node_radius, width=2, fill='gray')
        draw_tree(child, child_x, child_y, level + 1)

# Draw the tree starting from the root node
draw_tree('A', root_x, root_y, 0)

# Start the tkinter event loop
window.mainloop()