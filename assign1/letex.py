# <your name>
#

# CS358 Fall'24 Assignment 1 (Part B)
#
# LetEx - an expression language with let binding

from lark import Lark, v_args
from lark.visitors import Interpreter

# 1. Grammar
#
grammar = """

    # ... need code

"""

# Parser
#
# E.g. let x=1 in x+1
#      => let
#           x
#           num   1
#           add
#             var x
#             num 1
#
parser = Lark(grammar)


# 2. Variable environment
#
class Env(dict):
    def extend(self,x,v):
        # ...

    def lookup(self,x): 
        # ... 

    def retract(self,x):
        # ...

env = Env()

# 3. Interpreter
#
# E.g. (for the above example)
#      => 2
#
@v_args(inline=True)
class Eval(Interpreter):

    # ... need code


def main():
    while True:
        try:
            expr = input("Enter a let expr: ")
            tree = parser.parse(expr)
            print(expr)
            print(tree.pretty(), end="")
            print("tree.Eval() =", Eval().visit(tree))
            print()
        except EOFError:
            break
        except Exception as e:
            print("***", e)

if __name__ == '__main__':
    main()
