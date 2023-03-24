from Class.node import Node

def BFS(initial_node):
    
    Node.open_list = [initial_node]
    
    while len(Node.open_list) > 0:
        if Node.open_list[0].repeated_node():
            # print( "[" + ' '.join(Node.open_list[0].get_action_list()) + " REPEATED]\n" )
            Node.open_list.pop(0)
            continue
        Node.open_list = Node.open_list + Node.open_list[0].add_childs()
        node_status = Node.open_list[0].get_node_status()
        if node_status == 1 :
            action_list = Node.open_list[0].get_action_list()
            # print( "[" + ' '.join(action_list) + " FINISH]" )
            return action_list
        
        Node.close_list.append(Node.open_list[0])
        Node.open_list.pop(0)
        
 
    return ["ERROR"]