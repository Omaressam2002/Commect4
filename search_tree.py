import tkinter as tk

class TreeVisualizationGUI:
    def __init__(self, tree):
        self.tree = tree
        self.window = tk.Tk()
        self.window.title("Tree Visualization")
        
        # Create a frame to hold the canvas and scrollbars
        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas with scrollbars
        self.canvas = tk.Canvas(frame, width=800, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        x_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        x_scrollbar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=x_scrollbar.set)

        y_scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        y_scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=y_scrollbar.set)

        self.node_width = 100
        self.node_height = 50
        self.x_space = 200  # Increased horizontal padding
        self.y_space = 50

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_tree(self):
        self._draw_node(self.tree, 400, 50)

    def _draw_node(self, node, x, y, parent_x=None, parent_y=None):
        board, minimax_value = node.data
        board_str = '\n'.join(' '.join(str(cell) for cell in row) for row in board)
        node_text = f"Minimax: {minimax_value}\n\n{board_str}"
        self.canvas.create_rectangle(x - self.node_width // 2, y - self.node_height // 2,
                                     x + self.node_width // 2, y + self.node_height // 2,
                                     fill='lightblue', outline='black')
        self.canvas.create_text(x, y, text=node_text, width=self.node_width - 10, justify=tk.CENTER)
        
        if parent_x is not None and parent_y is not None:
            self.canvas.create_line(parent_x, parent_y + self.node_height // 2, x, y - self.node_height // 2)
        
        if node.children:
            child_count = len(node.children)
            x_offset = self.x_space * (child_count - 1) // 2 
            y_offset = self.y_space
            for i, child in enumerate(node.children):
                child_x = x - x_offset + i * self.x_space 
                child_y = y + y_offset + 100
                self._draw_node(child, child_x, child_y, x, y)

    def run(self):
        self.window.mainloop()

# Example usage
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

root_node = TreeNode(([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 10))
child1 = TreeNode(([[9, 8, 7], [6, 5, 4], [3, 2, 1]], 5))
child2 = TreeNode(([[0, 1, 0], [0, 1, 0], [0, 1, 0]], -3))
child3 = TreeNode(([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 8))
child4 = TreeNode(([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 8))
child5 = TreeNode(([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 8))
child6 = TreeNode(([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 8))
child7 = TreeNode(([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 8))
child8 = TreeNode(([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 8))
child9 = TreeNode(([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 8))
child10 = TreeNode(([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 8))
child11 = TreeNode(([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 8))
child12 = TreeNode(([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 8))

root_node.children = [child1, child2, child3]
child1.children = [child4, child5, child6]
child2.children = [child7, child8, child9]
child3.children = [child10, child11, child12]

gui = TreeVisualizationGUI(root_node)
gui.draw_tree()
gui.run()