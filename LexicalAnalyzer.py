import re
from TreeNode import *


class LexicalAnalyzer:
    def __init__(self, filepath):  # Constructor
        self.filepath = filepath
        self.lines = self.analyzeFile()
        self.MEM = 0
        self.RES = []
        self.trees = list(self.buildTree())

    def classifyToken(self, token):  # Classify the tokens
        if token in ("+", "-", "*", "/", "%", "^", "|"):
            return "OPERATOR"
        elif token in ("RES"):
            return "RES"
        elif token in ("MEM"):
            return "MEMORY"
        else:
            return "NUMBER"

    def analyze(self, line):  # Analyze the tokens
        tokenRegex = r"\+|-|\*|/|%|\^|\||[0-9]+(?:\.[0-9]+)?|\bRES\b|\bMEM\b"
        tokens = re.findall(tokenRegex, line)
        return [(token, self.classifyToken(token)) for token in tokens]

    def analyzeFile(self):  # Analyze the file
        with open(self.filepath, "r") as file:
            lines = file.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].replace("\n", "").strip()
            file.close()
        return lines

    def solveLine(self, line):  # Solve the line
        tokens = self.analyze(line)
        stack = []
        i = 0
        for token, type in tokens:
            if type == "NUMBER":
                stack.append(float(token))
            elif type == "MEMORY":
                try:
                    nextToken, nextType = tokens[i + 1]
                    if nextType == "OPERATOR" or nextType == "NUMBER":
                        stack.append(self.MEM)
                except IndexError:
                    self.MEM = stack.pop()
                    return 0
            elif type == "RES":
                left = stack.pop()
                stack.append(self.RES[-int(left)])
            elif type == "OPERATOR":
                right = stack.pop()
                left = stack.pop()
                if token == "+":
                    stack.append(left + right)
                elif token == "-":
                    stack.append(left - right)
                elif token == "*":
                    stack.append(left * right)
                elif token == "/":
                    stack.append(left / right)
                elif token == "%":
                    stack.append(left % right)
                elif token == "^":
                    stack.append(left**right)
            i += 1
        return stack.pop()

    def buildTree(self):
        for line in self.lines:
            self.RES.append(self.solveLine(line))
            tokens = self.analyze(line)
            stack = []
            i = 0
            for token, type in tokens:
                if type == "NUMBER":
                    stack.append(TreeNode(token, type="NUMBER"))
                elif type == "MEMORY":
                    try:
                        nextToken, nextType = tokens[i + 1]
                        if nextType == "OPERATOR" or nextType == "NUMBER":
                            stack.append(TreeNode(token, type="MEMORY"))
                    except IndexError:
                        try:
                            right = stack.pop()
                            left = stack.pop()
                            stack.append(
                                TreeNode(token, type="MEMORY", children=[left, right])
                            )
                        except IndexError:
                            stack.append(
                                TreeNode(token, type="MEMORY", children=[right])
                            )
                elif type == "RES":
                    left = stack.pop()
                    stack.append(TreeNode(f"{left} {token}", type="RES"))
                elif type == "OPERATOR":
                    right = stack.pop()
                    left = stack.pop()
                    node = TreeNode(token, type="OPERATOR", children=[left, right])
                    stack.append(node)
                i += 1
            yield stack.pop()


lex = LexicalAnalyzer("./misc/input.txt")
for index, ast in enumerate(lex.trees):
    ast_graph = visualize_ast(ast)
    ast_graph.render(
        filename=f"{index + 1}_ast", directory="./tree_imgs", format="png", cleanup=True
    )
print(lex.RES)
