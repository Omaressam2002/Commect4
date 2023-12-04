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
                tree.create_node(root.__str__(),root.__str__())
            elif current.__str__() not in visited :
                tree.create_node(current.__str__(),current.__str__(),parent = current.parent.__str__())
            
            visited.add(current.__str__())
        tree.show()
            