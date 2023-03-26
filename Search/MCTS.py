import random
import math
from Class.state import State



class MCTSNode:
    visited_node = []
    def __init__(self, state: State, parent=None, from_action=None):
        self.state = state
        self.parent = parent
        self.from_action = from_action
        self.children = []
        self.possible_children = []
        
        self.reward = 0.0
        self.visits = 0
        
            
        x1,y1 = self.state.blocks[0]
        x2,y2 = self.state.blocks[1]
        xg,yg = self.state.finish
        
        
        # Simple Chebyshev distance to goal
        h1 = max((x1-xg),(y1-yg))
        h2 = max((x2-xg),(y2-yg))
        self.h = max(h1,h2)
        
        

    def add_possible_children(self):
        child_states = self.state.next_valid_states()
        for child in child_states:
            next_node = MCTSNode(child[1],self,child[0])
            if not next_node.repeated_node():
                self.possible_children.append(next_node)
        return self.possible_children

    def not_fully_expand(self):
        if len(self.children) < len(self.possible_children):
            return True
        return False

    def is_terminal(self):
        if len(self.possible_children) == 0:
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
    
    def select_best_child(self, c=1.4):
        # Select a child node to explore, using the UCT formula.
        
        if not self.not_fully_expand():
            log_total = math.log(sum(child.visits for child in self.children))
            scores = [(child.reward / child.visits) + c * math.sqrt(log_total / child.visits) for child in self.children]
            max_score = max(scores)
            return self.children[scores.index(max_score)]
        else:
            # choose a random unexplored child and create a new node for it
            unexplored_children = [child for child in self.possible_children if child not in self.children]
            new_node = random.choice(unexplored_children)
            self.children.append(new_node)
            return new_node
        
    def simulation(self):
        # Perform a random simulation, stopping after 5 actions or when a terminal node is reached.
        node = self
        for i in range(5):
            
            if node.state.is_finished():
                return node.get_action_list()
            
            node.add_possible_children()
            MCTSNode.visited_node.append(node)
            possible_children = node.possible_children
            if node.is_terminal():
                return 0
            node = random.choice(possible_children)
        return node.h/len([x for x in node.get_action_list() if x!= 'SPACE'])
    
    def backpropagation(self, reward):
        # Update the node's reward and visit count and propagate it up the tree.
        self.reward += reward
        self.visits += 1

        # Propagate the reward and visit count up the tree.
        if self.parent is not None:
            self.parent.backpropagation(reward)

# Số lần thực hiện vòng lặp MCTS
NUM_SIMULATIONS = 100

    
def MCTS(root):
    
    if root.state.is_finished():
            return node.get_action_list()
    root.add_possible_children()
    MCTSNode.visited_node.append(root)
    for i in range(NUM_SIMULATIONS):
        node = root
        # selection
        while not node.is_terminal():
            if node.not_fully_expand():
                node = node.select_best_child()
                
                if node.state.is_finished():
                    return node.get_action_list()
                
                node.add_possible_children()      
                MCTSNode.visited_node.append(node)
                
                break
            else:
                node = node.select_best_child()
                
            
        
        
        
        # simulation
        reward = node.simulation()
        if isinstance(reward, list) and isinstance(reward[0], str):
            return reward
        # backpropagation
        node.backpropagation(reward)
    
    # get the best action
    best_child = max(root.children, key=lambda child: child.visits)
    return MCTS(best_child)

    
    
def compare_matrix(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False
    return True

    