import networkx as nx
from node2vec import Node2Vec
from gensim.models.word2vec import Word2Vec
import logging
import os


def node2vec(graph: nx.Graph, model_path: str, dimensions: int = 3, walk_length: int = 80, num_walks: int = 10, workers: int = 4):
    model = None
    if os.path.exists(model_path) is False:
        # The model is not saved before, now fit the graph and save model to model_path.
        node2vec = Node2Vec(graph, dimensions=dimensions,
                            walk_length=walk_length, num_walks=num_walks, workers=workers, temp_folder="./temp")
        model = node2vec.fit(workers=workers)
        model.save(model_path)
        logging.info("Saved model to file '%s'." % model_path)
    else:
        # The model is saved before, load it directly.
        if os.path.isfile(model_path) is False:
            raise FileNotFoundError("The path %s is not a file !" % model_path)
        model = Word2Vec.load(model_path)
        logging.info("Loaded model from file '%s'. " % model_path)
    return model
