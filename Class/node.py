class Node():
    open_list = []
    close_list = []
    def __init__(self,state, parent=None, from_action=None, f = 0, g = 0, h = 0):
        self.state = state
        self.parent = parent
        self.from_action = from_action
        self.f = f
        self.g = g
        self.h = h
    
    def add_childs(self):
        child_states = self.state.next_valid_states()
        self.child_nodes = []
        for child in child_states:
            self.child_nodes.append(Node(child[1],self,child[0]))
        return self.child_nodes
    
    def get_action_list(self):
        if self.parent == None:
            return []
        res = self.parent.get_action_list()
        if "SPACE" in self.from_action:
            res.append(self.from_action.split(" ")[0])
            res.append(self.from_action.split(" ")[1])
            return res
        res.append(self.from_action)
        return res
    
    def repeated_node(self):
        for s in Node.close_list:
            if compare_matrix(self.state.matrix,s.state.matrix) and ( self.state.blocks == s.state.blocks or  self.state.blocks[-1::-1] == s.state.blocks):
                return True
        return False
    
    def get_node_status(self):
        # -1 : DEAD NODE (NOT GOAL AND NO CHILD)
        # 0 : NORMAL NODE (NOT GOAL AND WITH CHILD)
        # 1 : FINISH NODE (IS GOAL)
        if self.state.is_finished():
            return 1
        return 0

def compare_matrix(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False
    return True
