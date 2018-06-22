from pprint import pprint
import types

from collections import defaultdict
from copy import deepcopy, copy

_N = 20

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
        return str(item)

class Any:
    def __init__(self, *items):
        self.items = list(items)
        assert len(self.items) > 0, 'Empty items given to "Any" class'
        self.index = 0
        self.state = self.items[self.index]

    def __str__(self):
        return 'Any({})'.format('{}..{}'.format(self.items[0], self.items[-1]))

    def __hash__(self):
        return hash(str(self))

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

    def complexity(self):
        return 1

class Seq:
    def __init__(self, *items):
        self.items = list(items)
        self.state = self.items # necessary

    def __str__(self):
        return 'Seq({})'.format(''.join(map(str, self.state)))

    def __hash__(self):
        return hash(str(self))

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

    def complexity(self):
        return sum(x.complexity() for x in self.items)

class Many:
    Limit = _N
    def __init__(self, item):
        self.item = item
        self.amount = 0
        self.state = self.item
        self.internal = [self.item] * self.amount

    def __str__(self):
        return 'Many({})'.format(self.item)

    def __hash__(self):
        return hash(str(self))

    def _expand(self):
        for i in range(Many.Limit):
            for exp in expand(self.item):
                yield ''.join([exp] * i)

    def _code(self):
        return ''.join(map(code, self.internal))

    def increase(self):
        self.amount += 1
        self.internal = [self.item] * self.amount

    def decrease(self):
        if self.amount <= 0:
            self.amount -= 1
        self.internal = [self.item] * self.amount

    def complexity(self):
        return self.item.complexity() * self.amount

class Get:
    def __init__(self, item):
        self.item = item
        self.copy = None

    @property
    def state(self):
        if self.copy is None:
            self.copy = deepcopy(python_grammar[self.item])
        return self.copy

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        return hash(str(self))

    def _expand(self):
        return expand(self.state)

    def _code(self):
        return code(self.state)

    def complexity(self):
        return self.state.complexity()

class Sequence:
    def __init__(self, starting_size=1, start='concat_def'):
        self.n     = starting_size
        self.state = python_grammar[start]

    def _expand(self):
        return expend(self.state)

    def _code(self):
        return '[{} for x in range(1, 1 + {})]'.format(code(self.state), self.n)

    #def increase(self):
    #    self.n += 1

    #def decrease(self):
    #    if self.n > 1:
    #        self.n -= 1

    def complexity(self):
        return self.state.complexity() + self.n

def recursive_collect_operators(item, given=None, indices=tuple()):
    if given is None:
        given = dict()

    if isinstance(item, (str, list)):
        return given
    given[indices] = collect_operators(item)

    n = item.state
    if isinstance(n, (list,)):
        for i, substate in enumerate(n):
            nextindices = indices + (i,)
            recursive_collect_operators(substate, given, nextindices)
    else:
        nextindices = indices + (-1,)
        recursive_collect_operators(n, given, nextindices)
    return given

def collect_operators(state):
    return [func for func in dir(state) if callable(getattr(state, func)) and not func.startswith('_')]

def operators(item):
    #print(item)
    #pprint(recursive_collect_operators(item))
    for indices, operators in recursive_collect_operators(item).items():
            for operator in operators:
                yield (indices, operator)

def get_state(state, indices):
    #print('Beginning get state')
    #print(repr(state))
    for index in indices:
        #print(index)
        if index == -1:
            state = state.state
        else:
            state = state.state[index]
        #print(repr(state))
    return state


python_grammar.update(dict(
atom = Any('x', *map(str, range(0, _N))),
expression = Any(Get('atom'),
                 Seq(Get('atom'), ' + ', Get('atom')),
                 Seq(Get('atom'), ' * ', Get('atom')),
                 Seq(Get('atom'), ' - ', Get('atom'))),

repeat       = Seq('(', '[', Get('expression'),'] * (', Get('expression'), '))'),
range_def    = Any(Seq('list(range(', Get('expression'), '))'),
                   Seq('list(range(', Get('expression'), ', ', Get('expression'), '))')),
list_literal = Seq('[', Get('expression'), Many(Seq(', ', Get('expression'))), ']'),

list_def     = Any(Get('list_literal'), Get('range_def'), Get('repeat')),
concat_def   = Any(Seq('(', Get('list_def'), ')', Many(Seq(' + (', Get('list_def'), ')'))))
))

#show   = lambda x : pprint(list(expand(x)))
#show_k = lambda x : show(python_grammar[x])


def pygen(name):
    return python_grammar[name]._expand()

def space(start=python_grammar['concat_def'], level=1, current=None):
    if current is None:
        current = set()
    space = [start]
    current.add(start)
    while level > 0:
        nextspace = []
        for item in space:
            for indices, op in operators(item):
                try:
                    nitem = deepcopy(item)
                    state = get_state(nitem, indices)
                    getattr(state, op)()
                    nextspace.append(nitem)
                    current.add(nitem)
                except AttributeError:
                    pass
                except TypeError:
                    pass
                except IndexError:
                    pass
        space = nextspace
        level -= 1
    return current

