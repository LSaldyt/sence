from functools import reduce, wraps, partial

from pprint import pprint
from copy   import deepcopy

from .operator import Operator
from .partial  import Partial
from .index    import Index, RevIndex
from .rule     import Rule

from .arithmetic import operators

def constant(l):
    return len(set(l)) == 1

def enumerate_relations(inputs, outputs, answer, operators):
    rules = set()
    for i, x in enumerate(inputs):
        for j, y in enumerate(outputs):
            for name, op in operators.items():
                if i == 0:
                    rules.add(Rule([Partial(op, [RevIndex(outputs, j, 'outputs'), Index(0, 'arguments')], [op.f(inputs[i], outputs[j])])]))
                if j == 0:
                    rules.add(Rule([Partial(op, [RevIndex(inputs, i, 'inputs'), Index(0, 'arguments')], [op.f(inputs[i], outputs[j])])]))
                rules.add(Rule([Partial(op, [RevIndex(inputs, i, 'inputs'), RevIndex(outputs, j, 'outputs')], [])]))
    return {rule for rule in rules if rule.guess(inputs, outputs) == answer}

def tree(inputs, outputs, depth=3):
    for i in range(1, len(inputs)):
        local_inputs  = inputs[:i + 1]
        local_outputs = outputs[:i]
        local_answer  = outputs[i]
        proposed = enumerate_relations(local_inputs, local_outputs,
                                       answer=local_answer, operators=operators)
        print(proposed)
        print([rule.guess(local_inputs, local_outputs) for rule in proposed])

        print(local_inputs)
        print(local_outputs)
        print(local_answer)
