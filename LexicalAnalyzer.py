import re
from TreeNode import TreeNode


class LexicalAnalyzer:
    def __init__(self, filepath):  # Constructor
        self.filepath = filepath
        self.lines = self.analyzeFile()

    def classifyToken(self, token):  # Classify the tokens
        if token in ("+", "-", "*", "/", "%", "^", "|"):
            return "OPERATOR"
        elif token in ("(", ")"):
            return "PARENTHESIS"
        elif token in ("RES", "MEM"):
            return "SPECIAL COMMAND"
        else:
            return "NUMBER"

    def analyze(self, line):  # Analyze the tokens
        tokenRegex = r"\(|\)|\+|-|\*|/|%|\^|\||[0-9]+(?:\.[0-9]+)?|\bRES\b|\bMEM\b"
        tokens = re.findall(tokenRegex, line)
        return [(token, self.classifyToken(token)) for token in tokens]

    def analyzeFile(self):  # Analyze the file
        with open(self.filepath, "r") as file:
            lines = file.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].replace("\n", "").strip()
            file.close()
        return lines

    def buildAST(self):
        # Este método pressupõe que as expressões estejam em notação RPN adequada
        for line in self.lines:
            tokens = self.analyze(line)
            stack = []
            for token, type in tokens:
                if type == "NUMBER":
                    stack.append(TreeNode(token, type="NUMBER"))
                elif type == "OPERATOR":
                    right = stack.pop()
                    left = stack.pop()
                    node = TreeNode(token, type="OPERATOR", children=[left, right])
                    stack.append(node)
                # Adicione condições adicionais para tipos especiais de tokens se necessário
            yield stack.pop()  # Retorna a raiz da AST para a linha atual


lex = LexicalAnalyzer("input.txt")
asts = list(lex.buildAST())
for ast in asts:
    print(ast)