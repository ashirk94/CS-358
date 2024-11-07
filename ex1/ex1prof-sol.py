#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

# Exercise 1 Solutions
#
# Usage: linux> python3 ex1sol.py
#

# 1. Palindrome

# return true if str is a palindrome
def palindrome1(str):
    return str == str[::-1]

# alternative solution
def palindrome2(str):
    n = len(str)
    for i in range(0,n//2):
        if str[i] != str[n-i-1]:
            return False
    return True

# 2. Stack and queue

# a stack based list
def newstack():
    return []

def push(s, x):
    s.insert(0,x)
    return s

def pop(s):
    return s.pop(0)

# a queue based list
def newqueue():
    return []

def enqueue(q, x):
    q.append(x)
    return q

def dequeue(q):
    return q.pop(0)

# 3. Two versions of factorial

# recursive
def fac1(n):
    if n < 0: return None
    if n < 1: return 1
    return fac1(n-1) * n

# iterative, with a while loop 
def fac2(n):
    if n < 0: return None
    fac = 1
    while n > 1: 
        fac *= n
        n -= 1
    return fac

# 4. Draw AST for expression "1 + 2 * 3 ^ 4 - 5"

# (a) C version: [- [+ 1 [* 2 [^ 3 4]]] 5] => 158
# (b) X version: [^ [* [+ 1 2] 3] [- 4 5]] => 1/9 = 0.111...

# 5. Class definiitions for AST nodes

class add: 
    def __init__(self,x,y): self.x = x; self.y = y
    
class sub: 
    def __init__(self,x,y): self.x = x; self.y = y
    
class mul: 
    def __init__(self,x,y): self.x = x; self.y = y
    
class exp: 
    def __init__(self,x,y): self.x = x; self.y = y
    
class plus: 
    def __init__(self,x,y): self.x = x; self.y = y
    
ctree = sub(add(1, mul(2, exp(3,4))), 5)
xtree = exp(mul(add(1,2), 3), (sub(4,5)))

def main():
    print("palindrome1('aba'):     ", palindrome1('aba'))
    print("palindrome2('++ ** ++'):", palindrome2('++ ** ++'))
    print("palindrome1('12/22/21'):", palindrome1('12/22/21'))
    print("palindrome2(''):        ", palindrome2(''))
    print("palindrome1('abb'):     ", palindrome1('abb'))
    print("palindrome2('123'):     ", palindrome2('123'))

    s = newstack()
    print("s=newstack():", s)
    print("push(s,1):   ", push(s,1))
    print("push(s,2):   ", push(s,2))
    print("pop(s):      ", pop(s))   
    print("pop(s):      ", pop(s))   
    print("s:           ", s)

    q = newqueue()
    print("q=newqueue():", q)
    print("enqueue(q,1):", enqueue(q,1))
    print("enqueue(q,2):", enqueue(q,2))
    print("dequeue(q):  ", dequeue(q))   
    print("dequeue(q):  ", dequeue(q))   
    print("q:           ", q)

    print("fac1(0): ", fac1(0)) 
    print("fac2(0): ", fac2(0)) 
    print("fac1(5): ", fac1(5)) 
    print("fac2(5): ", fac2(5)) 
    print("fac1(-1):", fac1(-1)) 
    print("fac2(-1):", fac2(-1)) 
    
    print("type(ctree):", type(ctree))
    print("type(xtree):", type(xtree))

if __name__ == "__main__":
    main()
