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
    prev = []

    def openScope(self):
        self.prev.insert(0,self)
        return Env()
    
    def closeScope(self):
        return self.prev.pop(0)
    
    def extend(self,x,v): 
        assert not x in self, "Variable already defined: " + x
        self[x] = v

    def lookup(self,x): 
        if x in self: return self[x]
        for envi in self.prev:
            if x in envi: return envi[x]
        raise Exception("Variable undefined: " + x)
    
    def update(self,x,v):
        if x in self: self[x] = v; return
        for envi in self.prev:
            if x in envi: envi[x] = v; return
        raise Exception("Variable undefined: " + x)

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

    def funcdecl(self, name, params, body):
        param_list = [param for param in params.children]
        closure = Closure(param_list, body, self.env)
        self.env.extend(name, closure)

    def body(self, *stmts):
        self.env = self.env.openScope()
        for stmt in stmts:
            stmt_result = self.visit(stmt)
            if stmt_result is not None:
                return stmt_result
        self.env = self.env.closeScope()

    def call(self, func_expr, args_expr):
        closure = self.visit(func_expr)
        arg_values = [self.visit(arg) for arg in args_expr.children]

        self.env = closure.env.openScope()
        for param, arg in zip(closure.ids, arg_values):
            self.env.extend(param, arg)
        
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
