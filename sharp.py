from pyspark.sql import SparkSession
import dag_parser
import sys
import draw_graph as dg
import cost_estimation
def optimize(df):
    orig_stdout=sys.stdout
    f=open('sharp_meta.txt', 'w')
    sys.stdout = f

    df.explain(mode="formatted")

    sys.stdout = orig_stdout
    f.close()

    parsed_graph, node_names = dag_parser.parseDAG('sharp_meta.txt')

    graph = cost_estimation.Graph(parsed_graph,node_names)
    persist_map = cost_estimation.local_search(graph)
    print("nodes to be persisted: ",persist_map)

    dg.plot(parsed_graph,persist_map)
