import tkinter as tk

class TreeVisualizationGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tree Visualization")

        frame = tk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True)

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

        # Zooming
        self.zoom_level = 1.0
        zoom_frame = tk.Frame(self.window)
        zoom_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        zoom_in_button = tk.Button(
            zoom_frame, text="Zoom In", command=self.zoom_in
        )
        zoom_in_button.pack(pady=5)

        zoom_out_button = tk.Button(
            zoom_frame, text="Zoom Out", command=self.zoom_out
        )
        zoom_out_button.pack(pady=5)

        self.node_width = 100
        self.node_height = 150
        self.x_space = 400
        self.y_space = 300

        # Dictionary to store line items associated with edges
        self.edge_lines = {}

    def zoom_in(self):
        self.zoom(1.1)

    def zoom_out(self):
        self.zoom(0.9)

    def zoom(self, scale):
        # Calculate the new zoom level
        new_zoom_level = self.zoom_level * scale
        scaling_factor = new_zoom_level / self.zoom_level
        self.zoom_level = new_zoom_level

        # Scale the canvas to reflect the new zoom level
        self.canvas.scale("all", 0, 0, scaling_factor, scaling_factor)

        # Update the scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_tree(self, root):
        self.root = root
        self._draw_node(root, 400, 50)

    def _draw_node(self, node, x, y, parent_x=None, parent_y=None, max=True):
        board = node.board

        board_str = '\n'.join(' '.join(str(cell) for cell in row) for row in board)
        node_text = f"Max: {node.max}\nMin: {node.min}\n\n{board_str}"

        node_compound = f"node_{id(node)}"  # Unique tag for each node for dragging

        if max:
            node_shape = [
                x, y - self.node_height // 2 - 50,
                x - self.node_width // 2 - 50, y + self.node_height // 2,
                x + self.node_width // 2 + 50, y + self.node_height // 2
            ]
        else:
            node_shape = [
                x, y + self.node_height // 2 + 50,
                x - self.node_width // 2 - 50, y - self.node_height // 2,
                x + self.node_width // 2 + 50, y - self.node_height // 2
            ]

        self.canvas.create_polygon(
            node_shape,
            fill='#E10C22', outline='black', tags=node_compound
        )
        self.canvas.create_text(
            x, y, text=node_text, width=self.node_width - 10,
            justify=tk.CENTER, tags=node_compound
        )

        if parent_x is not None and parent_y is not None:
            if not max:
                line = self.canvas.create_line(
                    parent_x, parent_y + self.node_height // 2,
                    x, y - self.node_height // 2, tags=(node_compound, "edge_line")
                )
            else:
                line = self.canvas.create_line(
                    parent_x, parent_y + self.node_height // 2 + 50,
                    x, y - self.node_height // 2 - 50, tags=(node_compound, "edge_line")
                )
            self.edge_lines[node_compound] = line  # Store the line object with the node_compound tag as the key
            print(f"Parent: ({parent_x}, {parent_y}) -> Child: ({x}, {y})")

            # Bind events for dragging
            self.canvas.tag_bind(node_compound, "<ButtonPress-1>",
                                lambda event, item=node_compound, x=x, y=y: self.on_press(event, item, x, y))
            self.canvas.tag_bind(node_compound, "<B1-Motion>",
                                lambda event, item=node_compound, x=x, y=y: self.on_drag(event, item, x, y))
            self.canvas.tag_bind(node_compound, "<ButtonRelease-1>", self.on_release)

        if node.children:
            child_count = len(node.children)
            x_offset = self.x_space * (child_count - 1) // 2
            y_offset = self.y_space
            for i, child in enumerate(node.children):
                child_x = x - x_offset + i * self.x_space
                if max:
                    child_y = y + y_offset
                else:
                    child_y = y + y_offset + 100
                self._draw_node(child, child_x, child_y, x, y, not max)

    def on_press(self, event, item, parent_x, parent_y):
        self.drag_data = {"item": item, "x": event.x, "y": event.y,
                        "initial_coords": self.canvas.coords(item),
                        "parent_coords": (parent_x, parent_y),
                        "offset": (event.x - self.canvas.coords(item)[0], event.y - self.canvas.coords(item)[1])}

    def on_drag(self, event, item, parent_x, parent_y):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]

        # Move the entire compound item
        self.canvas.move(item, delta_x, delta_y)

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

        dragged_item = self.drag_data["item"]
        dragged_x, dragged_y, _, _ = self.canvas.coords(dragged_item)

        for child_tag, line_coords in self.edge_lines.items():
            original_parent_x, original_parent_y, original_child_x, original_child_y = line_coords
            original_line = self.canvas.find_withtag(child_tag)

            if original_line:
                # Calculate the new child coordinates based on the difference between dragged coordinates and initial coordinates
                new_child_x = original_child_x + (dragged_x - self.drag_data["initial_coords"][0])
                new_child_y = original_child_y + (dragged_y - self.drag_data["initial_coords"][1])

                # Update the coordinates of the line
                self.canvas.coords(original_line,
                                dragged_x, dragged_y + self.node_height // 2,
                                new_child_x, new_child_y - self.node_height // 2
                                )

                # Update the stored line coordinates in the edge_lines dictionary
                self.edge_lines[child_tag] = (dragged_x, dragged_y, new_child_x, new_child_y)

                # If the child has children, update their edges
                self._update_child_edges(child_tag, new_child_x, new_child_y, dragged_x, dragged_y)

    def _update_child_edges(self, parent_tag, new_parent_x, new_parent_y, dragged_x, dragged_y):
        # Update the edges of the children of the given parent tag
        for child_tag, line_coords in self.edge_lines.items():
            _, _, original_child_x, original_child_y = line_coords

            # Check if the child is a child of the given parent
            if child_tag.startswith(f"{parent_tag}_child"):
                # Calculate the new child coordinates based on the difference between dragged coordinates and initial coordinates
                new_child_x = original_child_x + (dragged_x - self.drag_data["initial_coords"][0])
                new_child_y = original_child_y + (dragged_y - self.drag_data["initial_coords"][1])

                # Update the coordinates of the line
                self.canvas.coords(self.edge_lines[child_tag],
                                dragged_x, dragged_y + self.node_height // 2,
                                new_child_x, new_child_y - self.node_height // 2
                                )

                # Update the stored line coordinates in the edge_lines dictionary
                self.edge_lines[child_tag] = (dragged_x, dragged_y, new_child_x, new_child_y)

    def on_release(self, event):
        # Clear the drag_data
        self.drag_data = {}

    def run(self):
        self.window.mainloop()