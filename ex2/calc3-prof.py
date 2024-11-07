#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

# Calc - a calculator language with constants and operations

from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
  ?start: expr

  ?expr: expr "+" term  -> add
       | expr "-" term  -> sub
       | term         

  ?term: term "*" atom  -> mul
       | term "/" atom  -> div
       | atom

  ?atom: "(" expr ")"
       | NUM            -> num

  %import common.INT    -> NUM

  %ignore " "
"""

@v_args(inline=True)
class Eval(Interpreter):
    def num(self, val):  return int(val)
    def add(self, x, y): return Eval().visit(x) + Eval().visit(y)
    def sub(self, x, y): return Eval().visit(x) - Eval().visit(y)
    def mul(self, x, y): return Eval().visit(x) * Eval().visit(y)
    def div(self, x, y): return Eval().visit(x) // Eval().visit(y)

@v_args(inline=True)
class numNodes(Interpreter):
    def num(self, val):  return 1
    def add(self, x, y): return numNodes().visit(x) + numNodes().visit(y) + 1
    def sub(self, x, y): return numNodes().visit(x) + numNodes().visit(y) + 1
    def mul(self, x, y): return numNodes().visit(x) + numNodes().visit(y) + 1
    def div(self, x, y): return numNodes().visit(x) + numNodes().visit(y) + 1

@v_args(inline=True)
class count1s(Interpreter):
    def num(self, val):  return 1 if int(val) == 1 else 0
    def add(self, x, y): return count1s().visit(x) + count1s().visit(y)
    def sub(self, x, y): return count1s().visit(x) + count1s().visit(y)
    def mul(self, x, y): return count1s().visit(x) + count1s().visit(y)
    def div(self, x, y): return count1s().visit(x) + count1s().visit(y)

@v_args(inline=True)
class toList(Interpreter):
    def num(self, val):  return int(val);
    def add(self, x, y): return ['+', toList().visit(x), toList().visit(y)]
    def sub(self, x, y): return ['-', toList().visit(x), toList().visit(y)]
    def mul(self, x, y): return ['*', toList().visit(x), toList().visit(y)]
    def div(self, x, y): return ['/', toList().visit(x), toList().visit(y)]

parser = Lark(grammar)

def main():
    while True:
        try:
            prog = input("Enter an expr: ")
            tree = parser.parse(prog)
            print(tree.pretty(), end="")
            print("tree.Eval() =", Eval().visit(tree))
            print("tree.numNodes() =", numNodes().visit(tree))
            print("tree.count1s() =", count1s().visit(tree))
            print("tree.toList() =", toList().visit(tree))
        except EOFError:
            break
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
