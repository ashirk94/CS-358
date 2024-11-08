# Alan Shirk
#
# CS358 Fall'24 Assignment 2 (Part A)
#
# Expr - an expression language with arithmetic, logical, and 
#        relational operations
#

from lark import Lark, v_args
from lark.visitors import Interpreter

# Grammar
#
grammar = """
  ?start: orex

  ?orex: orex "or" andex       -> orop
       | andex

  ?andex: andex "and" notex    -> andop
        | notex

  ?notex: "not" notex          -> notop
        | relex

  ?relex: expr REL_OP expr     -> relop
       | expr

  ?expr: expr "+" term         -> add
       | expr "-" term         -> sub
       | term         

  ?term: term "*" atom         -> mul
       | term "/" atom         -> div
       | atom

  ?atom: "(" orex ")"
       | NUM                   -> num
       | "True"                -> true
       | "False"               -> false

  REL_OP: "<" | "<=" | ">" | ">=" | "==" | "!="

  %import common.INT           -> NUM
  %ignore " "
"""

parser = Lark(grammar)

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def num(self, val):  
        return int(val)

    def true(self):
        return True

    def false(self):
        return False

    def add(self, x, y): 
        return self.visit(x) + self.visit(y)

    def sub(self, x, y): 
        return self.visit(x) - self.visit(y)

    def mul(self, x, y): 
        return self.visit(x) * self.visit(y)

    def div(self, x, y): 
        return self.visit(x) // self.visit(y)

    def orop(self, x, y): 
        return self.visit(x) or self.visit(y)

    def andop(self, x, y): 
        return self.visit(x) and self.visit(y)

    def notop(self, x): 
        return not self.visit(x)

    def relop(self, left, op_token, right):
        left = self.visit(left)
        right = self.visit(right)
        op = op_token.value

        if op == '<':
            return left < right
        elif op == '<=':
            return left <= right
        elif op == '>':
            return left > right
        elif op == '>=':
            return left >= right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        else:
            raise Exception(f"Unknown operator: {op}")

def main():
    try:
        prog = input("Enter an expr: ")
        tree = parser.parse(prog)
        print(prog)
        print(tree.pretty(), end="")
        print(Eval().visit(tree))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
