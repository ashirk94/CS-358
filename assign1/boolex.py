# Alan Shirk
#

# CS358 Fall'24 Assignment 1 (Part A)
#
# BoolEx - a Boolean expression language

from lark import Lark, v_args
from lark.visitors import Interpreter

# 1. Grammar
#
grammar = """
?start: orex
orex: orex "or" andex   -> orop
    | andex
andex: andex "and" atom -> andop
    | atom
atom: "not" atom        -> notop
    | "(" orex ")"
    | "True"            -> truev
    | "False"           -> falsev
"""
# Parser
#
# E.g. (True or not False) and True
#      => andop  
#           orop
#             truev
#             notop
#               falsev
#           truev
#
parser = Lark(grammar)

# 2. Interpreter
#
# E.g. (for the above example)
#      => True
#
@v_args(inline=True)
class Eval(Interpreter):

    # ... need code


# 3. Convert the AST to a list form
#
# E.g. (for the above example)
#      => ['and', ['or', 'True', ['not', 'False']], 'True']
#
@v_args(inline=True)
class toList(Interpreter):

    # ... need code


# 4. Convert a nested list to a string form
#
# E.g. (for the above example)
#      => (and (or True (not False)) True)
#
def strForm(lst):

    # ... need code


def main():
    while True:
        try:
            expr = input("Enter a bool expr: ")
            tree = parser.parse(expr)
            lst = toList().visit(tree)
            print(expr)
            print(tree.pretty(), end="")
            print("tree.Eval() =", Eval().visit(tree))
            print("tree.toList() =", lst)
            print("strForm() =", strForm(lst))
            print()
        except EOFError:
            break
        except Exception as e:
            print("***", e)

if __name__ == '__main__':
    main()
