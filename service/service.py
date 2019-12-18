import networkx as nx
from entity.entity import Graph, Node
from node2vec import Node2Vec
import numpy as np
from gensim.models.word2vec import Word2Vec
from flask import current_app
from sklearn.decomposition import PCA
from sklearn import manifold
from algorithm.search_community import PyLouvain
from algorithm.similar_structure import get_similar_structure
from algorithm.structure_correspond import find_structure_correspond
import config.task_mapping as TASK_ID
import logging
import os
import pickle


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


def get_graph_by_name(name: str):
    nxGraph, model = get_graph_model_by_name(name)
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
    elif "mock_community_graph" == graph_name:
        return current_app.config["mock_community_graph"], current_app.config["mock_community_model"]
    return None, None


def get_similar_struc(name: str, nodes: list, k: int):
    graph, model = get_graph_model_by_name(name)
    compoments = get_similar_structure(name, nodes, k)
    correspond = find_structure_correspond(nodes, model, compoments)
    return {"compoments": compoments, "correspond": correspond}


def get_commutity_by_name(name: str):
    if 'soc_blog_catalog' == name:
        return get_patition_model_by_name(name, './dump/community/soc_blog_community')
    elif 'mock_community_graph' == name:
        return get_patition_model_by_name(name, './dump/community/mock_community_graph')
    return None


def get_patition_model_by_name(name: str, path: str):
    """
    If dumped the partition before, load the partition directly,
    if not , use algrithm to search partition first, then dump it to file while the method's param specific.
    """
    partition = None
    if os.path.exists(path):
        pickle_file = open(path, 'rb')
        partition = pickle.load(pickle_file)
        logging.info("Loaded partition from file '%s'." % path)
    else:
        graph, model = get_graph_model_by_name(name)
        alg = PyLouvain.from_graph(graph)
        res, q = alg.apply_method()
        partition = []
        for arr in res:
            partition.append([a + 1 for a in arr])
        dump_file = open(path, 'wb')
        pickle.dump(partition, dump_file)
        logging.info("Dumped partition to file '%s' " % path)
    return partition


def decomposition(X: list, n_component: int = 2):
    pca = PCA(n_component)
    pca.fit(X)
    res = pca.fit_transform(X)
    return res


def decomposition_by_tsne(X: list, n_component: int = 2):

    embeded = manifold.TSNE(n_components=n_component,
                            random_state=1).fit_transform(X)
    return embeded


def sigmoid(X):
    return 1.0 / (1 + np.exp(-X))


def doTask(task, container: dict = None):
    if dict is None:
        raise AttributeError("container is None in 'doTask'!")
    """task是一个Task类型的json"""
    taskId = task.taskId
    if taskId == TASK_ID.COMMUNITY_DETECT:
        __checkParam(task, "graph_name")
        container[taskId] = get_commutity_by_name(task["params"]["graph_name"])
        __doSubTasks(task, container)
    elif taskId == TASK_ID.NODE_EMBEDDING:
        __checkParam(task, "graph_name")
        container[taskId] = get_graph_by_name(task["params"]["graph_name"])
        __doSubTasks(task, container)
    elif taskId == TASK_ID.UNUSUAL_NODE_DETECT:
        pass
    elif taskId == TASK_ID.SIMILAR_STRUCTURE:
        __checkParam(task, "graph_name")
        __checkParam(task, "nodes")
        __checkParam(task, "k")
        container[taskId] = get_graph_by_name(
            task["params"]["graph_name"], task["params"]["nodes"], task["params"]["k"])
        __doSubTasks(task, container)
    elif taskId == TASK_ID.NODE_CORESSPOND:
        pass
    else:
        pass


def __doSubTasks(task, container):
    if "subTasks" in task:
        for subTask in task["subTasks"]:
            doTask(subTask, container)


def __checkParam(task: dict, paramName: str):
    if "params" not in task:
        raise AttributeError(
            "params is None in '%s' !" % task.taskName)
    if paramName not in task["params"]:
        raise AttributeError(
            "params '%s' is None in 'doTask' of task '%s' !" % (paramName, task.taskName))
