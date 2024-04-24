import re
from Node import *

with open("input.txt", "r") as file:
    lines = file.readlines()
    file.close()


global i, operations, tokens, parenthesis, MEM, results
operations = ["+", "-", "*", "/", "|", "%", "^"]
tokens = []
parenthesis = 0
MEM = 0
results = []


def main():
    global i, z
    global isValid
    global parenthesis
    global tokens
    global MEM
    MEM = 0
    for line in lines:
        i = 0
        parenthesis = 0
        isValid = False
        look = ""
        start(look, line)
        if isValid:
            print("Valid expression: ", line.replace("\n", ""))
            print("Tokens: ", separateTokens(tokens))
            visualize_tree(buildSyntaxTree(makeStack(separateTokens(tokens))))
            print("Result: ", solve_rpn(makeStack(separateTokens(tokens))))
        else:
            print("Not valid expression: ", line)
        print()
        tokens = []


def start(look, line):
    global parenthesis
    look = line[i]
    if look == "(":
        parenthesis += 1
        look = next(line)
        state0(look, line)


def next(line):
    global i, tokens
    try:
        tokens.append(line[i])
    except:
        pass
    i += 1
    if i >= len(line):
        return "\n"
    else:
        return line[i]


def state0(look, line):
    global parenthesis, tokens
    if look == "(":
        parenthesis += 1
        look = next(line)
        state0(look, line)
    elif look.isdigit():
        look = next(line)
        state1(look, line)
    elif look == "M":
        look = next(line)
        state8(look, line)
    elif look in operations:
        look = next(line)
        state5(look, line)


def state1(look, line):
    if look.isdigit():
        look = next(line)
        state1(look, line)
    elif look.isspace():
        look = next(line)
        state2(look, line)
    elif look == ".":
        look = next(line)
        state11(look, line)


def state2(look, line):
    global parenthesis
    if look.isdigit():
        look = next(line)
        state3(look, line)
    elif look == "M":
        look = next(line)
        state8(look, line)
    elif look == "R":
        look = next(line)
        state13(look, line)
    elif look == "(":
        parenthesis += 1
        look = next(line)
        state0(look, line)
    elif look in operations:
        look = next(line)
        state5(look, line)


def state3(look, line):
    if look.isdigit():
        look = next(line)
        state3(look, line)
    elif look == ".":
        look = next(line)
        state14(look, line)
    elif look.isspace():
        look = next(line)
        state4(look, line)


def state4(look, line):
    if look in operations:
        look = next(line)
        state5(look, line)


def state5(look, line):
    global parenthesis
    if look == ")":
        parenthesis -= 1
        look = next(line)
        state6(look, line)


def state6(look, line):
    global parenthesis
    if look == "\n":
        look = next(line)
        state7(look, line)
    elif look == "(":
        parenthesis += 1
        look = next(line)
        state0(look, line)
    elif look.isspace():
        look = next(line)
        state0(look, line)
    elif look == ")":
        parenthesis -= 1
        look = next(line)
        state6(look, line)
    elif look in operations:
        look = next(line)
        state1(look, line)


def state7(look, line):
    global isValid, parenthesis
    if parenthesis == 0:
        isValid = True


def state8(look, line):
    if look == "E":
        look = next(line)
        state9(look, line)


def state9(look, line):
    global tokens
    if look == "M":
        tokens.append("MEM")
        look = next(line)
        state10(look, line)


def state10(look, line):
    global parenthesis
    if look.isspace():
        look = next(line)
        state10(look, line)
    elif look == ")":
        parenthesis -= 1
        look = next(line)
        state6(look, line)
    elif look == "(":
        parenthesis += 1
        look = next(line)
        state0(look, line)
    elif look in operations:
        look = next(line)
        state5(look, line)
    elif look.isdigit():
        look = next(line)
        state3(look, line)


def state11(look, line):
    if look.isdigit():
        look = next(line)
        state11(look, line)
    elif look.isspace():
        look = next(line)
        state12(look, line)


def state12(look, line):
    global parenthesis
    if look.isdigit():
        look = next(line)
        state3(look, line)
    if look == "(":
        parenthesis += 1
        look = next(line)
        state0(look, line)


def state13(look, line):
    if look == "E":
        look = next(line)
        state15(look, line)


def state14(look, line):
    if look.isspace():
        look = next(line)
        state4(look, line)
    elif look.isdigit():
        look = next(line)
        state14(look, line)


def state15(look, line):
    global tokens
    if look == "S":
        tokens.append("RES")
        look = next(line)
        state5(look, line)


def separateTokens(tokens):
    tokens = "".join(tokens)
    pattern = re.compile(r"\d+\.\d+|\d+|MEM|RES|[()+\-*\/%^]| ")
    return pattern.findall(tokens)


def makeStack(tokens):
    global operations
    stack = []
    for token in tokens:
        try:
            if token == "MEM" or token == "RES" or token in operations:
                stack.append(token)
            elif float(token):
                stack.append(float(token))
        except:
            pass
    return stack


def solve_rpn(expression):
    global MEM, results
    stack = []
    for j in range(len(expression)):
        token = expression[j]
        if token in operations:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                stack.append(a / b)
            elif token == "%":
                stack.append(a % b)
            elif token == "^":
                stack.append(a**b)
        elif token == "MEM":
            try:
                if expression[j + 1] in operations or type(expression[j + 1]) == float:
                    stack.append(MEM)
                else:
                    MEM = stack.pop()
                    stack.append(0.0)
            except:
                MEM = stack.pop()
                stack.append(0.0)
        elif token == "RES":
            try:
                n = int(stack.pop())
                stack.append(results[-n])
            except:
                stack.append(0.0)
        else:
            stack.append(float(token))
    results.append(stack.pop())
    return results[-1]


main()
