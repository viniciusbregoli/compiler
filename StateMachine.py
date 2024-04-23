import re
from Node import *

with open("input.txt", "r") as arquivo:
    linhas = arquivo.readlines()
    arquivo.close()


global i, operations, tokens, parenteses
operations = ["+", "-", "*", "/", "|", "%", "^"]
tokens = []
parenteses = 0


def main():
    global i
    global isValido
    global parenteses
    global tokens
    for linha in linhas:
        i = 0
        parenteses = 0
        isValido = False
        look = ""
        start(look, linha)
        if isValido:
            print("Linha válida: ", linha.replace("\n", ""))
            print("Tokens: ", separarTokens(tokens))
            print(
                "Arvore: ",
            )
            print_tree(build_syntax_tree(montarPilha(separarTokens(tokens))))
        else:
            print("Linha inválida: ", linha)
        print()
        tokens = []


def start(look, linha):
    global parenteses
    look = linha[i]
    if look == "(":
        parenteses += 1
        look = proximo(linha)
        estado0(look, linha)


def proximo(linha):
    global i, tokens
    try:
        tokens.append(linha[i])
    except:
        pass
    i += 1
    if i >= len(linha):
        return "\n"
    else:
        return linha[i]


def estado0(look, linha):
    global parenteses, tokens
    if look == "(":
        parenteses += 1
        look = proximo(linha)
        estado0(look, linha)
    elif look.isdigit():
        look = proximo(linha)
        estado1(look, linha)
    elif look == "M":
        look = proximo(linha)
        estado8(look, linha)
    elif look in operations:
        look = proximo(linha)
        estado5(look, linha)


def estado1(look, linha):
    if look.isdigit():
        look = proximo(linha)
        estado1(look, linha)
    elif look.isspace():
        look = proximo(linha)
        estado2(look, linha)
    elif look == ".":
        look = proximo(linha)
        estado11(look, linha)


def estado2(look, linha):
    global parenteses
    if look.isdigit():
        look = proximo(linha)
        estado3(look, linha)
    elif look == "M":
        look = proximo(linha)
        estado8(look, linha)
    elif look == "R":
        look = proximo(linha)
        estado13(look, linha)
    elif look == "(":
        parenteses += 1
        look = proximo(linha)
        estado0(look, linha)


def estado3(look, linha):
    if look.isdigit():
        look = proximo(linha)
        estado3(look, linha)
    elif look == ".":
        look = proximo(linha)
        estado14(look, linha)
    elif look.isspace():
        look = proximo(linha)
        estado4(look, linha)


def estado4(look, linha):
    if look in operations:
        look = proximo(linha)
        estado5(look, linha)


def estado5(look, linha):
    global parenteses
    if look == ")":
        parenteses -= 1
        look = proximo(linha)
        estado6(look, linha)


def estado6(look, linha):
    global parenteses
    if look == "\n":
        look = proximo(linha)
        estado7(look, linha)
    elif look == "(":
        parenteses += 1
        look = proximo(linha)
        estado0(look, linha)
    elif look.isspace():
        look = proximo(linha)
        estado0(look, linha)
    elif look == ")":
        parenteses -= 1
        look = proximo(linha)
        estado6(look, linha)
    elif look in operations:
        look = proximo(linha)
        estado1(look, linha)


def estado7(look, linha):
    global isValido, parenteses
    if parenteses == 0:
        isValido = True


def estado8(look, linha):
    if look == "E":
        look = proximo(linha)
        estado9(look, linha)


def estado9(look, linha):
    global tokens
    if look == "M":
        tokens.append("MEM")
        look = proximo(linha)
        estado10(look, linha)


def estado10(look, linha):
    global parenteses
    if look.isspace():
        look = proximo(linha)
        estado10(look, linha)
    elif look == ")":
        parenteses -= 1
        look = proximo(linha)
        estado6(look, linha)
    elif look == "(":
        parenteses += 1
        look = proximo(linha)
        estado0(look, linha)
    elif look in operations:
        look = proximo(linha)
        estado5(look, linha)
    elif look.isdigit():
        look = proximo(linha)
        estado3(look, linha)


def estado11(look, linha):
    if look.isdigit():
        look = proximo(linha)
        estado11(look, linha)
    elif look.isspace():
        look = proximo(linha)
        estado12(look, linha)


def estado12(look, linha):
    global parenteses
    if look.isdigit():
        look = proximo(linha)
        estado3(look, linha)
    if look == "(":
        parenteses += 1
        look = proximo(linha)
        estado0(look, linha)


def estado13(look, linha):
    if look == "E":
        look = proximo(linha)
        estado15(look, linha)


def estado14(look, linha):
    if look.isspace():
        look = proximo(linha)
        estado4(look, linha)
    elif look.isdigit():
        look = proximo(linha)
        estado14(look, linha)


def estado15(look, linha):
    global tokens
    if look == "S":
        tokens.append("RES")
        look = proximo(linha)
        estado5(look, linha)


def separarTokens(tokens):
    tokens = "".join(tokens)
    pattern = re.compile(r"\d+\.\d+|\d+|[()+\-*\/]| ")
    return pattern.findall(tokens)


def montarPilha(tokens):
    global operations
    pilha = []
    for token in tokens:
        try:
            if token == "MEM" or token == "RES" or token in operations:
                pilha.append(token)
            elif float(token):
                pilha.append(float(token))
        except:
            pass
    return pilha


def solve_rpn(expression):
    stack = []
    for token in expression:
        if token in ["+", "-", "*", "/"]:
            b = stack.pop()  # Remove e retorna o último item
            a = stack.pop()  # Remove e retorna o penúltimo item
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                stack.append(a / b)
        else:
            stack.append(
                float(token)
            )  # Converte o token para float e adiciona na pilha
    return stack.pop()  # Retorna o resultado final


main()
