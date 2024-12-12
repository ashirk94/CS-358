# Alan Shirk
#

# CS358 Fall'24 Assignment 3 (Part B)
#
# ImpLang2

from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
?start: stmt+

stmt: "var" ID "=" expr              -> decl
    | ID "=" expr                    -> assign
    | "if" "(" expr ")" stmt ["else" stmt] -> ifstmt
    | "while" "(" expr ")" stmt      -> whstmt
    | "for" ID "in" range stmt       -> forloop
    | "print" "(" expr ")"           -> prstmt
    | "{" stmt (";" stmt)* "}"       -> block

?range: "[" expr ".." expr "]"       -> rangeexpr

?expr: expr "or" andexpr             -> orop
     | andexpr

?andexpr: andexpr "and" relexpr      -> andop
        | relexpr

?relexpr: aexpr "<" aexpr    -> lt
        | aexpr "==" aexpr   -> eq
        | aexpr "!=" aexpr   -> neq
        | aexpr

?aexpr: aexpr "+" term       -> add
          | aexpr "-" term       -> sub
          | term

?term: term "*" atom                  -> mul
     | term "/" atom                  -> div
     | term "%" atom                  -> mod
     | atom

?atom: "(" aexpr ")"
     | ID                             -> var
     | NUM                            -> num

  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore WS
"""

# With an 'lalr' parser, Lark handles the 'dangling else' 
# case correctly.
parser = Lark(grammar, parser='lalr')

debug = False

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
    
    def mod(self, left, right):
        return self.visit(left) % self.visit(right)

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
        while cond:
            self.visit(body)

    def prstmt(self, expr):
        print(self.visit(expr))

    def block(self, *stmts):
        self.env = self.env.openScope()
        for stmt in stmts:
            self.visit(stmt)
        self.env = self.env.closeScope()

    def lt(self, left, right):
        return self.visit(left) < self.visit(right)

    def eq(self, left, right):
        return self.visit(left) == self.visit(right)
    
    def neq(self, left, right):
        return self.visit(left) != self.visit(right)
    
    def rangeexpr(self, lo, hi):
        lo_val = self.visit(lo)
        hi_val = self.visit(hi)
        return range(lo_val, hi_val)
    
    def forloop(self, loop_var, range_expr, stmt):
        range_values = self.visit(range_expr)
        self.env = self.env.openScope()

        for value in range_values:
            if loop_var in self.env:
                self.env.update(loop_var, value)
            else:
                self.env.extend(loop_var, value)
            self.visit(stmt)     

        self.env = self.env.closeScope()

    def andop(self, left, right):
        return self.visit(left) and self.visit(right)

    def orop(self, left, right):
        return self.visit(left) or self.visit(right)



# A new input routine - sys.stdin.read() 
# - It allows source program be written in multiple lines
#
import sys
def main():
    try:
        prog = sys.stdin.read()
        tree = parser.parse(prog)
        print(prog)
        Eval().visit(tree)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

