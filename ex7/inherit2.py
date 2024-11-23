#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

class A:
    def __init__(self): 
        print('init A')

class B1(A):
    def __init__(self): 
        print('init B1')
        super().__init__()

class B2(A):
    def __init__(self): 
        print('init B2')
        super().__init__()

class C(B1,B2):
    def __init__(self): 
        print('init C')
        super().__init__()

if __name__ == "__main__":
    c = C()

