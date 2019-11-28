class Node(object):

    def __init__(self, id):
        self.id = id
        self.vec = []
        self.neighbours = []

    def add_neighbour(self, node_id):
        self.neighbours.append(node_id)


class Edge(object):

    def __init__(self, start_node_id, end_node_id):
        """ Receive 2 arguments from and to node."""
        self.start = start_node_id
        self.end = end_node_id


class Graph(object):

    def __init__(self):
        # id -> node
        self.nodes = {}
        self.edges = []

    def add_node(self, node):
        if type(node) != Node:
            raise AttributeError(
                "the arrgument 'node' in method add_node is not type Node !")
        self.nodes[node.id] = node

    def get_node(self, id):
        return self.nodes[id]

    def add_edge(self, edge):
        if type(edge) != Edge:
            raise AttributeError(
                "the arrgument 'edge' in method add_edge is not type Edge !")
        self.edges.append(edge)
