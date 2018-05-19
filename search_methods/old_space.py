from functools import wraps, partial
from pprint    import pprint
from math      import log10, ceil

from .known import seqsee_analyzed, known_lookup
from .utils import flatten

original = 'x'

# Operators on basic state

def arithmetic(op, a, b):
    return '{} {} {}'.format(a, op, b)

add   = partial(arithmetic, '+')
multi = partial(arithmetic, '*')
sub1  = lambda a, b: arithmetic('-', a, b)
sub2  = lambda a, b: arithmetic('-', b, a)

def repeat(state, n):
    return '[{}] * {}'.format(state, n)

binary_operators = [add, multi, sub1, sub2, repeat]
atom_operators = [partial(op, n) for op in binary_operators for n in range(1, 11)]

pprint([op('x') for op in atom_operators])

# atom = any_of(atom)
# expression = atom
#            | atom + atom
#            | atom * atom
#            | atom - atom

# range = range(atom)
# list = [expression] or range()
# concat = concat(list, list, ..) (up to three lists)
# repeat = repeat(list)

types = ['list', 'atom']



1/0

def better_distance(found, known):
    distances  = [abs(a - b) for a, b in zip(found, known)]
    total = 0
    multiplier = 10
    for d in reversed(distances):
        total += multiplier * d
        multiplier *= 10
    total += 10 * multiplier * abs(len(found) - len(known))
    total = total / (10**(len(distances) + 2))
    return total

#********************************************************************************#
