import networkx as nx
from entity.entity import Graph, Node
from node2vec import Node2Vec
import numpy as np
from gensim.models.word2vec import Word2Vec
from flask import current_app
from sklearn.decomposition import PCA
import logging
import os


def node2vec(graph: nx.Graph, model_path: str, dimensions: int = 20, walk_length: int = 80, num_walks: int = 10, workers: int = 4):
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


def get_graph(nxGraph: nx.Graph, model: Word2Vec):
    graph = Graph()
    X = []
    for i in range(len(nxGraph.nodes)):
        X.append(model.wv.get_vector(str(i + 1)))

    X_2 = sigmoid(decomposition(X))

    for node_id in nxGraph.nodes():
        node = Node(node_id)
        """node_id index from 1 but X_2 index from 0."""
        node.vec = [float(x) for x in X_2[node_id - 1]]
        graph.add_node(node)
    graph.edges = list(nxGraph.edges())
    # print(graph.edges[0])
    return graph


def get_graph_model_by_name(graph_name: str):
    if "soc_blog_catalog" == graph_name:
        return current_app.config["soc_blog_graph"], current_app.config["soc_blog_model"]
    return None, None


def decomposition(X: list, n_component: int = 2):
    pca = PCA(n_component)
    pca.fit(X)
    res = pca.fit_transform(X)
    return res


def sigmoid(X):
    return 1.0 / (1 + np.exp(-X))
