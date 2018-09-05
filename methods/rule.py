from copy import deepcopy

from .operator import Partial

class Rule:
    def __init__(self, partials):
        self.partials = deepcopy(partials)

    def __str__(self):
        return ', '.join(map(str, self.partials))

    def __repr__(self):
        return '{}'.format(self)

    def apply(self, *args):
        working = args
        for partial in self.partials:
            working = partial.operator.apply(*partial.arguments, *working)
        return working

    def add(self, partial):
        self.partials.append(partial)

    def expand(self):
        return str(self)
