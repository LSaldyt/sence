from copy import deepcopy
from pprint import pprint

from .operator import Partial


class Rule:
    def __init__(self, partials):
        #pprint(partials)
        self.partials = deepcopy(partials)

    def __str__(self):
        return ', '.join(map(str, self.partials))

    def __repr__(self):
        return '{}'.format(self)

    def __hash__(self):
        return hash(tuple(self.partials))

    def guess(self, inputs, outputs):
        return self.partials[0].apply(inputs, outputs)

    def apply(self, x):
        working = x
        for partial in self.partials:
            working = partial.operator.apply(*partial.arguments, working)
        return working

    def add(self, partial):
        self.partials.append(partial)

    def join(self, other):
        joined = deepcopy(self)
        for partial in other.partials:
            joined.add(partial)
        return joined

    def expand(self):
        return str(self)
