# CS 358
# Alan Shirk - alans@pdx.edu
# Exercise 1: AST and Python Programming

# 1.
def palindrome1(str):
    return str == str[::-1]

def palindrome2(str):
    reverse = ""
    i = len(str) - 1
    while i >= 0:
        reverse += str[i]
        i -= 1
    return str == reverse

# 2.
def newstack():
    return []

def newqueue():
    return []

def push(s, x):
    s.append(x)
    return s

def pop(s):
    return s.pop()

def enqueue(q, x):
    q.append(x)
    return q

def dequeue(q):
    return q.pop(0)

# 3.
def fac1(n):
    if n < 0:
        return None
    if n == 0:
        return 1
    else:
        return n * fac1(n - 1)
    
def fac2(n):
    if n < 0:
        return None
    result = 1
    while n > 0:
        result *= n
        n -= 1
    return result

# 4.

"""
a.

[- [+ 1 [* 2 [^ 3 4]]] 5] = 158

b.

[^ [* [+ 1 2] 3] [- 4 5]] = 1/9
"""

# 5.

# Base class for AST nodes
class ASTNode:
    def evaluate(self):
        raise NotImplementedError("This method is only implemented by the subclasses")

# Class for number nodes
class Num(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def evaluate(self):
        return self.value

# Class for addition nodes
class Add(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()

# Class for subtraction nodes
class Sub(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()

# Class for multiplication nodes
class Mul(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()

# Class for exponentiation nodes
class Exp(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def evaluate(self):
        return self.left.evaluate() ** self.right.evaluate()

# Tree structure for building and evaluating the AST
class AST:
    def __init__(self, root=None):
        self.root = root
    
    def evaluate(self):
        if self.root:
            return self.root.evaluate()
        return None

# Construct AST for C precedence
def construct_c_precedence_ast():
    # 1 + (2 * (3 ^ 4)) - 5
    node_exp = Exp(Num(3), Num(4))      # 3 ^ 4
    node_mul = Mul(Num(2), node_exp)    # 2 * (3 ^ 4)
    node_add = Add(Num(1), node_mul)    # 1 + (2 * (3 ^ 4))
    root = Sub(node_add, Num(5))        # (1 + (2 * (3 ^ 4))) - 5
    return AST(root)

# Construct AST for reversed precedence
def construct_reversed_precedence_ast():
    # ((1 + 2) * 3) ^ (4 - 5)
    node_add = Add(Num(1), Num(2))      # 1 + 2
    node_mul = Mul(node_add, Num(3))    # (1 + 2) * 3
    node_sub = Sub(Num(4), Num(5))      # 4 - 5
    root = Exp(node_mul, node_sub)      # ((1 + 2) * 3) ^ (4 - 5)
    return AST(root)

# C Precedence AST
c_ast = construct_c_precedence_ast()
print("C Precedence AST Evaluation:", c_ast.evaluate())  # Output: 158

# Reversed Precedence AST
reversed_ast = construct_reversed_precedence_ast()
print("Reversed Precedence AST Evaluation:", reversed_ast.evaluate())  # Output: 1/9

