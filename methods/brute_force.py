from .space import python_grammar

from pprint import pprint
from .known import seqsee_analyzed, known_lookup
from .heuristics import better_distance
from .utils import flatten

from .space import pygen

function_template = 'lambda x : {}'

def functify(body, do_flatten=False, a=1, b=3):
    code = function_template.format(body)
    f    = eval(code)
    elements = [f(x) for x in range(a, b)]
    return (code, flatten(elements) if do_flatten else elements)

def match(found, known):
    for a, b in zip(found, known):
        if a != b:
            return False
    return True

def distance(found, known):
    result = 0
    for a, b in zip(found, known):
        result += abs(a - b)
    return result

def match_in(a, bs):
    for b in bs:
        if match(a, b):
            return b
    return None

def gen_all():
    for item in pygen('concat_def'):
        yield item

def brute_force():
    bodies    = gen_all()
    print('Generator created')
    generated = (functify(body, do_flatten=True, a=1, b=6) for body in bodies)
    print('Generation done')
    found = dict()
    i = 0
    for code, elements in generated:
        i += 1
        if len(elements) <= 1:
            continue
        for known in known_lookup.keys():
            #print('Distance {} from {}:'.format(elements, known))
            #print(distance(elements, known))
            #print(better_distance(elements, known))
            if match(elements, known):
                found[tuple(elements)] = code
                #print(code)
                #print(elements)
        print('{}\r'.format(i), end='', flush=True)
    print(i)
    print('Progress:')
    for known, label in known_lookup.items():
        key = match_in(known, found.keys())
        if key is None:
            code = ''
            check = '.'
        else:
            code = found[key]
            check = 'x'
        print('{} {}: {}\n    ({})'.format(check, label, known, code))
