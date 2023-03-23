from Class.state import State
from math import sqrt

# Heuristic function = Manhattan Distance.


def A_star(initial_node):
    # Initialize open states and close states:
    State.open_states = [initial_node]
    State.close_states = []
    
    while len(State.open_states) > 0:  
        current_node = State.open_states[0]
        current_index = 0
        node_status = current_node.get_node_status()

        if node_status == 1 :
            action_list = State.open_states[0].get_action_list()
            print( "[" + ' '.join(action_list) + " FINISH]" )
            return action_list
        elif node_status == -1 :
            action_list = State.open_states[0].get_action_list()
            print( "[" + ' '.join(action_list) + " DEAD]" )

        for index, item in enumerate(State.open_states):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        State.open_states.pop(current_index)
        State.close_states.append(current_node)

        # if State.is_finished():
        #     path = []
        #     current = current_node

        #     while current is not None:
        #         path.append(current.move)
        #         current = current.parent
        #     return path[::-1]

        children = current_node.add_childs()

        for child in children:
            if child in State.close_states:
                continue

            child.g = current_node.g + 1

            # hn1 = abs(child.state.blocks[0] - )

    return ["ERROR"]
