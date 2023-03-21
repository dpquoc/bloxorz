class O:
    # type = 4
    def __init__(self, pos, targets, switch = 0):
        self.pos = pos
        self.targets = targets
        self.switch = switch
        
    def trigger(self,matrix):
        # CAUTION HERE
        for target in self.targets:
            (x,y) ,s = target
            if s == 0:
                matrix[x][y] = 1 - matrix[x][y]
            elif s == 1:
                matrix[x][y] = 1
            elif s == -1:
                matrix[x][y] = 0
        
class X:
    # type = 5
    # example : pos = (1,2)  , targets = [ ((1,1),0),((1,2),1),((1,3),-1) ]
    # switch = 0 (Swap targets ON/OFF) , = 1 (always ON) , = -1 ( always OFF)
    def __init__(self, pos, targets, switch = 0):
        self.pos = pos
        self.targets = targets
        self.switch = switch
    def trigger(self,matrix):
        for target in self.targets:
            (x,y) ,s = target
            if s == 0:
                matrix[x][y] = 1 - matrix[x][y]
            elif s == 1:
                matrix[x][y] = 1
            elif s == -1:
                matrix[x][y] = 0

class Split:
    # type = 6
    def __init__(self, pos, block1, block2, target):
        self.pos = pos
        self.block1 = block1
        self.block2 = block2
        self.target = target
    
    
    
class Map:
    def __init__(self , stageInfo):
        with open(stageInfo, 'r') as f:
            first_line = f.readline().strip()
            first_line = [int(x) for x in first_line.split(" ")]
            n = first_line[0]
            
            self.init_pos = (first_line[1],first_line[2])
            
            matrix = [f.readline().strip() for _ in range(n)]
            self.matrix = [list(map(int, row.split(" "))) for row in matrix]
            
            for i, row in enumerate(self.matrix):
                for j, element in enumerate(row):
                    if element == 2:
                        self.finish = (i,j)
                        break
            
            self.buttons = {}
            buttons = [line.strip() for line in f]
            for button in buttons:
                button = [int(x) for x in button.split(" ")]
                x_pos = button[0]
                y_pos = button[1]
                type_button = self.matrix[button[0]][button[1]]
                if type_button == 4:
                    targets = []
                    
                    for i in range (2, len(button) , 3):
                        targets.append(((button[i], button[i+1]) , button[i+2]))
                        
                    o_button = O((x_pos,y_pos), targets)
                    self.buttons[o_button.pos] = o_button
                    
                elif type_button == 5:
                    targets = []
                    
                    for i in range (2, len(button) , 3):
                        targets.append(((button[i], button[i+1]) , button[i+2]))
                        
                    x_button = X((x_pos,y_pos), targets)
                    self.buttons[x_button.pos] = x_button
                    
                elif type_button == 6:
                    split_button = Split( (button[0],button[1]), (button[2],button[3]), (button[4],button[5]), (button[6],button[7]))
                    self.buttons[split_button.pos] = split_button
            print(self.buttons)