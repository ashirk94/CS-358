# CS 358
# Alan Shirk - alans@pdx.edu
# Exercise 2: Parser Generation and AST Processing

from lark import Lark

# Lark grammar for regex
grammar = """
?start: seq

seq: rep+

rep: LETTER STAR?
    | "(" seq ")" STAR?

STAR: "*"

%import common.LETTER
%ignore " "
"""

# Lark parser
parser = Lark(grammar)

def main():
    while True:
        try:
            expr = input("Enter an RE: ")
            tree = parser.parse(expr)
            print(tree.pretty())
        except EOFError:
            break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
