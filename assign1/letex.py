# Alan Shirk
#

# CS358 Fall'24 Assignment 1 (Part B)
#
# LetEx - an expression language with let binding

from lark import Lark, v_args
from lark.visitors import Interpreter

# 1. Grammar
#
grammar = """
?start: let_expr | expr

let_expr: "let" ID "=" start "in" start -> let

?expr: expr "+" term -> add
    | expr "-" term -> sub
    | term

?term: term "*" atom -> mul
    | term "/" atom -> div
    | atom

atom: ID -> var
    | NUM -> num
    | "(" start ")"

%import common.CNAME -> ID
%import common.INT -> NUM
%ignore " "
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
    def extend(self, x, val):
        new_env = Env(self)
        new_env[x] = val
        return new_env

    def lookup(self,x): 
        if x in self:
            return self[x]
        else:
            raise NameError(f"Variable '{x}' not defined")

    def retract(self, x):
        if x in self:
            del self[x]
        else:
            raise NameError(f"Variable '{x}' not found")

env = Env()

# 3. Interpreter
#
# E.g. (for the above example)
#      => 2
#
@v_args(inline=True)
class Eval(Interpreter):
    def __init__(self, env):
        self.env = env

    def let(self, var_name, value_expr, body_expr):
        value = self.visit(value_expr)
        new_env = self.env.extend(var_name, value)
        return Eval(new_env).visit(body_expr)

    def var(self, var_name):
        return self.env.lookup(var_name)

    def num(self, n):
        return int(n)

    def add(self, left, right):
        return Eval(self.env).visit(left) + Eval(self.env).visit(right)

    def sub(self, left, right):
        return Eval(self.env).visit(left) - Eval(self.env).visit(right)

    def mul(self, left, right):
        return Eval(self.env).visit(left) * Eval(self.env).visit(right)

    def div(self, left, right):
        return Eval(self.env).visit(left) / Eval(self.env).visit(right)

def main():
    while True:
        try:
            expr = input("Enter a let expr: ")
            tree = parser.parse(expr)
            print(expr)
            print(tree.pretty(), end="")
            print("tree.Eval() =", Eval(env).visit(tree))
            print()
        except EOFError:
            break
        except Exception as e:
            print("***", e)

if __name__ == '__main__':
    main()
