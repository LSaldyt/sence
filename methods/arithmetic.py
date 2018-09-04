from .operator import Operator

def test():
    add  = Operator(lambda a, b : a + b, 2, '{} + {}', 'add')
    radd = add.remap((1, 0))
    print(add)
    print(add.expand(1, 2))
    print(radd)
    print(radd.expand(1, 2))
