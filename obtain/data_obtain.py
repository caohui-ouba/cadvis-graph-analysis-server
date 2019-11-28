
import pandas as pd
import networkx as nx


def get_soc_blog_catalog(path):
    """
    read soc_blog_catalog data set from path.
    param path is the path of it.
    """
    graph_info = pd.DataFrame(pd.read_csv(path, delimiter=' '))
    graph = nx.Graph()
    node_cnt = int(graph_info.iloc[0][0])
    graph.add_nodes_from([i + 1 for i in range(node_cnt)])
    """
    the first line of soc_blog_catalog is node_cnt, node_cnt, edge_cnt, so skip it.
    the data set has a huge number of nodes and edges, for test, I peeked only 100000 head of it.
    """
    graph.add_edges_from(
        zip(graph_info.iloc[1:100000, 0], graph_info.iloc[1:100000, 1]))
    return graph
