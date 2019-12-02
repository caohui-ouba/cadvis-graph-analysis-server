class Node(object):

    def __init__(self, id):
        self.id = id
        self.vec = []
        self.neighbours = []

    def add_neighbour(self, node_id):
        self.neighbours.append(node_id)


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
        self.edges.append(edge)
