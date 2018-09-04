from copy import deepcopy

class Operator:
    def __init__(self, f, nargs, template, name):
        assert template.count('{}') == nargs, 'Template contains wrong number of format locations ("{}"s)'
        self.f           = f
        self.name        = name
        self.nargs       = nargs
        self.template    = template
        self.arg_mapping = tuple(range(nargs))

    def __str__(self):
        return self.name

    def _mapped(self, args):
        return (args[i] for i in self.arg_mapping)

    def remap(self, mapping, name=None):
        copy = deepcopy(self)
        copy.arg_mapping = mapping
        if name is not None:
            copy.name = name
        return copy

    def apply(self, *args):
        assert len(args) == self.nargs
        return self.f(*self._mapped(args))

    def expand(self, *args):
        return self.template.format(*self._mapped(args))