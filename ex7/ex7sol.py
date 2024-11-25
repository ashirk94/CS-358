# CS 358
# Alan Shirk - alans@pdx.edu
# Exercise 7: Object-Oriented Programming

# 1.
# (a)

class LambdaExpr: pass

class Var(LambdaExpr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Def(LambdaExpr):
    def __init__(self, param, body):
        self.param = param
        self.body = body

    def __str__(self):
        return f"λ{self.param}.{self.body}"

class App(LambdaExpr):
    def __init__(self, funcExpr, argExpr):
        self.funcExpr = funcExpr
        self.argExpr = argExpr

    def __str__(self):
        funcStr = f"({self.funcExpr})" if isinstance(self.funcExpr, Def) else f"{self.funcExpr}"
        argStr = f"({self.argExpr})" if isinstance(self.argExpr, App) or isinstance(self.argExpr, Def) else f"{self.argExpr}"

        return f"{funcStr}{argStr}"

# (b)
# i.
expr1 = Def(
    "x",
    Def(
        "y",
        App(Var("x"), Var("y"))
    )
)
# ii.
expr2 = App(
    Def(
        "x",
        App(Var("x"), Var("x"))
    ),
    Var("y")
)

# 2
# (a)
# When A's constructor is uncommented, init A and 2 are printed.
# When C's constructor is also uncommented, init C and 1 are printed.
# When only A's constructor is uncommented, it is called because C's constructor is not defined. Therefore x is changed to 2 and init A is printed. When both are uncommented, C's is called instead because it overrides A's constructor. Then x remains 1 and init C is printed.
# (b)
# Each constructor is only called once, while I expected A to be called twice since B1 and B2 both inherit from A. From searching online, I found that Python solves this problem by determining a Method Resolution Order using the C3 Linearization Algorithm.
# (c)
# The outputs matched what I expected due to the fact that the classes would have the same Method Resolution Order as part b. As x is incremented before it is passed to B1, B2, and A, the fields z, y, and x increment by 1 in that order from the original 1 passed into C's constructor.

# 3.
# (a)
# C++ Example
#
# class Overloading {
# public:
#     int multiplyNums(int x, int y) {
#         return x * y;
#     }
#     double multiplyNums(double x, double y) {
#         return x * y;
#     }
# };
# (b)
class Parent:
    def whoami(self):
        return "Parent class"

class Child(Parent):
    def whoami(self):
        return "Child class"
# (c)
# Part b I was able to write in Python because Python supports overriding natively as was shown in problem 2a. Part a on the other hand I could not because Python does not support true method overloading. The C++ overloading example I wrote would not make sense in Python because Python is dynamically typed.
