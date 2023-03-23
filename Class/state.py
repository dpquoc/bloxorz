from Class.map import Map
#from map import Map
import copy



class State(Map):
    def __init__(self,stageInfo):
        super().__init__(stageInfo)
        self.target_block = -1  # -1 : None , 0 : first block , 1 : second block
        # (first block pos , second block pos) : [(1,2),(3,4)]
        self.blocks = [self.init_pos, self.init_pos]

    #"SPACE" action , no change in state
    def switch_target(self):
        if self.target_block == 0:
            self.target_block = 1
        elif self.target_block == 1:
            self.target_block = 0

    # return a next State() , do not update the self , action is "UP" , "DOWN" , "LEFT" , "RIGHT"
    def next_state(self, action):
        next_state = copy.deepcopy(self)
        action_dict = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }
        dx, dy = action_dict[action]
        x0, y0 = next_state.blocks[0]
        x1, y1 = next_state.blocks[1]

        # Update the coordinates of the target block
        if next_state.target_block == -1:
            
            if x0 == x1 and y0 == y1: # standing
                if action == "UP":
                    next_state.blocks[0] = (x0 - 1, y0)
                    next_state.blocks[1] = (x1 - 2, y1)
                elif action == "DOWN":
                    next_state.blocks[0] = (x0 + 1, y0)
                    next_state.blocks[1] = (x1 + 2, y1)
                elif action == "RIGHT":
                    next_state.blocks[0] = (x0, y0 + 1)
                    next_state.blocks[1] = (x1, y1 + 2)
                elif action == "LEFT":
                    next_state.blocks[0] = (x0, y0 - 1)
                    next_state.blocks[1] = (x1, y1 - 2)
                
            elif y0 == y1: # lying vertical  : X-AXIS
                if action == "UP":
                    if next_state.blocks[0][0] < next_state.blocks[1][0]:
                        next_state.blocks[0] = (x0 - 1, y0)
                        next_state.blocks[1] = (x1 - 2, y1)
                    else:
                        next_state.blocks[0] = (x0 - 2, y0)
                        next_state.blocks[1] = (x1 - 1, y1)
                elif action == "DOWN":
                    if next_state.blocks[0][0] > next_state.blocks[1][0]:
                        next_state.blocks[0] = (x0 + 1, y0)
                        next_state.blocks[1] = (x1 + 2, y1)
                    else:
                        next_state.blocks[0] = (x0 + 2, y0)
                        next_state.blocks[1] = (x1 + 1, y1)
                elif action == "RIGHT":
                    next_state.blocks[0] = (x0, y0 + 1)
                    next_state.blocks[1] = (x1, y1 + 1)
                elif action == "LEFT":
                    next_state.blocks[0] = (x0, y0 - 1)
                    next_state.blocks[1] = (x1, y1 - 1)
                
            elif x0 == x1 : # lying horizontal   : Y-AXIS
                if action == "RIGHT":
                    if next_state.blocks[0][1] > next_state.blocks[1][1]:
                        next_state.blocks[0] = (x0, y0 + 1)
                        next_state.blocks[1] = (x1, y1 + 2)
                    else:
                        next_state.blocks[0] = (x0, y0 + 2)
                        next_state.blocks[1] = (x1, y1 + 1)
                elif action == "LEFT":
                    if next_state.blocks[0][1] < next_state.blocks[1][1]:
                        next_state.blocks[0] = (x0, y0 - 1)
                        next_state.blocks[1] = (x1, y1 - 2)
                    else:
                        next_state.blocks[0] = (x0, y0 - 2)
                        next_state.blocks[1] = (x1, y1 - 1)
                elif action == "UP":
                    next_state.blocks[0] = (x0 - 1, y0)
                    next_state.blocks[1] = (x1 - 1, y1)
                elif action == "DOWN":
                    next_state.blocks[0] = (x0 + 1, y0)
                    next_state.blocks[1] = (x1 + 1, y1)
            
        else:
            x, y = next_state.blocks[next_state.target_block]
            next_state.blocks[next_state.target_block] = (x + dx, y + dy)
            
        return next_state

    # return true if game not over , false if game over for the current state (self)
    def valid_state(self):
        x0, y0 = self.blocks[0]
        x1, y1 = self.blocks[1]
        if self.matrix[x0][y0] == 0 or self.matrix[x1][y1] == 0:
            return False
        if self.blocks[0] == self.blocks[1] and self.matrix[x0][y0] == 3:
            return False
        return True
        

    # check if we triggered any type of button or join 2 block into 1 , if so update the state (self)
    def trigger(self):
        x0, y0 = self.blocks[0]
        x1, y1 = self.blocks[1]
        
        if self.blocks[0] == self.blocks[1] :
            if self.matrix[x0][y0] == 4 or self.matrix[x0][y0] == 5:
                self.buttons[(x0,y0)].trigger(self.matrix)
            elif self.matrix[x0][y0] == 6 :
                self.blocks[0] = self.buttons[(x0,y0)].block1
                self.blocks[1] = self.buttons[(x0,y0)].block2
                if self.blocks[0] == self.buttons[(x0,y0)].target:
                    self.target_block = 0
                else:
                    self.target_block = 1
        else:
            if self.matrix[x0][y0] == 4:
                self.buttons[(x0,y0)].trigger(self.matrix)
            if self.matrix[x1][y1] == 4:
                self.buttons[(x1,y1)].trigger(self.matrix)
                
            if self.target_block != -1 and abs(x0-x1) + abs(y0-y1) == 1:
                self.target_block = -1
            
                        

    
    def is_finished(self):
        if self.blocks[0] == self.blocks[1] and self.blocks[0] == self.finish :
            return True
        return False
    
    #return all valid next state as much as possible : 
    # [("UP" , state1) ,("DOWN" , state2), ("SPACE LEFT" , state3) ...]
    # IMPORTANT!!! This function will NOT ADD change any close_list and open_list, 
    # So pls make sure you can control the open and close list your own
    def next_valid_states(self):
        res = []
        # State.close_list.append(self)
        
        if self.target_block == -1:
            for action in ["UP" , "DOWN" , "LEFT" ,"RIGHT"]:
                new_state = self.next_state(action)
                if new_state.valid_state():
                    new_state.trigger()
                    
                    # if not new_state.repeated_state():
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
                        # if not new_state.repeated_state():
                        res.append((target + action,new_state))
        return res

