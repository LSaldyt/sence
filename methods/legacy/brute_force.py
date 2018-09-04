from .space import python_grammar

from pprint import pprint

from .check import check
from .space import pygen

def distance(found, known):
    result = 0
    for a, b in zip(found, known):
        result += abs(a - b)
    return result

def gen_all():
    for item in pygen('concat_def'):
        yield item

def brute_force():
    bodies    = gen_all()
    check(bodies)
