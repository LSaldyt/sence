from .known import seqsee_analyzed, known_lookup
from .utils import flatten
from .space import code

function_template = 'lambda x : {}'

def listify(body, do_flatten=False, a=1, b=3):
    code = function_template.format(body)
    f    = eval(code)
    elements = [f(x) for x in range(a, b)]
    return (code, flatten(elements) if do_flatten else elements)

def listify1(*args, **kwargs):
    return listify(code(args[0]), *(args[1:]), **kwargs)[1]

def match(found, known):
    for a, b in zip(found, known):
        if a != b:
            return False
    return True

def match_in(a, bs):
    for b in bs:
        if match(a, b):
            return b
    return None

def check(bodies):
    generated = (listify(body, do_flatten=True, a=1, b=6) for body in bodies)
    print('Generation done')
    found = dict()
    i = 0
    for code, elements in generated:
        i += 1
        if len(elements) <= 1:
            continue
        for known in known_lookup.keys():
            if match(elements, known):
                found[tuple(elements)] = code
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
