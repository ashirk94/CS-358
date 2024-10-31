from lark import Lark

grammar = """
    ?start: stmt
    stmt: "if" "expr" stmt ["else" stmt] | "other"

    %ignore " "
"""

parser = Lark(grammar, parser='lalr')

test_case = "if expr if expr other else other"
tree = parser.parse(test_case)
print(tree.pretty())
