from lark import Lark, v_args
from lark.visitors import Interpreter

# 1. Grammar
grammar = """
?start: orex

?orex: orex "or" andex   -> orop
    | andex

?andex: andex "and" atom -> andop
     | atom

?atom: "not" atom        -> notop
    | "(" orex ")"
    | "True"            -> truev
    | "False"           -> falsev

%ignore " "
"""

# 2. Interpreter for Evaluating Boolean Expressions
class Eval(Interpreter):
    def truev(self, tree):
        return True

    def falsev(self, tree):
        return False

    def notop(self, tree):
        expr_val = self.visit(tree.children[0])
        return not expr_val

    def andop(self, tree):
        left_val = self.visit(tree.children[0])
        right_val = self.visit(tree.children[1])
        return left_val and right_val

    def orop(self, tree):
        left_val = self.visit(tree.children[0])
        right_val = self.visit(tree.children[1])
        return left_val or right_val

# 3. Interpreter for Converting AST to List
class toList(Interpreter):
    def truev(self, tree):
        return 'True'

    def falsev(self, tree):
        return 'False'

    def notop(self, tree):
        expr_list = self.visit(tree.children[0])
        return ['not', expr_list]

    def andop(self, tree):
        left_list = self.visit(tree.children[0])
        right_list = self.visit(tree.children[1])
        return ['and', left_list, right_list]

    def orop(self, tree):
        left_list = self.visit(tree.children[0])
        right_list = self.visit(tree.children[1])
        return ['or', left_list, right_list]

# 4. Convert Nested List to a String Form
def strForm(lst):
    if isinstance(lst, list):
        return '(' + ' '.join(strForm(elem) for elem in lst) + ')'
    else:
        return str(lst)

# Main Function
def main():
    parser = Lark(grammar)
    while True:
        try:
            expr = input("Enter a bool expr: ")
            tree = parser.parse(expr)

            evaluated = Eval().visit(tree)
            lst = toList().visit(tree)

            print(expr)
            print(tree.pretty(), end="")
            print("tree.Eval() =", evaluated)
            print("tree.toList() =", lst)
            print("strForm() =", strForm(lst))
            print()
        except EOFError:
            break
        except Exception as e:
            print("***", e)
            print()

if __name__ == '__main__':
    main()
