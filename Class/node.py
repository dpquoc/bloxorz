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
        self.child_nodes = []
        for child in child_states:
            self.child_nodes.append(Node(child[1],self,child[0]))
        return self.child_nodes
    
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
    
    def get_node_status(self):
        # -1 : DEAD NODE (NOT GOAL AND NO CHILD)
        # 0 : NORMAL NODE (NOT GOAL AND WITH CHILD)
        # 1 : FINISH NODE (IS GOAL)
        if self.state.is_finished():
            return 1
        if len(self.child_nodes) == 0:
            return -1
        return 0
        