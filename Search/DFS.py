from ..Class.node import Node
def DFS(initial_node = Node()):
    
    initial_node.add_childs()
    node_status = initial_node.get_node_status()
    
    if node_status == 1 :
        return ["FINISH"]
    
    if node_status == -1 :
        return ["DEAD"]
    
    for child in initial_node.child_nodes :
        path = DFS(child)
        if path[-1] == "FINISH":
            return [child.from_action] + path
        
    return ["ERROR"]