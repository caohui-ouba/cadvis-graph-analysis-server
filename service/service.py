import networkx as nx
from entity.entity import Graph, Node
from node2vec import Node2Vec
from gensim.models.word2vec import Word2Vec
from flask import current_app
import logging
import os


def node2vec(graph: nx.Graph, model_path: str, dimensions: int = 2, walk_length: int = 80, num_walks: int = 10, workers: int = 4):
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

    for node_id in nxGraph.nodes():
        node = Node(node_id)
        node.vec = [float(dig) for dig in model.wv.get_vector(str(node_id))]
        graph.add_node(node)
    graph.edges = list(nxGraph.edges())
    # print(graph.edges[0])
    return graph


def get_similar_structure(graph_name: str, nodes: list, k: int):
    """
    Accordiing to the Paper Structure-Based Suggestive Exploration :A New Approach for Effective Exploration of Large Networks.
    Impliment the algrithem of this paper to find a similar structure with given structure.
    """
    graph, model = get_graph_model_by_name(graph_name)
    gsim = []
    for node_id in nodes:
        similar_k = model.wv.most_similar(positive=[str(node_id)], topn=k)
        gsim += [int(item[0]) for item in similar_k if int(item[0])
                 not in gsim and int(item[0]) not in nodes]
    """Find the connected component of gsim"""
    visited = []
    components = []
    for node_id in gsim:
        if node_id not in visited:
            c_nodes = []
            c_edges = []
            find_connected_component(
                node_id, c_nodes, c_edges, visited, graph, gsim)
            components.append({"nodes": c_nodes, "edges": c_edges})
    return components


def find_connected_component(id: int, nodes: list, edges: list, visited: list, graph: nx.Graph, gsim: list):
    """Use dfs find a connected component """
    visited.append(id)
    nodes.append(id)
    neighbors = graph.neighbors(id)
    for neighbor_id in neighbors:
        if neighbor_id in gsim and neighbor_id not in visited:
            edges.append((id, neighbor_id))
            find_connected_component(
                neighbor_id, nodes, edges, visited, graph, gsim)


def get_graph_model_by_name(graph_name: str):
    if "soc_blog_catalog" == graph_name:
        return current_app.config["soc_blog_graph"], current_app.config["soc_blog_model"]
    return None, None
