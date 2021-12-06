import re
import collections

vertex_map={}
edges_list=[]
graph={}
supported_operations={"range", "join", "filter", "union"}
supported_vertices=set()
new_graph={}

def getDetailsFromLine(line):
    x=re.search("[a-zA-Z]", line)
    line=line[x.start():]
    words = line.split()
    last_word=words[-1]
    last_word = last_word[1:-1]
    words= words[:-1]
    return ' '.join(words), int(last_word)

def process_graph(start_line, lines):
    if start_line+1 >= len(lines):
        return
    line = lines[start_line]
    curr_pos = line.find("+-")
    curr_col_pos = line.find(":-")
    if curr_pos == -1:
        curr_pos = curr_col_pos
    next_line = lines[start_line+1]

    plus_pos = next_line.find("+-")
    colon_pos = next_line.find(":-")

    if plus_pos == -1 and colon_pos == -1:
        return

    if plus_pos != -1 and plus_pos <= curr_pos:
        return
    if colon_pos != -1 and colon_pos <= curr_pos:
        return

    l1_name, l1_num = getDetailsFromLine(line)
    l2_name, l2_num = getDetailsFromLine(next_line)

    vertex_map[l1_num] = l1_name
    vertex_map[l2_num] = l2_name
    edges_list.append([l1_num, l2_num])
    if plus_pos != -1:
        process_graph(start_line+1, lines)
        return
    process_graph(start_line+1, lines)
    cnt = start_line+1
    for tline in lines[start_line+1:]:
        if tline[colon_pos] == '+':
            l3_name, l3_num = getDetailsFromLine(tline)
            vertex_map[l3_num] = l3_name
            edges_list.append([l1_num, l3_num])
            process_graph(cnt, lines)
            return

        cnt += 1

def make_graph(edges):
    for vertex in vertex_map.keys():
        graph[vertex]=[]

    for edge in edges:
        graph[edge[1]].append(edge[0])

    for v, childs in graph.items():
        graph[v]=list(dict.fromkeys(childs))

def make_supported_vertices() :
    for vertex in graph.keys():
        for so in supported_operations:
            if so in vertex_map[vertex].lower():
                supported_vertices.add(vertex)
                vertex_map[vertex] = so

def prune_edges(vertex):
    for child in graph[vertex]:
        if not (child in supported_vertices):
            graph[vertex].remove(child)
            graph[vertex]=graph[vertex]+(graph[child])
            prune_edges(vertex)
            return

def parseDAG(filename):
    with open(filename) as f:
        lines = f.readlines()
        process_graph(1, lines)

    od = collections.OrderedDict(sorted(vertex_map.items()))

    make_graph(edges_list)

    make_supported_vertices()

    for vertex in supported_vertices:
        prune_edges(vertex)
        new_graph[vertex] = graph[vertex]

    # print(new_graph, vertex_map)
    return new_graph,vertex_map

if __name__ == "main":
    pass


