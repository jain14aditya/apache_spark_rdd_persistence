import dag_parser
from dag_parser import parseDAG
import random
import copy
import draw_graph as dg

persist_limit_percent = 0.2
min_limit_of_nodes = 1

number_of_nodes_to_persist = 3

iterations = 10

class Node:
    def __init__(self,idx,name,children):
        self.idx = idx
        self.children = children
        self.name = name
        self.parents = []

class Graph:
    def __init__(self,adj_list,node_names):
        self._node_map = {}
        self._out_node = None
        for k,v in adj_list.items():
            node = Node(k,node_names[k],v)
            self._node_map[k] = node
            if len(v) == 0:
                self._out_node = node
        
        for k,v in self._node_map.items():
            for child in v.children:
                self._node_map[child].parents.append(k)

    def getNode(self,idx):
        return self._node_map[idx] if idx in self._node_map else None

    def getOutNode(self):
        return self._out_node

    def getOutNodeIdx(self):
        return self._out_node.idx

    def getNodesCount(self):
        return len(self._node_map)

    def getNodes(self):
        return self._node_map


def ComputeCost(graph,node_idx,persist_map,cost1,cost2,is_visited):
    cost = 0
    node = graph.getNode(node_idx)
    if len(node.parents) == 0:
        return cost

    for p in node.parents:
        if p not in is_visited:
            c1 = ComputeCost(graph,p,persist_map,cost1,cost2,is_visited)
            cost += c1
            cost1[p] = c1
            is_visited.add(p)
            if p in persist_map:
                cost2[p] = 0
        else:
            if p not in cost2:
                cost2[p] = ComputeCost(graph,p,persist_map,cost1,cost2,is_visited)
            cost += cost2[p]
    return cost + 1

def Cost(graph,persist_map):
    cost1 = {}
    cost2 = {}
    is_visited = set()

    return ComputeCost(graph,graph.getOutNodeIdx(),persist_map,cost1,cost2,is_visited)

def find_optmial_persistence(graph):
    pass


def get_persist_map(persistable_state, persistable_list):
	persist_map = set()
	for i,k in enumerate(persistable_state):
		if k == 1:
			persist_map.add(persistable_list[i])
	return persist_map

def get_neighbours(persistable_state):
	persistable_neighbours = []
	zeros = []
	ones = []
	for i,v in enumerate(persistable_state):
		if v == 0:
			zeros.append(i)
		else:
			ones.append(i)

	for o in ones:
		for z in zeros:
			neighbor = copy.deepcopy(persistable_state)
			neighbor[o],neighbor[z] = neighbor[z],neighbor[o]
			persistable_neighbours.append(neighbor)
	return persistable_neighbours

def local_search(graph):
    # only the nodes that have more than 2 childs
    nodes_with_2_childs = []
    for _, node in graph.getNodes().items():
    	if len(node.children) >= 2:
    		nodes_with_2_childs.append([node.idx, len(node.children)])

    nodes_with_2_childs.sort(key = lambda x: x[1], reverse = True)
    cnt = len(nodes_with_2_childs)

    state_length = cnt

    # form initial state of persist map
    persistable_list = [x[0] for x in nodes_with_2_childs][:state_length]

    if state_length < number_of_nodes_to_persist:
        persistable_state = [1] * state_length
        return get_persist_map(persistable_state,persistable_list)

    persistable_state = [1] * number_of_nodes_to_persist + [0] * (state_length - number_of_nodes_to_persist)
    
    itr = 0
    best_state = persistable_state
    best_cost = Cost(graph, get_persist_map(persistable_state, persistable_list))
    while itr < iterations:
    	random.shuffle(persistable_state)
    	curr_state = persistable_state
    	curr_cost = Cost(graph, get_persist_map(curr_state, persistable_list))
    	counter = 0
    	while True:
    		print("iteration : ",itr,"counter : ",counter)
    		print("curr state : ",curr_state,"curr cost : ",curr_cost)
    		min_neigh_cost = curr_cost
    		min_neigh_state = curr_state
    		for neighbor_state in get_neighbours(curr_state):
    			neigh_cost = Cost(graph, get_persist_map(neighbor_state, persistable_list))
    			if min_neigh_cost > neigh_cost:
    				min_neigh_cost = neigh_cost
    				min_neigh_state = neighbor_state
    		if min_neigh_state == curr_state:
    			break
    		else:
    			curr_state = min_neigh_state
    			curr_cost = min_neigh_cost
    		counter += 1

    	if best_cost >= curr_cost:
    		best_state = curr_state
    		best_cost = curr_cost
    	itr += 1

    print(get_persist_map(best_state, persistable_list))
    return get_persist_map(best_state, persistable_list)


