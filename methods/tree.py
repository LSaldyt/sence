from functools import reduce, wraps, partial

from pprint import pprint
from copy import deepcopy

from .arithmetic import operators
from .operator import Operator, Partial
from .rule import Rule

def constant(l):
    return len(set(l)) == 1

def enumerate_relations(inputs, outputs, answer, operators):
    rules = set()
    for i, x in enumerate(inputs):
        for j, y in enumerate(outputs):
            for name, op in operators.items():
                rules.add(Rule([op.partial(x, y)]))
    return rules

def tree(inputs, outputs):
    rules = set()
    for i in range(1, len(inputs)):
        local_inputs  = inputs[:i + 1]
        local_outputs = outputs[:i]
        rules = enumerate_relations(local_inputs, local_outputs, answer=outputs[i], operators=operators)
        working = {rule for rule in rules if [rule.apply(x) for x in inputs] == outputs}
        pprint(rules)
        pprint(working)
