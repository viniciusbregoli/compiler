from graphviz import Digraph

global z
z = 0


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.value})"


def build_syntax_tree(expression):
    stack = []
    for k in range(len(expression)):
        token = expression[k]
        if token in ["+", "-", "*", "/", "|", "%", "^"]:
            # Cria um novo nó com o operador
            node = Node(token)

            # Define os filhos direito e esquerdo retirando da pilha
            node.right = stack.pop()
            node.left = stack.pop()

            # Empilha o nó
            stack.append(node)
        elif token == "MEM":
            try:
                if (
                    expression[k + 1] in ["+", "-", "*", "/", "|", "%", "^"]
                    or type(expression[k + 1]) == float
                ):
                    stack.append(Node("MEM"))
            except:
                node = Node(token)
                node.left = stack.pop()
                stack.append(node)
        elif token == "RES":
            n = int(stack.pop().value)
            stack.append(Node(f"RES {n}"))
        else:
            # Empilha um novo nó com o número
            stack.append(Node(float(token)))
    return stack.pop()  # Retorna a raiz da árvore

def create_graph(node, graph=None):
    if graph is None:
        graph = Digraph()
        graph.node(name=str(node), label=str(node.value))
    if node.left:
        graph.node(name=str(node.left), label=str(node.left.value))
        graph.edge(str(node), str(node.left))
        create_graph(node.left, graph)
    if node.right:
        graph.node(name=str(node.right), label=str(node.right.value))
        graph.edge(str(node), str(node.right))
        create_graph(node.right, graph)
    return graph


def visualize_tree(node):
    global z
    graph = create_graph(node)
    graph.render(f"syntax_tree_{z}", format="png", cleanup=True, directory="./imgs")
    z += 1
