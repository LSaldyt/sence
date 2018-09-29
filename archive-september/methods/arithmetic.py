from .operator import Operator

def save_integer_division(a, b):
    if b == 0:
        return 2**32
    else:
        return a // b

__functions__ = [(lambda a, b : a + b,   'add', '+', 'sub'),
                 (lambda a, b : a - b,   'sub', '-', 'add'),
                 (lambda a, b : a * b,   'mul', '*', 'div'),
                 (save_integer_division, 'div', '/', 'mul')]

operators = {t[1] : Operator(t[0], 2, '{} ' + t[2] + ' {}', t[1], t[3]) for t in __functions__}
operators['rdiv'] = operators['div'].remap((1, 0))
operators['rsub'] = operators['sub'].remap((1, 0))
