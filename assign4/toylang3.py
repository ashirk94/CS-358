# Alan Shirk
#

# CS358 Fall'24 Assignment 4 (Part C)
#
# ToyLang3
#
#   prog -> stmt
#
#   stmt -> "var" ID "=" expr
#         | "print" "(" expr ")"
#         | "{" stmt (";" stmt)* "}" 
#
#   expr -> "lambda" ID ":" expr
#         | expr "(" expr ")"
#         | aexpr 
#
#   aexpr -> aexpr "+" term
#          | aexpr "-" term
#          | term         
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

grammar = """
  ?start: stmt

  stmt: "var" ID "=" expr             -> decl
       | "def" ID "(" idlist ")" "=" body -> funcdecl
       | ID "=" expr                  -> assign
       | "if" "(" expr ")" stmt ["else" stmt] -> ifstmt
       | "while" "(" expr ")" stmt    -> whstmt
       | "print" "(" expr ")"         -> prstmt
       | "{" stmt (";" stmt)* "}"     -> block
       | "return" expr                -> returnstmt

  body: "{" (stmt ";")* "return" expr "}"

  idlist: ID ("," ID)* -> idlist

  ?expr: "lambda" ID ":" expr    -> func
       | expr "(" explist ")"    -> call
       | relexpr

  explist: expr ("," expr)* -> explist

  ?relexpr: aexpr "<" aexpr -> lt
          | aexpr "==" aexpr   -> eq
          | aexpr "!=" aexpr   -> neq
          | aexpr ">" aexpr    -> gt
          | aexpr

  ?aexpr: aexpr "+" term  -> add
       | aexpr "-" term   -> sub
       | term

  ?term: term "*" atom  -> mul
       | term "/" atom  -> div
       | atom

  ?atom: "(" expr ")"
       | ID             -> var
       | NUM            -> num

  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore WS
"""

parser = Lark(grammar, parser='lalr')

# Variable environment
#
class Env(dict):
    def __init__(self, prev=None):
        self.prev = prev

    def openScope(self):
        return Env(prev=self)

    def closeScope(self):
        return self.prev

    def extend(self, x, v):
        if x in self:
            raise Exception(f"Variable '{x}' is already defined in the current scope")
        self[x] = v

    def lookup(self, x):
        if x in self:
            return self[x]
        elif self.prev is not None:
            return self.prev.lookup(x)
        else:
            raise Exception(f"Undefined variable: {x}")

    def update(self, x, v):
        if x in self:
            self[x] = v
            return
        elif self.prev is not None:
            self.prev.update(x, v)
            return
        else:
            raise Exception(f"Undefined variable: {x}")

    def display(self, msg):
        print(msg, self, self.prev)

env = Env()

# Closure
#
class Closure:
    def __init__(self, ids, body, env):
        self.ids = ids
        self.body = body
        self.env = env

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def __init__(self):
        self.env = env

    def num(self, val):
        return int(val)

    def var(self, name):
        return self.env.lookup(name)

    def add(self, left, right):
        return self.visit(left) + self.visit(right)

    def sub(self, left, right):
        return self.visit(left) - self.visit(right)

    def mul(self, left, right):
        return self.visit(left) * self.visit(right)

    def div(self, left, right):
        return self.visit(left) // self.visit(right)

    def decl(self, name, value):
        self.env.extend(name, self.visit(value))

    def assign(self, name, value):
        self.env.update(name, self.visit(value))

    def ifstmt(self, cond, then_stmt, else_stmt=None):
        if self.visit(cond):
            self.visit(then_stmt)
        elif else_stmt:
            self.visit(else_stmt)

    def whstmt(self, cond, body):
        while self.visit(cond):
            self.visit(body)

    def prstmt(self, expr):
        print(self.visit(expr))

    def returnstmt(self, expr):
        return self.visit(expr)

    def block(self, *stmts):
        self.env = self.env.openScope()
        for stmt in stmts:
            self.visit(stmt)
        self.env = self.env.closeScope()

    def func(self, param, body):
        return Closure(param, body, self.env)

    def funcdecl(self, name, param, body):
        closure = Closure(param, body, self.env)
        self.env.extend(name, closure)

    def body(self, *stmts):
        self.env = self.env.openScope()
        for stmt in stmts:
            stmt_result = self.visit(stmt)
            if stmt_result is not None:
                return stmt_result
        self.env = self.env.closeScope()

    def call(self, func_expr, arg_expr):
        closure = self.visit(func_expr)
        arg_value = self.visit(arg_expr)

        self.env = closure.env.openScope()
        self.env.extend(closure.id, arg_value)
        return_value = self.visit(closure.body)
        self.env = self.env.closeScope()

        return return_value

    def lt(self, left, right):
        return self.visit(left) < self.visit(right)

    def eq(self, left, right):
        return self.visit(left) == self.visit(right)

    def neq(self, left, right):
        return self.visit(left) != self.visit(right)

    def gt(self, left, right):
        return self.visit(left) > self.visit(right)

import sys
def main():
    try:
        prog = sys.stdin.read()
        tree = parser.parse(prog)
        print(prog, end="")
        Eval().visit(tree)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
