class Node(object):

    def __init__(self, id):
        self.id = id
        self.vec = []
        self.neighbours = []

    def add_neighbour(self, nei):
        if type(nei) != Node:
            raise AttributeError(
                "the arrgument 'nei' in method add_neighbour is not type Node !")
            self.vec.insert(nei)


class Edge(object):

    def __init__(self, start, end):
        """ Receive 2 arguments from and to node."""
        if type(start) != Node or type(end) != Node:
            raise AttributeError("start or end is node the type Node!")
        self.start = start
        self.end = end


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
