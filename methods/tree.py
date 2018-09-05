from functools import reduce, wraps, partial

from pprint import pprint
from copy import deepcopy

from .arithmetic import operators
from .operator import Operator
from .partial  import Partial
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

def tree(inputs, outputs, depth=2):
    rules = set()
    solutions = set()
    for d in range(depth):
        new_rules = set()
        working   = set()
        for i in range(1, len(inputs)):
            local_inputs  = inputs[:i + 1]
            local_outputs = outputs[:i]
            rules = enumerate_relations(local_inputs, local_outputs,
                                        answer=outputs[i], operators=operators)
            working.update(  {rule for rule in rules
                              if [rule.apply(x) for x in inputs] == outputs})
            new_rules.update({rule for rule in rules
                              if [rule.apply(x) for x in inputs] != outputs})
        for hypothesis in working:
            if [hypothesis.apply(x) for x in inputs] == outputs:
                solutions.add(hypothesis)

    print('Rules:')
    pprint(rules)
    print('Solutions:')
    pprint(solutions)
