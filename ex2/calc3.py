from lark import Lark, v_args, Token
from lark.visitors import Interpreter

# Grammar
grammar = """
?start: expr
?expr: expr "+" term
     | expr "-" term
     | term
?term: term "*" atom
     | term "/" atom
     | atom
?atom: "(" expr ")"
     | NUM

%import common.INT -> NUM
%ignore " "
"""

# Lark parser
parser = Lark(grammar)

@v_args(inline=True)
class Eval(Interpreter):
    def num(self, val):
        return int(val)

    def add(self, left, right):
        return Eval().visit(left) + Eval().visit(right)

    def sub(self, left, right):
        return Eval().visit(left) - Eval().visit(right)

    def mul(self, left, right):
        return Eval().visit(left) * Eval().visit(right)

    def div(self, left, right):
        return Eval().visit(left) / Eval().visit(right)

    # Count AST nodes (operators and numbers)
    def numNodes(self, tree):
        if isinstance(tree, Token):
            return 1  # Leaf node (number)
        count = 1  # Counts current node (operator)
        for child in tree.children:
            count += self.numNodes(child)
        return count

    # Count the number of '1's in the tree
    def count1s(self, tree):
        if isinstance(tree, Token):
            return 1 if tree == "1" else 0  # If the token is '1', count it
        count = 0
        for child in tree.children:
            count += self.count1s(child)
        return count

    # Convert tree to prefix list (both Tree and Token)
    def toList(self, tree):
        if isinstance(tree, Token):
            return int(tree)
        op = tree.data
        return [op] + [self.toList(child) for child in tree.children]

def main():
    while True:
        try:
            prog = input("Enter an expr: ")
            tree = parser.parse(prog)
            print(tree.pretty())  # Visualize the tree structure
            evaluator = Eval()
            print("tree.Eval() =", evaluator.visit(tree))  # Evaluate the expression
            print("tree.numNodes() =", evaluator.numNodes(tree))  # Count the nodes
            print("tree.count1s() =", evaluator.count1s(tree))  # Count how many '1's exist
            print("tree.toList() =", evaluator.toList(tree))  # Convert tree to prefix notation
        except EOFError:
            break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
