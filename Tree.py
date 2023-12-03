class Tree:
    def __init__(self,root):
        self.root = root

    # bfs 
    def tree_traverse(self,root):
        current_level = 0
        queue = []
        queue.append(root)
        while len(queue) != 0:
            current = queue[0]
            
            if current.level != current_level:
                current_level = current.level
                print("\n")
            # visit
            print(current.board,current.max,current.min, end = "_____")
            for child in current.children:
                queue.append(child)
            queue.remove(queue[0])