from Class.node import Node

def DFS(initial_node):
    
    initial_node.add_childs()
    node_status = initial_node.get_node_status()
    
    if node_status == 1 :
        res = ""
        for action in initial_node.get_action_list():
            res = res + " " + action
        res = res + " FINISH"
        print(res)
        return ["FINISH"]
    elif node_status == -1 :
        res = ""
        for action in initial_node.get_action_list():
            res = res + " " + action
        res = res + " DEAD"
        print(res)
        return ["DEAD"]
        
    for child in initial_node.child_nodes :
        path = DFS(child)
        print(child.from_action)
        if path[-1] == "FINISH":
            return [child.from_action] + path
        
    return ["ERROR"]