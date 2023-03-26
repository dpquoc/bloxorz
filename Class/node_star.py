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
        
        
        # Simple Chebyshev distance to goal
        h1 = max(abs(x1-xg),abs(y1-yg))
        h2 = max(abs(x2-xg),abs(y2-yg))
        self.h = max(h1,h2)
        
        # # This is just experiment
        # # Chebyshev distance to nearest not-yet activated button
        # for pos_button , button in self.state.buttons.items() :
        #     if button.count > 0:
        #         continue
        #     xb , yb = pos_button
        #     h1 = max(abs(x1-xb),abs(y1-yb))
        #     h2 = max(abs(x2-xb),abs(y2-yb))
        #     nearest_button = max(h1,h2)
        #     self.h = min(self.h,nearest_button)
            
            
        
        self.f = self.g + self.h
        
    def __lt__(self, other):
        return True
        
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
