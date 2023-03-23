from Class.node import Node
from Class.map import Map

from math import sqrt

# Heuristic function = Chebyshev Distance.


def A_star(initial_node):
    # Initialize open states and close states:
    Node.open_list = [initial_node]
    Node.close_list = []
    
    while len(Node.open_list) > 0:  
        if Node.open_list[0].repeated_node():
            print( "[" + ' '.join(Node.open_list[0].get_action_list()) + " REPEATED]\n" )
            Node.open_list.pop(0)
            continue

        current_node = Node.open_list[0]
        current_index = 0
        node_status = current_node.get_node_status()

        if node_status == 1 :
            action_list = Node.open_list[0].get_action_list()
            print( "[" + ' '.join(action_list) + " FINISH]" )
            return action_list
        elif node_status == -1 :
            action_list = Node.open_list[0].get_action_list()
            print( "[" + ' '.join(action_list) + " DEAD]" )

        for index, item in enumerate(Node.open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        Node.open_list.pop(current_index)
        Node.close_list.append(current_node)

        # if State.is_finished():
        #     path = []
        #     current = current_node

        #     while current is not None:
        #         path.append(current.move)
        #         current = current.parent
        #     return path[::-1]

        children = current_node.add_childs()

        for child in children:
            if child in Node.close_list:
                continue

            child.g = current_node.g + 1

            h1 = max(abs(child.state.blocks[0][0] - Map.finish[0]), abs(child.state.blocks[0][1] - Map.finish[1]))
            h2 = max(abs(child.state.blocks[1][0] - Map.finish[0]), abs(child.state.blocks[1][1] - Map.finish[1]))
            child.h = max(h1, h2)

            child.f = child.g + child.h

            for open_node in Node.open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            Node.open_list.append(child)

    return ["ERROR"]
