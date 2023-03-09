class Node():
    def __init__(self,state, parent=None, from_action=None):
        self.state = state
        self.parent = parent
        self.from_action = from_action
    
    def get_state_log(self):
        if self.parent == None:
            return None
        res = self.parent.get_state_log()
        res.append(self.state)
        return res
    
    def add_childs(self):
        child_states = self.state.next_valid_states(self.get_state_log())
        child_nodes = []
        for child in child_states:
            child_nodes.append(Node(child[1],self,child[0]))
        return child_nodes
    
    def get_action_list(self):
        if self.parent == None:
            return None
        res = self.parent.get_action_list()
        if "SPACE" in self.from_action:
            res.append(self.from_action.split(" ")[0])
            res.append(self.from_action.split(" ")[1])
            return res
        res.append(self.from_action)
        return res