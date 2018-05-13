from pprint import pprint
from .known import seqsee_analyzed, known_lookup
from .space import better_distance
from .utils import flatten

function_template = 'lambda x : {}'

atoms = ['x'] + list(map(str, range(1, 3)))
operators = ['+', '-', '*']
commutative = ['+', '*']

# atom = any_of(atom)
# expression = atom
#            | atom + atom
#            | atom * atom
#            | atom - atom

# range = range(atom)
# list = [expression] or range()
# concat = concat(list, list, ..) (up to three lists)
# repeat = repeat(list)

def both(a, b):
    for item in a:
        yield item
    for item in b:
        yield item

'''
The following functions simulate enumeration across a subset of the python grammar
'''

def gen_atoms():
    for atom in atoms:
        yield atom

def gen_expression():
    for a in atoms:
        yield a
        for b in atoms:
            for operator in operators:
                if a == 'x' or b == 'x':
                    if operator in commutative and a > b:
                        yield '{} {} {}'.format(a, operator, b)
                    else:
                        yield '{} {} {}'.format(a, operator, b)

def gen_range():
    for a in gen_expression():
        for b in gen_expression():
            yield 'list(range({}, {}))'.format(a, b)

def gen_repeat():
    for a in gen_expression():
        for b in gen_expression():
            yield '[{}] * ({})'.format(a, b)

def gen_concat():
    for a in gen_expression():
        for b in gen_expression():
            yield '[{}] + [{}]'.format(a, b)
            for c in gen_expression(): # To arbitrary depth
                yield '[{}] + [{}] + [{}]'.format(a, b, c)
        for b in both(gen_range(), gen_repeat()):
            yield '[{}] + ({})'.format(a, b)
    for a in both(gen_range(), gen_repeat()):
        for b in gen_expression():
            yield '({}) + [{}]'.format(a, b)
        for b in both(gen_range(), gen_repeat()):
            yield '({}) + ({})'.format(a, b)

def gen_all():
    return (list(gen_expression()) +
            list(gen_range()) +
            list(gen_concat()) +
            list(gen_repeat()))

def functify(body, do_flatten=False, a=1, b=3):
    code = function_template.format(body)
    f = eval(code)
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
            print('Distance {} from {}:'.format(elements, known))
            print(distance(elements, known))
            print(better_distance(elements, known))
            if match(elements, known):
                found[tuple(elements)] = code
                #print(code)
                #print(elements)
        print('{}/450054\r'.format(i), end='', flush=True)
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
