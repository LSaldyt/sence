from pprint import pprint
import types

python_grammar = dict()

def expand(item):
    if hasattr(item, 'expand'):
        return item.expand()
    else:
        return [item]

class Any:
    def __init__(self, *items):
        self.items = items

    def expand(self):
        for item in self.items:
            for subitem in expand(item):
                yield subitem

class Seq:
    def __init__(self, *items):
        self.items = items

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

    def expand(self):
        return self._seq_expand('', self.items)

class Many:
    Limit = 2
    def __init__(self, item):
        self.item = item

    def expand(self):
        for i in range(1, Many.Limit):
            for exp in expand(self.item):
                yield ''.join([exp] * i)

class Get:
    def __init__(self, item):
        self.item = item

    def expand(self):
        return expand(python_grammar[self.item])

python_grammar.update(dict(
atom = Any('x', *map(str, range(1, 11))),
expression = Any(Get('atom'),
                 Seq(Get('atom'), ' + ', Get('atom')),
                 Seq(Get('atom'), ' * ', Get('atom')),
                 Seq(Get('atom'), ' - ', Get('atom'))),

repeat       = Seq('[', Get('atom'),'] * ', Get('atom')),
range_def    = Seq('list(range(', Get('atom'), '))'),
list_literal = Seq('[', Get('atom'), Many(Seq(', ', Get('atom'))), ']'),

list_def     = Any(Get('list_literal'), Get('range_def'), Get('repeat')),
concat_def   = Seq('(', Get('list_def'), ')', Many(Seq(' + (', Get('list_def'), ')'))),
))

pprint(python_grammar)
#pprint(list(expand(python_grammar['atom'])))
#pprint(list(expand(python_grammar['expression'])))
#pprint(list(expand(Seq(Get('atom'), '+', Get('atom')))))
show = lambda x : pprint(list(expand(x)))
show_k = lambda x : show(python_grammar[x])

#show_k('repeat')
#show_k('list_literal')
#show_k('list_def')
#print(len(list(expand(python_grammar['list_def']))))
show_k('concat_def')
