import random
import math
from Class.state import State

# Số lần thực hiện vòng lặp MCTS
ITERATIONLIMIT = 10000

def compare_matrix(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False
    return True

class MCTSNode:
    # Visited node là những node đã simulation. Root sẽ được tính là visited mà không cần simulation.
    visited_node = []
    def __init__(self, state: State, parent=None, from_action=None):
        self.state = state
        self.parent = parent
        self.from_action = from_action
        self.childrens = []
        # reward và visit sẽ dùng trong công thức UCB để tính toán giá trị dùng để chọn
        # best child node
        self.reward = 0.0
        self.visits = 0
        self.countSimulation = 0
        self.is_closed = False

        if parent == None:
            self.g = 0
        else:
            self.g = self.parent.g + 1
            
        x1,y1 = self.state.blocks[0]
        x2,y2 = self.state.blocks[1]
        xg,yg = self.state.finish
        
        
        # Simple Chebyshev distance to goal
        h1 = max((x1-xg),(y1-yg))
        h2 = max((x2-xg),(y2-yg))
        self.h = max(h1,h2)
        
        self.f = self.g + self.h

    # Lấy ra danh sách những node có thể được expand bởi node hiện tại
    # Những node cho phép phải:
    # - Không phải game over
    # - Không phải node đã có trong cây
    def get_possible_next_node(self):
        possible_next_node = []
        temp = self.state.next_valid_states()

        for i in range(len(temp)):
            node = MCTSNode(temp[i][1], self, temp[i][0])
            if not node.repeated_node():
                possible_next_node.append(node)
        
        return possible_next_node


    # Check có phải leaf node không
    def is_leaf_node(self):
        if self.childrens == []:
            return True
        return False


    # Node terminal là node không thể expand thêm child node nữa, cũng như là node lá
    def is_terminal(self):
        if (self.childrens == []) and (self.get_possible_next_node() == []):
            return True
        return False


    def repeated_node(self):
        for s in MCTSNode.visited_node:
            if compare_matrix(self.state.matrix,s.state.matrix) and ( self.state.blocks == s.state.blocks or  self.state.blocks[-1::-1] == s.state.blocks):
                return True                
        return False


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
    

# Selection: chọn ra node để thực hiện expand. Chọn node lá để expand
def selection(node: MCTSNode):
    while not node.is_leaf_node() and not node.is_closed:
        node = get_best_child(node)
    return expand(node)


# Expand: Thêm node mới vào cây. Với mỗi action cho ra state hợp lệ
# sẽ thêm node mới với state đó vào cây.
# Trả về node con đầu tiên. Nếu không thể expand nữa trả về chính nó.
def expand(node: MCTSNode):
    possible_child_node = node.get_possible_next_node()
    if possible_child_node != []:
        for child_node in possible_child_node:
            node.childrens.append(child_node)
        return node.childrens[0]
    else:
        return node


# Dùng công thức UCB để tính giá trị của các node con. Chọn ra node có giá trị cao nhất.
# Nếu có nhiều hơn 1 bestchild chọn ngẫu nhiên.
def get_best_child(node: MCTSNode):
    scalar = 2
    bestscore = -99999
    bestchildren = []
    all_score = []

    count_is_closed = 0
    for c in node.childrens:
        if c.visits == 0:
            return c
        if c.is_closed:
            count_is_closed += 1
            continue
        exploit = c.reward / c.visits	
        explore = math.sqrt(math.log(node.visits)/float(c.visits))	
        score = exploit + scalar * explore
        all_score.append(score)
        if score == bestscore:
            bestchildren.append(c)
        if score > bestscore:
            bestchildren = [c]
            bestscore = score

    if count_is_closed == len(node.childrens):
        node.is_closed = True
        return node
    return random.choice(bestchildren)
        

# Simulation: thực hiện chọn ngẫu nhiên 1 possible_next_node. Sau đó di chuyển xuống node đã chọn.
# Thực hiện cho đến khi gặp terminal node. Sau đó tính toán reward rồi trả về reward.
# Nếu trong khi đang simulation mà gặp finish node trả về finish node luôn.
def simulation(node: MCTSNode, i):
    # Trường hợp này xảy ra khi phát hiện một node có tất cả các con đều đã close
    if node.is_closed:
        return -100     # Need consider
    
    MCTSNode.visited_node.append(node)
    node.countSimulation += 1
    depth_of_simulation = 0
    #max_depth = 7
    max_depth = 4

    while depth_of_simulation < max_depth:
        if node.state.is_finished():
            return node
        if not node.is_terminal():
            temp = node.get_possible_next_node()
            node = random.choice(temp)
            depth_of_simulation += 1
        else:
            break
    
    if node.state.is_finished():
        return node

    if depth_of_simulation == 0:
        node.is_closed = True
        return -100 # Need consider

    # Tính điểm cho simulation
    score = 0

    if node.is_terminal() == False:
        score += 100
    score -= node.f

    count = 0
    while (node != None):
        node = node.parent
        count += 1
    print(i, depth_of_simulation, count)
    return score


# Backpropagate kết quả thu được từ simulation lên trở lại đến root.
# Mỗi node trên backpropagation path sẽ được cộng thêm reward và visit cộng 1
def backpropagate(node: MCTSNode, reward):
    while node != None:
        node.reward += reward
        node.visits += 1
        node = node.parent
    

def MCTS(state: State):
    root = MCTSNode(state)
    MCTSNode.visited_node.append(root)
    for i in range(ITERATIONLIMIT):
        node = selection(root)
        reward = simulation(node, i)
        if type(reward) == float or type(reward) == int:
            backpropagate(node, reward)
        else:
            action_list = reward.get_action_list()
            return action_list

    return ["OUT OF TIME"]
    