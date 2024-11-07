#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

# RegEx - a regular expression language

from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
  ?start: alt
  ?alt:   seq ("|" seq)+
      |   seq
  ?seq:   rep (rep)+ 
      |   rep
  ?rep:   atom "*" 
      |   atom
  ?atom:  "(" alt ")" 
       |  CHAR 

  %import common.LETTER -> CHAR
  %import common.WS
  %ignore WS
"""
parser = Lark(grammar)

def main():
    while True:
        try:
            str = input("Enter an RE: ")
            tree = parser.parse(str)
            print(tree.pretty(), end="")
        except EOFError:
            break
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
