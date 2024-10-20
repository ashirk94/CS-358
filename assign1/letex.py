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
    def extend(self, x, v):
        if x in self:
            self[x].insert(0, v)
        else:
            self[x] = [v]

    def lookup(self,x):
        vals = super().get(x)
        if not vals:
            raise Exception("Undefined variable: " + x)
        return vals[0]

    def retract(self,x):
        assert x in self, "Undefined variable: " + x
        self[x].pop(0)

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

    def let(self, x, value, body):
        val = self.visit(value)
        self.env.extend(x, val)
        
        result = self.visit(body)
        
        self.env.retract(x)
        
        return result

    def var(self, id):
        return self.env.lookup(id)

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
