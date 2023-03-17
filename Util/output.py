import os
from Class.state import State
from Class.node import Node
from Search.DFS import DFS

# used for main.py
def get_output(level, algorithm , realtime = False):
    if not realtime :
        path = f'Output/{algorithm}/{level}.txt'
        with open(path, 'r') as file:
            first_line = file.readline().strip()
            actions = first_line.split(' ')
        return actions
    
    path = f'StageInfo/{level}.txt'
    if algorithm == 'DFS':
        init_node = Node(State(path))
        return DFS(init_node)
    elif algorithm == 'BFS':
        pass
    elif algorithm == 'AStar':
        pass
    elif algorithm == 'MCTS':
        pass

def write_output(level, actions, algorithm, path=None):
    if path is None:
        path = f'Output/{algorithm}/{level}.txt'
    else:
        path = os.path.join(path,f'{algorithm}/{level}.txt')
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path,'w') as f:
        f.write(' '.join(actions))