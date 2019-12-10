
# from service.service import get_graph_model_by_name
import service.service as service
import networkx as nx


def get_similar_structure(graph_name: str, nodes: list, k: int):
    """
    Accordiing to the Paper Structure-Based Suggestive Exploration :A New Approach for Effective Exploration of Large Networks.
    Impliment the algrithem of this paper to find a similar structure with given structure.
    """
    graph, model = service.get_graph_model_by_name(graph_name)
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
        if neighbor_id in gsim:
            """Iclude circle."""
            edges.append((id, neighbor_id))
            if neighbor_id not in visited:
                find_connected_component(
                    neighbor_id, nodes, edges, visited, graph, gsim)
