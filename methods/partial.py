Partial = namedtuple('Partial', ['operator', 'arguments'])
Partial.__str__  = lambda self : self.operator.expand('x', *self.arguments)
Partial.__repr__ = lambda self : str(self)
Partial.__hash__ = lambda self : hash((self.operator, tuple(self.arguments)))

