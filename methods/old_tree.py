from functools import reduce, wraps, partial

from pprint import pprint
from copy import deepcopy

def reverse(f):
    @wraps(f)
    def inner(a, b):
        return f(b, a)
    return inner

def mult(a, b):
    return a * b

def div(a, b):
    if b == 0:
        return 2**32
    return a // b

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

operators = {'add' : add,
             'sub' : sub,
             'mul' : mult,
             'div' : div}

inverses = {'add' : 'sub',
            'mul' : 'div',
            'sub' : 'add',
            'div' : 'mul'}

def constant(l):
    return len(set(l)) == 1

def enumerate_relations(inputs, outputs, answer, operators):
    rules = set()
    for i, x in enumerate(inputs):
        for j, y in enumerate(outputs):
            for name, op in operators.items():
                inv_op_name = inverses[name]
                inv_op      = operators[inv_op_name]
                rel = op(x, y)
                rules.add(partial(inv_op, rel))
                rel = op(y, x)
                rules.add(partial(inv_op, b=rel))

    transforms = {rule for rule in rules if rule(inputs[-1]) != answer}
    rules      = {rule for rule in rules if rule(inputs[-1]) == answer}
    return rules, transforms

def distance(a, b):
    return sum(abs(x-y) for x, y in zip(a, b))

def inner_tree_search(inputs, outputs, depth):
    assert len(inputs) == len(outputs), 'Inputs and outputs must be the same length'
    input_set = {(tuple(), tuple(inputs))}
    next_set  = deepcopy(input_set)
    for d in range(depth):
        print('Recursing to functions of depth {}'.format(d + 1))
        for previous_rules, inputs in sorted(list(input_set), key=lambda t : distance(t[1], outputs)):
            for i in range(1, len(inputs)):
                local_inputs  = inputs[:i + 1]
                local_outputs = outputs[:i]
                rules, transforms = enumerate_relations(local_inputs, local_outputs, answer=outputs[i], operators=operators)
                for partial_rule in transforms:
                    transformed_inputs = list(map(partial_rule, inputs))
                    next_set.add((previous_rules + (partial_rule,), tuple(transformed_inputs)))
                for rule in rules:
                    applied = list(map(rule, inputs))
                    if applied == outputs:
                        print('Finished at depth: ', d + 1)
                        return previous_rules + (rule,)
        input_set.update(next_set)

def tree(inputs, outputs, depth=4):
    rules = inner_tree_search(inputs, outputs, depth)
    print('Started with ', inputs)
    transformed = deepcopy(inputs)
    for rule in rules:
        transformed = list(map(rule, transformed))
        print(rule, ' gave: ')
        print(transformed)
