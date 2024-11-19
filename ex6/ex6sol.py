# Alan Shirk
# CS 358
# Exercise 6: Functional Programming

# 1.
def currying(f):
    def curried(a):
        def inner(b):
            return f(a, b)
        return inner
    return curried

# 2.
def ktimes(f, k):
    def repeated_function(x):
        result = x
        for _ in range(k):
            result = f(result)
        return result
    return repeated_function

# 3.
def mymap(f, itr):
    if isinstance(itr, list):
        return list(f(x) for x in itr)
    elif isinstance(itr, tuple):
        return tuple(f(x) for x in itr)
    elif isinstance(itr, set):
        return set(f(x) for x in itr)
    elif isinstance(itr, str):
        return ''.join(f(x) for x in itr)
    else:
        raise TypeError("Unsupported type")

# 4.