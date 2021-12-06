import networkx as nx 
import numpy as np 
import math
import matplotlib.pyplot as plt
from collections import defaultdict

persisted_node_color = '#f5ef42'
norm_color = '#1f77b4'
out_node_color = '#eb3467'
input_node_color = '#4ceb34'

options = {
	'node_size': 400,
	'width': 2,
	'arrowstyle': '-|>',
	'arrowsize': 12,
}

def plot(graph_adj_list,persist_map,name_map=[],show=False,out_filename='graph.png'):
	g = nx.DiGraph()

	parent_map = defaultdict(list)
	for k,v in graph_adj_list.items():
		for child in v: 
			g.add_edge(k,child)
			parent_map[child].append(k)

	node_colors = []
	labels = {}
	for x in g.nodes:
		if x in persist_map:
			node_colors.append(persisted_node_color)
		elif len(graph_adj_list[x]) == 0:
			node_colors.append(out_node_color)
		elif len(parent_map[x]) == 0:
			node_colors.append(input_node_color)
		else:
			node_colors.append(norm_color)

		if len(name_map) > 0:
			labels[x] = name_map[x]
	
	if len(name_map) > 0:
		nx.draw_networkx(g, arrows = True, node_color = node_colors, labels = labels,pos = nx.spring_layout(g),**options)
	else:
		nx.draw_networkx(g, arrows = True, node_color = node_colors, label = 'hello',pos = nx.spring_layout(g),**options)

	if show:
		plt.show()
	else:
		plt.savefig('graph.png')

		