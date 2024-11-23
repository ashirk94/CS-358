#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

class A:
    x = 1
#    def __init__(self): 
#        self.x = 2
#        print('init A')

class C(A):
#    def __init__(self): 
#        print('init C')
    pass

if __name__ == "__main__":
    c = C()
    print(c.x)
