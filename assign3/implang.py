# Alan Shirk
#

# CS358 Fall'24 Assignment 3 (Part A)
#
# ImpLang - a simple imperative language with nested scopes

# ImpLang - an imperative language
#
#   prog -> stmt
#
#   stmt -> "var" ID "=" expr
#         | ID "=" expr 
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

grammar = """
  ?start: stmt

   stmt: "var" ID "=" expr         -> decl
       | ID "=" expr               -> assign
       | "if" "(" expr ")" stmt ["else" stmt] -> ifstmt
       | "while" "(" expr ")" stmt -> whstmt
       | "print" "(" expr ")"      -> prstmt
       | "{" stmt (";" stmt)* "}"  -> block      

  ?expr: expr "+" term  -> add
       | expr "-" term  -> sub
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

# With an 'lalr' parser, Lark handles the 'dangling else' 
# case correctly.
parser = Lark(grammar, parser='lalr')

debug = False

# Variable environment
#
class Env(dict):

    # ... need code

env = Env()

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def num(self, val): 
        return int(val)

    # ... need code

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

