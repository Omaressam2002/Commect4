from treelib import Node,Tree
class MMTree:
    def __init__(self,root):
        self.root = root
    # bfs 
    def tree_traverse(self,root):
        tree = Tree()
        current_level = 0
        queue = []
        visited = set()
        queue.append(root)
        while len(queue) != 0:
            current = queue[0]
            queue.remove(current)
            for child in current.children:
                queue.append(child)
            if current.parent == None:
                tree.create_node(root.T(),root.T())
            elif current.T() not in visited :
                tree.create_node(current.T(),current.T(),parent = current.parent.T())
            
            visited.add(current.T())
        tree.show()
            