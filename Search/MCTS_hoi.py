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

def compare_node(node1, node2):
    if compare_matrix(node1.state.matrix,node2.state.matrix) and ( node1.state.blocks == node2.state.blocks or  node1.state.blocks[-1::-1] == node2.state.blocks):
        return True    
    return False

class MCTSNode:
    # Visited node là những node đã simulation. Root sẽ được tính là visited mà không cần simulation.
    visited_node = []
    root = None
    init_start_to_finish_dist = 0
    best_distance = 99999
    candidate_node = []
    count_to_move_up = 0
    def __init__(self, state: State, parent=None, from_action=None):
        self.state = state
        self.parent = parent
        self.from_action = from_action
        self.childrens = []
        # reward và visit sẽ dùng trong công thức UCB để tính toán giá trị dùng để chọn
        # best child node
        self.reward = 0.0
        self.visits = 0
        self.is_closed = False
        if self.parent == None:
            self.depth = 1
        else:
            self.depth = self.parent.depth + 1

        x1,y1 = self.state.blocks[0]
        x2,y2 = self.state.blocks[1]
        xg,yg = self.state.finish
        
        # Simple Euclid distance to goal
        h1 = math.sqrt(pow(abs(x1-xg),2) + pow(abs(y1-yg),2))
        h2 = math.sqrt(pow(abs(x2-xg),2) + pow(abs(y2-yg),2))
        self.h = (h1 + h2) / 2

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
            if compare_node(s, self):
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
        # Move down
        if node.depth == MCTSNode.root.depth + 10: # Số depth move down, up
            if MCTSNode.candidate_node == []:
                MCTSNode.candidate_node.append([node, 1])
            else:
                exist = False
                for n in MCTSNode.candidate_node:
                    if compare_node(n[0], node):
                        exist = True
                        n[1] += 1
                        # count_to_move_down
                        if n[1] == 65:
                            MCTSNode.root = node
                            MCTSNode.candidate_node = []
                if exist == False:
                    MCTSNode.candidate_node.append([node, 1])


        node = get_best_child(node)
    return expand(node)


# Expand: Thêm node mới vào cây. Với mỗi action cho ra state hợp lệ
# sẽ thêm node mới với state đó vào cây.
# Trả về node con đầu tiên. Nếu không thể expand nữa trả về chính nó.
def expand(node: MCTSNode):
    possible_child_node = node.get_possible_next_node()
    if possible_child_node != []:
        for child_node in possible_child_node:
            MCTSNode.visited_node.append(child_node)
            node.childrens.append(child_node)
        return node.childrens[0]
    else:
        return node


# Dùng công thức UCB để tính giá trị của các node con. Chọn ra node có giá trị cao nhất.
# Nếu có nhiều hơn 1 bestchild chọn ngẫu nhiên.
def get_best_child(node: MCTSNode):
    scalar = 20
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
        explore = math.sqrt(20 * math.log(node.visits)/float(c.visits))	
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
    score = 0

# Tính điểm trước random move
    ## Trường hợp trừ điểm

        ### Move up do simulation hoài mà không tiến gần được đến finish
    if node.h >= MCTSNode.best_distance:
        MCTSNode.count_to_move_up += 1
    
    if MCTSNode.count_to_move_up == 110:        # count_to_move_up
        MCTSNode.candidate_node = []
        MCTSNode.count_to_move_up = 0
        if MCTSNode.root.parent != None:
            for x in range(10):  # Số depth move down, up
                MCTSNode.root = MCTSNode.root.parent
        score += -100

        ### Move up do node close
    if node.is_closed and compare_node(node, MCTSNode.root):
        MCTSNode.candidate_node = []
        MCTSNode.count_to_move_up = 0
        if MCTSNode.root.parent != None:
            for x in range(10):  # Số depth move down, up
                MCTSNode.root = MCTSNode.root.parent
        return -45
        
        ### Node bị close
    if node.is_closed:
        return -5
    
    ## Trường hợp cộng điểm
    if node.h < MCTSNode.best_distance:
        score += 100
        MCTSNode.best_distance = node.h
        MCTSNode.count_to_move_up = 0
    
    if node.h < node.parent.h:
        score += 25
    

    depth_of_simulation = 0
    max_depth = 3

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

# Tính điểm sau khi đã simulation

    ## Node bị close
    if depth_of_simulation == 0:
        node.is_closed = True
        return -5

    if node.is_terminal() == False:
        score += 0.5
    else:
        score += -0.5
    

    return score


# Backpropagate kết quả thu được từ simulation lên trở lại đến root.
# Mỗi node trên backpropagation path sẽ được cộng thêm reward và visit cộng 1
def backpropagate(node: MCTSNode, reward):
    while node != None:
        node.reward += reward * (node.visits / 10)
        node.visits += 1
        node = node.parent
    

def MCTS(state: State):
    initial = MCTSNode(state)
    MCTSNode.root = initial
    MCTSNode.init_start_to_finish_dist = initial.h
    MCTSNode.visited_node.append(initial)
    for i in range(ITERATIONLIMIT):
        # cont = '---------------------------Vòng lặp ' + str(i) + '--------------------------' + '\n'
        # file = open("result.txt", 'a', encoding="utf-8")
        # file.write(cont)
        # file.close()
        node = selection(MCTSNode.root)
        reward = simulation(node, i)
        if type(reward) == float or type(reward) == int:
            backpropagate(node, reward)
        else:
            action_list = reward.get_action_list()
            return action_list

    return ["OUT OF TIME"]
    