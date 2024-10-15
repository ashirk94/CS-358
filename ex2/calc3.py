# CS 358
# Alan Shirk - alans@pdx.edu
# Exercise 2: Parser Generation and AST Processing

from lark import Lark, v_args, Token
from lark.visitors import Interpreter

# Lark grammar for calculator
grammar = """
?start: expr
?expr: expr "+" term -> add
     | expr "-" term -> sub
     | term
?term: term "*" atom -> mul
     | term "/" atom -> div
     | atom
?atom: "(" expr ")"
     | NUM -> num

%import common.INT -> NUM
%ignore " "
"""

# Lark parser
parser = Lark(grammar)

# Calculator Interpreter
@v_args(inline=True)
class Eval(Interpreter):
    def num(self, val):
        return int(val)

    def add(self, left, right):
        return self.visit(left) + self.visit(right)

    def sub(self, left, right):
        return self.visit(left) - self.visit(right)

    def mul(self, left, right):
        return self.visit(left) * self.visit(right)

    def div(self, left, right):
        return self.visit(left) / self.visit(right)

    # Counts AST nodes
    def numNodes(self, tree):
        if tree.data in {"add", "sub", "mul", "div"}:
            count = 1  # Operator node
            for child in tree.children:
                count += self.numNodes(child)  # Recursively counts child nodes
            return count
        
        if tree.data == "num":  # Number node
            return 1
        
        return 0  # Ignores other nodes

    # Counts the number of 1s in the tree
    def count1s(self, tree):
        if isinstance(tree, Token):
            return 1 if tree == "1" else 0  # Only counts if the token is 1
        count = 0
        for child in tree.children:
            count += self.count1s(child)
        return count

    # Converts tree to a prefix list
    def toList(self, tree):
        if isinstance(tree, Token):
            return int(tree)
        
        # Map for operator symbols
        op_map = {
            "add": "+",
            "sub": "-",
            "mul": "*",
            "div": "/"
        }

        if tree.data == "num":
            return self.toList(tree.children[0])  # Returns integer without 'num'

        return [op_map.get(tree.data, tree.data)] + [self.toList(child) for child in tree.children]

def main():
    while True:
        try:
            prog = input("Enter an expr: ")
            tree = parser.parse(prog)
            print(tree.pretty())
            evaluator = Eval()
            print("tree.Eval() =", evaluator.visit(tree))
            print("tree.numNodes() =", evaluator.numNodes(tree))
            print("tree.count1s() =", evaluator.count1s(tree))
            print("tree.toList() =", evaluator.toList(tree))
        except EOFError:
            break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
