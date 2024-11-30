class Num:
    def __init__(self,v): self.val = v
    def add(self,other): pass

class Int(Num):
    // ... need code
    
class Str(Num):
    // ... need code

def add(x,y):
    // ... need code

if __name__ == "__main__":
    ival = Int(1)
    sval = Str("2")
    sval2 = Str("3")
    print("add(ival,ival) =", add(ival,ival))
    print("add(ival,sval) =", add(ival,sval))
    print("add(sval,ival) =", add(sval,ival))
    print("add(sval,sval2) =", add(sval,sval2))
    print("ival.add(ival) =", ival.add(ival))
    print("ival.add(sval) =", ival.add(sval))
    print("sval.add(ival) =", sval.add(ival))
    print("sval.add(sval) =", sval.add(sval2))
