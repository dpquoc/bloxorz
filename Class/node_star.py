from Class.node import Node

class NodeStar(Node):
    def __init__(self, state, parent=None, from_action=None):
        super().__init__(state, parent, from_action)
        if parent == None:
            self.g = 0
        else:
            self.g = self.parent.g + 1
            
        x1,y1 = self.state.blocks[0]
        x2,y2 = self.state.blocks[1]
        xg,yg = self.state.finish
        
        # Chebyshev distance
        h1 = max((x1-xg),(y1-yg))
        h2 = max((x2-xg),(y2-yg))
        self.h = max(h1,h2)
        
        self.f = self.g + self.h
        
    def repeated_node(self):
        for s in NodeStar.close_list:
            if compare_matrix(self.state.matrix,s.state.matrix) and (self.state.blocks == s.state.blocks or self.state.blocks[-1::-1] == s.state.blocks):
                if self.f < s.f:
                    s.parent = self.parent
                    s.from_action = self.from_action
                    s.g = self.g
                    s.h = self.h
                    s.f = self.f
                    return 1
                return 2
        return 3
    
    def add_childs(self):
        child_states = self.state.next_valid_states()
        self.child_nodes = []
        for child in child_states:
            self.child_nodes.append(NodeStar(child[1],self,child[0]))
        return self.child_nodes
        
        
        
def compare_matrix(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False
    return True
