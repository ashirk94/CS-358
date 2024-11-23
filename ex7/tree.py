#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

import sys

class T: pass

class T0(T):
    def __init__(self,x): self.x = x

    def sum(self): return self.x
    def equal(self,other): return other.eqT0(self)
    def eqT0(self,other): return self.x == other.x
    def eqT2(self, other): return False

class T2(T):
    def __init__(self,x,left,right):
        self.x = x
        self.left = left
        self.right = right

    def sum(self):
        return self.x + self.left.sum() + self.right.sum()

    def equal(self,other):
        return other.eqT2(self)

    def eqT0(self, other): return False

    def eqT2(self,other):
        return self.x == other.x \
            and self.left.equal(other.left) \
            and self.right.equal(other.right)

if __name__ == "__main__":
    t1 = T2(1,T0(2),T2(4,T0(0),T0(3)))
    t2 = T2(1,T0(2),T2(4,T0(0),T0(3)))
    t3 = T2(1,T0(2),T0(0))
    print("t1.sum() =", t1.sum())
    print("t3.sum() =", t3.sum())
    print("t1.equal(t2):", t1.equal(t2))
    print("t1.equal(t3):", t1.equal(t3))
