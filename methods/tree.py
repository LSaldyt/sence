from functools import reduce, wraps

def reverse(f):
    @wraps(f)
    def inner(a, b):
        return f(b, a)
    return inner

def mult(a, b):
    return a * b

def div(a, b):
    return a // b

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

operators = {'{a}+{b}' : add,
             '{a}-{b}' : sub,
             '{a}*{b}' : mult,
             '{a}/{b}' : div,
             '{b}+{a}' : reverse(sub),
             '{b}*{a}' : reverse(div)}

def constant(l):
    return len(set(l)) == 1

def tree(inputs, outputs, working=None):
    working = [] if working is None else working
    pairs = list(zip(inputs, outputs))
    for name, op in operators.items():
        diff = [op(x, y) for x, y in pairs]
        print(diff)
        print(constant(diff))
        if constant(diff) and diff[0] != 0:
            working.append((op, diff[0], name))
        else:
            pass
            #tree(inputs, diff, working)
    print(working)
    for _, base, name in working:
        print('F(x) = ' + name.format(a=base, b='x'))
