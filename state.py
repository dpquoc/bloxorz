from map import Map


class State(Map):
    def __init__(self):
        super().__init__()
        self.target_block = - 1  # -1 : None , 0 : first block , 1 : second block
        # (first block pos , second block pos) : ((1,2),(3,4))
        self.blocks = (self.init_pos, self.init_pos)

    #"SPACE" action , no change in state
    def switch_target(self):
        if self.target_block == 0:
            self.target_block = 1
        elif self.target_block == 1:
            self.target_block = 0

    # return a next State() , do not update the self , action is "UP" , "DOWN" , "LEFT" , "RIGHT"
    def next_state(self, action):
        pass

    # return true if game not over , false if game over for the current state (self)
    def valid_state(self):
        pass

    # check if we triggered any type of button or join 2 block into 1 , if so update the state (self)
    def trigger(self):
        pass

    @staticmethod
    def repeated_state(state_log, new_state):
        for state in reversed(state_log):
            if new_state.matrix == state.matrix and new_state.blocks == state.blocks :
                return True
        return False
    
    #return all valid next state as much as possible : [("UP" , state1) ,("DOWN" , state2) ...]
    def next_valid_states(self , state_log ):
        res = []
        if self.target_block == -1:
            for action in ["UP" , "DOWN" , "LEFT" ,"RIGHT"]:
                new_state = self.next_state(action)
                if new_state.valid_state():
                    new_state.trigger()
                    if not new_state.repeated_state(state_log, new_state):
                        res.append((action,new_state))
        else:
            for target in ["" , "SPACE "]:
                for action in ["UP" , "DOWN" , "LEFT" ,"RIGHT"]:
                    new_state = self
                    if target == "SPACE " : 
                        new_state.switch_target()
                    new_state = new_state.next_state(action)
                    if new_state.valid_state():
                        new_state.trigger()
                        if not new_state.repeated_state(state_log, new_state):
                            res.append((target + action,new_state))
        return res