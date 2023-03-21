def DFS(initial_node):
    
    initial_node.add_childs()
    node_status = initial_node.get_node_status()
    
    if node_status == 1 :
        print( "[" + ' '.join(initial_node.get_action_list()) + " FINISH]" )
        return ["FINISH"]
    elif node_status == -1 :
        print( "[" + ' '.join(initial_node.get_action_list()) + " DEAD]" )
        return ["DEAD"]
        
    for child in initial_node.child_nodes :
        path = DFS(child)
        if path[-1] == "FINISH":
            return [child.from_action] + path
        
    return ["ERROR"]