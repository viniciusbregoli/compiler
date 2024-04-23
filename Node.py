class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.value})"


def build_syntax_tree(expression):
    stack = []
    for token in expression:
        if token in ["+", "-", "*", "/"]:
            # Cria um novo nó com o operador
            node = Node(token)

            # Define os filhos direito e esquerdo retirando da pilha
            node.right = stack.pop()
            node.left = stack.pop()

            # Empilha o nó
            stack.append(node)
        else:
            # Empilha um novo nó com o número
            stack.append(Node(float(token)))
    return stack.pop()  # Retorna a raiz da árvore


def print_tree(node, level=0):
    if node != None:
        print_tree(node.right, level + 1)
        print(" " * 4 * level + "->", node.value)
        print_tree(node.left, level + 1)
