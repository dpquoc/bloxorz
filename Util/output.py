import os
from Class.state import State
from Class.node import Node
from Class.node_star import NodeStar
from Search.DFS import DFS
from Search.BFS import BFS
from Search.MCTS import MCTS
from Search.AStar import AStar

# used for main.py
def get_output(level, algorithm , realtime = False):
    if not realtime :
        path = f'Output/{algorithm}/{level}.txt'
        with open(path, 'r') as file:
            first_line = file.readline().strip()
            actions = first_line.split(' ')
        return actions
    
    print('---------------------------------------------------CALCULATING---------------------------------------------------\n')
    Node.close_list = []
    Node.open_list = []
    NodeStar.close_list = []
    
    path = f'StageInfo/{level}.txt'
    if algorithm == 'DFS':
        init_node = Node(State(path))
        return DFS(init_node)
    elif algorithm == 'BFS':
        init_node = Node(State(path))
        return BFS(init_node)
    elif algorithm == 'AStar':
        init_node = NodeStar(State(path))
        return AStar(init_node)
    elif algorithm == 'MCTS':
        init_state = State(path)
        return MCTS(init_state)

def write_output(level, actions, algorithm, path=None):
    if path is None:
        path = f'Output/{algorithm}/{level}.txt'
    else:
        path = os.path.join(path,f'{algorithm}/{level}.txt')
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path,'w') as f:
        f.write(' '.join(actions))