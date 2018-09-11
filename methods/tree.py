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

def enumerate_relations(inputs, outputs, answer, operators, considering=None):
    if considering is None:
        considering = {Rule([])}
    rules = set()
    for i, x in enumerate(inputs):
        for j, y in enumerate(outputs):
            for name, op in operators.items():
                for previous in considering:
                    if i == 0:
                        rules.add(previous.join(
                                  Rule([Partial(op, [RevIndex(outputs, j, 'outputs'), Index(0, 'arguments')], [op.f(inputs[i], outputs[j])])])))
                    if j == 0:
                        rules.add(previous.join(
                                  Rule([Partial(op, [RevIndex(inputs, i, 'inputs'), Index(0, 'arguments')], [op.f(inputs[i], outputs[j])])])))
                    rules.add(previous.join(
                              Rule([Partial(op, [RevIndex(inputs, i, 'inputs'), RevIndex(outputs, j, 'outputs')], [])])))
    return rules

def tree(inputs, outputs, depth=1):
    considering = None
    for i in range(1, len(inputs)):
        for d in range(depth):
            local_inputs  = inputs[:i + 1]
            local_outputs = outputs[:i]
            local_answer  = outputs[i]
            proposed = enumerate_relations(local_inputs, local_outputs,
                                           answer=local_answer, operators=operators)
            pprint(proposed)
            final = {rule for rule in proposed if rule.guess(local_inputs, local_outputs) == local_answer}
            if final:
                guesses = {f.guess(inputs, outputs) for f in final}
                for f in final:
                    print(f, ' gives:')
                    print(f.guess(inputs, outputs[:-1]))
                    print('correct:', outputs[-1])
                return
            else:
                considering = proposed
