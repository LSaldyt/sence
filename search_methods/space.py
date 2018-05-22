from pprint import pprint
import types

from collections import defaultdict
from copy import deepcopy

python_grammar = dict()

def expand(item):
    if hasattr(item, '_expand'):
        return item._expand()
    else:
        return [item]

def code(item):
    if hasattr(item, '_code'):
        return item._code()
    else:
        return item

class Any:
    def __init__(self, *items):
        self.items = list(items)
        assert len(self.items) > 0, 'Empty items given to "Any" class'
        self.index = 0
        self.state = self.items[self.index]

    def _expand(self):
        for item in self.items:
            for subitem in expand(item):
                yield subitem

    def _code(self):
        return code(self.state)

    def next(self):
        if self.index < len(self.items) - 1:
            self.index += 1
        elif self.index > 0:
            self.index -= 1
        self.state = self.items[self.index]

class Seq:
    def __init__(self, *items):
        self.items = list(items)
        self.state = self.items # necessary

    def _seq_expand(self, s, remaining):
        if len(remaining) == 1:
            last = remaining[0]
            for exp in expand(last):
                yield s + exp
        else:
            first = remaining[0]
            for exp in expand(first):
                for item in self._seq_expand(s + exp, remaining[1:]):
                    yield item

    def _expand(self):
        return self._seq_expand('', self.items)

    def _code(self):
        return ''.join(map(code, self.state))

class Many:
    Limit = 3
    def __init__(self, item):
        self.item = item
        self.amount = 0
        self.state = [self.item] * self.amount

    def _expand(self):
        for i in range(Many.Limit):
            for exp in expand(self.item):
                yield ''.join([exp] * i)

    def _code(self):
        return ''.join(map(code, self.state))

    def increase(self):
        self.amount += 1
        self.state = [self.item] * self.amount

    def decrease(self):
        if self.amount <= 0:
            self.amount -= 1
        self.state = [self.item] * self.amount

class Get:
    def __init__(self, item):
        self.item = item
        self.state = self.item # necessary

    def _expand(self):
        return expand(python_grammar[self.item])

    def _code(self):
        return code(python_grammar[self.state])

def recursive_collect_operators(item, given=None, level=0):
    if given is None:
        given = defaultdict(list)

    if isinstance(item, str):
        return given

    operators = collect_operators(item)
    if len(operators[1]) > 0:
        given[level].append(operators)

    if isinstance(item.state, (list,)):
        for substate in item.state:
            recursive_collect_operators(substate, given, level + 1)
    else:
        recursive_collect_operators(item.state, given, level + 1)
    return given

def collect_operators(state):
    return (state, [func for func in dir(state) if callable(getattr(state, func)) and not func.startswith('_')])

def operators(item):
    for level, outervalue in recursive_collect_operators(item).items():
        for key, value in outervalue:
            for operator in value:
                yield (key, operator)

python_grammar.update(dict(
atom = Any('x', *map(str, range(1, 3))),
expression = Any(Get('atom'),
                 Seq(Get('atom'), ' + ', Get('atom'))),
                 #Seq(Get('atom'), ' * ', Get('atom')),
                 #Seq(Get('atom'), ' - ', Get('atom'))),

repeat       = Seq('[', Get('expression'),'] * (', Get('expression'), ')'),
range_def    = Seq('list(range(', Get('expression'), '))'),
list_literal = Seq('[', Get('expression'), Many(Seq(', ', Get('expression'))), ']'),

list_def     = Any(Get('list_literal'), Get('range_def'), Get('repeat')),
concat_def   = Any(Seq('(', Get('list_def'), ')', Many(Seq(' + (', Get('list_def'), ')'))))
))

#show   = lambda x : pprint(list(expand(x)))
#show_k = lambda x : show(python_grammar[x])


def pygen(name):
    return python_grammar[name]._expand()

def space(start=python_grammar['concat_def'], level=4, current=None):
    if current is None:
        current = set()
    if level == 0:
        return current
    else:
        current.add(code(start))
        for key, operator in operators(start):
            state = deepcopy(start)
            getattr(key, operator)()
            current.add(code(state))
            space(state, level-1, current)
    return current

pprint(space())
