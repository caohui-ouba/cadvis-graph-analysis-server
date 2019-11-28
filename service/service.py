import networkx as nx
from node2vec import Node2Vec
import logging
import os


def node2vec(graph: nx.Graph, model_path: str, dimensions: int = 3, walk_length: int = 3, num_walks: int = 200, workers: int = 8):
    model = None
    if os.path.exists(model_path) is False:
        node2vec = Node2Vec(graph, dimensions=dimensions,
                            walk_length=walk_length, num_walks=num_walks, workers=workers, temp_folder="./temp")
        model = node2vec.fit(window=10, min_count=1, batch_words=4)
        model.save(model_path)
        logging.info("saved model to path '%s'." % model_path)
    else:
        if os.path.isfile(model_path) is False:
            raise FileNotFoundError("The path %s is not a file !" % model_path)
    return model
