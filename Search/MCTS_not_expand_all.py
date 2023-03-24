import random
import math
from Class.state import State

ITERATIONLIMIT = 1000

def compare_matrix(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False
    return True

class Node:
    visited_node = []
    def __init__(self, state: State, parent=None, from_action=None):
        self.state = state
        self.parent = parent
        self.from_action = from_action
        self.childrens = []
        self.reward = 0.0
        self.visits = 0

        self.reverse_action = None
        if from_action == "UP" or from_action == "SPACE UP":
            self.reverse_action = "DOWN"
        if from_action == "DOWN" or from_action == "SPACE DOWN":
            self.reverse_action = "UP"
        if from_action == "RIGHT" or from_action == "SPACE RIGHT":
            self.reverse_action = "LEFT"
        if from_action == "LEFT" or from_action == "SPACE LEFT":
            self.reverse_action = "RIGHT"
            

    # Lấy ra danh sách những node có thể được expand bởi node hiện tại
    def get_possible_next_node(self):
        possible_next_node = []
        temp = self.state.next_valid_states()

        for i in range(len(temp)):
            node = Node(temp[i][1], self, temp[i][0])
            if not node.repeated_node():
                possible_next_node.append(node)
        
        return possible_next_node
            

    def dist_to_finish(self):
        if self.state.target_block == -1:
            x = abs(self.state.blocks[0][0] - self.state.finish[0])
            y = abs(self.state.blocks[0][1] - self.state.finish[1])
            return x + y
        else:
            x1 = abs(self.state.blocks[0][0] - self.state.finish[0])
            y1 = abs(self.state.blocks[0][1] - self.state.finish[1])
            x2 = abs(self.state.blocks[1][0] - self.state.finish[0])
            y2 = abs(self.state.blocks[1][1] - self.state.finish[1])
            return (x1 + x2 + y1 + y2) / 2.0


    # Check liệu node đã expand hết tất cả những next node có thể chưa 
    def is_fully_expanded(self):
        if (self.childrens != []) and (self.get_possible_next_node() == []):
            return True
        return False


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
        for s in Node.visited_node:
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
    

# Chọn ra node để simulation
def selection(node: Node):
    while not node.is_leaf_node():
        if random.uniform(0,1) < 0.5:
            node = get_best_child(node)
        else:
            if node.is_fully_expanded():
                node = get_best_child(node)
            else:
                return expand(node)
    return expand(node)


# Thực hiện expand node. Tức thêm con vào node đó
def expand(node: Node):
    possible_child_node = node.get_possible_next_node()
    # res = [node.from_action]
    # for c in possible_child_node:
    #     res.append(c.from_action)
    # print(res)
    if possible_child_node != []:
        child_node = random.choice(possible_child_node)
        node.childrens.append(child_node)
        return child_node
    else:
        return node


# Dùng công thức UCB để tính giá trị của các node. Chọn ra node có giá trị cao nhất
def get_best_child(node: Node):
    scalar = 2
    bestscore = -9999
    bestchildren = []

    for c in node.childrens:
        exploit = c.reward / c.visits
        explore = math.sqrt(math.log(node.visits)/float(c.visits))	
        score = exploit + scalar * explore
        if score == bestscore:
            bestchildren.append(c)
        if score > bestscore:
            bestchildren = [c]
            bestscore = score
    return random.choice(bestchildren)
        

def simulation(node: Node, i):
    Node.visited_node.append(node)
    depth_of_simulation = 0
    max_depth = 10
    min_depth = 5
    
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

    score = 50.0
    if depth_of_simulation < min_depth:
        score -= 70
    if depth_of_simulation == max_depth:
        score -= 70
    score -= node.dist_to_finish()

    print(depth_of_simulation, i, node.get_action_list())
    return score


def backpropagate(node: Node, reward):
    while node != None:
        node.reward += reward
        node.visits += 1
        node = node.parent
    

def MCTS(state: State):
    root = Node(state)
    Node.visited_node.append(root)
    for i in range(ITERATIONLIMIT):
        node = selection(root)
        reward = simulation(node, i)
        if type(reward) == float:
            backpropagate(node, reward)
            print(node.reward)
        else:
            action_list = reward.get_action_list()
            return action_list

    return ["OUT OF TIME"]
    