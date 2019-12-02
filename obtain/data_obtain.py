
import pandas as pd
import networkx as nx
import os
import pickle
import logging


def get_soc_blog_catalog(path):
    DUMP_PATH = './dump/graph/soc_blog_catalog'
    MAX_NODE = 5000
    graph = None
    if os.path.exists(DUMP_PATH):
        pickle_file = open(DUMP_PATH, 'rb')
        graph = pickle.load(pickle_file)
        logging.info("load soc_blog_catalog from file '%s'" % DUMP_PATH)
    else:
        """
        read soc_blog_catalog data set from path.
        param path is the path of it.
        """
        graph_info = pd.DataFrame(pd.read_csv(path, delimiter=' '))
        graph = nx.Graph()
        # node_cnt = int(graph_info.iloc[0][0])
        graph.add_nodes_from([i + 1 for i in range(MAX_NODE)])

        """filter the node whose id is grater than MAX_NODE"""
        all_edges = zip(graph_info.iloc[1:, 0], graph_info.iloc[1:, 1])
        filtered_eages = [edge for edge in all_edges if edge[0] >=
                          1 and edge[0] <= MAX_NODE and edge[1] >= 1 and edge[1] <= MAX_NODE]
        logging.info(
            "After filtered, the soc_blog_catalog edges is %d." % len(filtered_eages))
        """
        the first line of soc_blog_catalog is node_cnt, node_cnt, edge_cnt, so skip it.
        the data set has a huge number of nodes and edges, for test, I peeked only 100000 head of it.
        """
        graph.add_edges_from(filtered_eages)
        """dump graph to the file."""
        pickle_file = open(DUMP_PATH, 'wb')
        pickle.dump(graph, pickle_file)
        logging.info("dump graph to file '%s'" % DUMP_PATH)
    return graph
