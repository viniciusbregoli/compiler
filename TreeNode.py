class TreeNode:
    def __init__(self, value, type=None, children=[]):
        self.value = value
        self.type = type
        self.children = children

    def __repr__(self):
        return f"Node(value={self.value}, type={self.type}, children={self.children})"
