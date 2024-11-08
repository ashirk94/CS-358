# Alan Shirk
#

# CS358 Fall'24 Assignment 2 (Part B)
#
# Stmt - a language with simple statements
#
#   prog -> stmt
#
#   stmt -> ID "=" expr 
#         | "if" "(" expr ")" stmt ["else" stmt]
#         | "while" "(" expr ")" stmt
#         | "print" "(" expr ")"
#         | "{" stmt (";" stmt)* "}" 
#
#   expr -> expr "+" term
#         | expr "-" term
#         | term         
#
#   term -> term "*" atom
#         | term "/" atom
#         | atom
#
#   atom: "(" expr ")"
#         | ID
#         | NUM
#
from lark import Lark, v_args
from lark.visitors import Interpreter

# Grammar
#
grammar = """
  ?start: stmt (";" stmt)* [";"]

  ?stmt: ID "=" expr                          -> assign
       | "if" "(" expr ")" stmt ["else" stmt] -> if_stmt
       | "while" "(" expr ")" stmt            -> while_stmt
       | "print" "(" expr ")"                 -> print_stmt
       | "{" (stmt (";" stmt)* [";"])? "}"    -> block

  ?expr: expr "<=" term                       -> le
       | expr "<" term                        -> lt
       | expr ">=" term                       -> ge
       | expr ">" term                        -> gt
       | expr "==" term                       -> eq
       | expr "!=" term                       -> ne
       | expr "+" term                        -> add
       | expr "-" term                        -> sub
       | term

  ?term: term "*" atom                        -> mul
       | term "/" atom                        -> div
       | atom

  ?atom: "(" expr ")"
       | ID                                   -> var
       | NUM                                  -> num

  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore WS
"""

parser = Lark(grammar, parser="lalr")

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def __init__(self):
        super().__init__()
        self.env = {}

    def num(self, val):
        return int(val)

    def var(self, name):
        return self.env.get(str(name), 0)

    def assign(self, name, expr):
        value = self.visit(expr)
        self.env[str(name)] = value
        return value

    def add(self, x, y):
        return self.visit(x) + self.visit(y)

    def sub(self, x, y):
        return self.visit(x) - self.visit(y)

    def mul(self, x, y):
        return self.visit(x) * self.visit(y)

    def div(self, x, y):
        return self.visit(x) // self.visit(y)

    def if_stmt(self, condition, true_stmt, false_stmt=None):
        if self.visit(condition) != False:
            return self.visit(true_stmt)
        elif false_stmt:
            return self.visit(false_stmt)

    def while_stmt(self, condition, body):
        while self.visit(condition) != False:
            self.visit(body)

    def print_stmt(self, expr):
        value = self.visit(expr)
        print(value)
        return value

    def block(self, *statements):
        for stmt in statements:
            if isinstance(stmt, list):
                for s in stmt:
                    self.visit(s)
            else:
                self.visit(stmt)

    def le(self, x, y): 
        return self.visit(x) <= self.visit(y)

    def lt(self, x, y): 
        return self.visit(x) < self.visit(y)

    def ge(self, x, y): 
        return self.visit(x) >= self.visit(y)

    def gt(self, x, y): 
        return self.visit(x) > self.visit(y)

    def eq(self, x, y): 
        return self.visit(x) == self.visit(y)

    def ne(self, x, y): 
        return self.visit(x) != self.visit(y)

def main():
    try:
        prog = input("Enter a program: ")
        tree = parser.parse(prog)
        print(prog)
        print(tree.pretty(), end="")
        print(Eval().visit(tree))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

