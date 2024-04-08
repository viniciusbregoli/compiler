from graphviz import Digraph


class TreeNode:
    def __init__(self, value, type=None, children=[]):
        self.value = value
        self.type = type
        self.children = children

    def __repr__(self):
        return f"{self.value}"


def visualize_ast(node, graph=None):
    if graph is None:
        graph = Digraph()
        graph.node(name=str(id(node)), label=str(node.value))

    for child in node.children:
        graph.node(name=str(id(child)), label=str(child.value))
        graph.edge(str(id(node)), str(id(child)))
        visualize_ast(child, graph)

    return graph

