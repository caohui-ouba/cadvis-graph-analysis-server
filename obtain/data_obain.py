
import pandas as pd
from entity.entity import Graph, Node, Edge


def get_soc_blog_catalog(path):
    graph_info = pd.DataFrame(pd.read_csv(path, delimiter=' '))
    graph = Graph()
    node_cnt = int(graph_info.iloc[0][0])

    for id in range(node_cnt):
        graph.add_node(Node(id + 1))

    edge_cnt = int(graph_info.iloc[0][2])
    num = 0
    for row in zip(graph_info.iloc[1:, 0], graph_info.iloc[1:, 1]):
        a = graph.get_node(row[0])
        b = graph.get_node(row[1])
        a.add_neighbour(b)
        b.add_neighbour(a)
        graph.add_edge(Edge(a, b))
        graph.add_edge(Edge(b, a))
        num += 1
        if num % 50000 == 0:
            print("read soc_blog_catalog %.2f" % ((num * 100) / edge_cnt), "%")
    print("read soc_blog_catalog 100%")
    return graph
