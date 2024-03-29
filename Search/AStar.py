import heapq
from Class.node_star import NodeStar


def AStar(initial_node):
    open_list = []
    NodeStar.close_list = []
    heapq.heappush(open_list, (initial_node.f, initial_node))
    
    while open_list:
        current_node = heapq.heappop(open_list)[1]
        if current_node.get_node_status() == 1:
            return current_node.get_action_list()
        
        node_cond = current_node.repeated_node()
        current_node.add_childs()
        
        if node_cond == 3: # not repeated in NodeStar.close_list and add childs
            for child in current_node.child_nodes:
                heapq.heappush(open_list, (child.f, child))
            NodeStar.close_list.append(current_node)
            
        # elif node_cond == 2: # repeated NodeStar.close_list with f value bigger 
        #     continue
        
        elif node_cond == 1: # repeated NodeStar.close_list but f value smaller
            for child in current_node.child_nodes:
                heapq.heappush(open_list, (child.f, child))
        
    return ['ERROR']
