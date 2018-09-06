from functools import reduce, wraps, partial

from pprint import pprint
from copy import deepcopy

from .operator   import Operator
from .partial    import Partial
from .rule       import Rule

from .arithmetic import operators

def constant(l):
    return len(set(l)) == 1

def enumerate_relations(inputs, outputs, answer, operators):
    rules = set()
    for i, x in enumerate(inputs):
        for j, y in enumerate(outputs):
            for name, op in operators.items():
                rules.add(Rule([op.partial(x, y)]))
    return rules

def tree(inputs, outputs, depth=3):
    rules = {Rule([])}
    solutions = set()
    finished = False
    for d in range(depth):
        new_rules = set()
        working   = set()
        for previous_rule in rules:
            for i in range(1, len(inputs)):
                local_inputs  = [previous_rule.apply(x) for x in inputs[:i + 1]]
                local_outputs = outputs[:i]
                rules = enumerate_relations(local_inputs, local_outputs,
                                            answer=outputs[i], operators=operators)
                rules = {previous_rule.join(rule) for rule in rules}

                working.update(  {rule for rule in rules
                                  if [rule.apply(x) for x in inputs] == outputs})
                new_rules.update({rule for rule in rules
                                  if [rule.apply(x) for x in inputs] != outputs})
        for hypothesis in working:
            if [hypothesis.apply(x) for x in inputs] == outputs:
                solutions.add(hypothesis)
                finished = True
        rules.update(new_rules)
        if finished:
            break

    print('Rules:')
    pprint(rules)
    print('Solutions:')
    pprint(solutions)
