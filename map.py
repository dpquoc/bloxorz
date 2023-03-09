class O:
    type = 4
    def __init__(self, pos, targets):
        self.pos = pos
        self.targets = targets
        
class X:
    type = 5
    # example : pos = (1,2)  , targets = [ (1,1),(1,2),(1,3) ]
    def __init__(self, pos, targets):
        self.pos = pos
        self.targets = targets

class Split:
    type = 6
    def __init__(self, pos, block1, block2, target):
        self.pos = pos
        self.block1 = block1
        self.block2 = block2
        self.target = target
    
    
    
class Map:
    def __init__(self , stageInfo):
        with open(stageInfo, 'r') as f:
            first_line = int(f.readline().strip())
            first_line = [int(x) for x in first_line.split(" ")]
            n = first_line[0]
            
            self.init_pos = (first_line[1],first_line[2])
            
            matrix = [f.readline().strip() for _ in range(n)]
            self.matrix = [list(map(int, row.split(" "))) for row in matrix]
            
            for i in range(matrix):
                for j in range(matrix[0]):
                    if matrix[i][j] == 2:
                        self.finish = (i,j)
            
            self.buttons = {}
            buttons = [line.strip() for line in f]
            for button in buttons:
                x_pos = button[1]
                y_pos = button[2]
                button = [int(x) for x in button.split(" ")]
                if button[0] == 4:
                    targets = []
                    
                    for i in range (3, len(button) , 2):
                        targets.append((button[i], button[i+1]))
                        
                    x_button = X((x_pos,y_pos), targets)
                    self.buttons[x_button.pos] = x_button
                    
                elif button[0] == 5:
                    targets = []
                    
                    for i in range (3, len(button) , 2):
                        targets.append((button[i], button[i+1]))
                        
                    o_button = X((x_pos,y_pos), targets)
                    self.buttons[o_button.pos] = o_button
                    
                elif button[0] == 6:
                    split_button = Split( (button[1],button[2]), (button[3],button[4]), (button[5],button[6]), (button[7],button[8]))
                    self.buttons[split_button.pos] = split_button
            
            