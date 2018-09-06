
class Partial:
    def __init__(self, operator, arguments):
        self.operator  = operator
        self.arguments = arguments

    def __str__(self):
        return self.operator.expand('x', *self.arguments)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.operator, tuple(self.arguments)))
