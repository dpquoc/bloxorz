from Class.state import State

def BFS(initial_node):
    
    State.open_states = [initial_node]
    
    while len(State.open_states) > 0:
        State.open_states = State.open_states + State.open_states[0].add_childs()
        node_status = State.open_states[0].get_node_status()
        
        if node_status == 1 :
            action_list = State.open_states[0].get_action_list()
            print( "[" + ' '.join(action_list) + " FINISH]" )
            return action_list
        elif node_status == -1 :
            action_list = State.open_states[0].get_action_list()
            print( "[" + ' '.join(action_list) + " DEAD]" )
        
        State.open_states.pop(0)
        
 
    return ["ERROR"]