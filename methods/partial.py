
class Partial:
    def __init__(self, operator, indices, arguments):
        self.operator  = operator
        self.arguments = arguments
        self.indices   = indices

    def __str__(self):
        format_index = lambda i : '(n-{})'.format(self.indices[i])
        return str(self.operator) + '[x' + format_index(0) + ', y' + format_index(1) + ']'
        #return self.operator.expand('x', *self.arguments)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.operator, tuple(self.arguments)))

    def apply(self, inputs, outputs):
        x = inputs[-self.indices[0]]
        y = outputs[-self.indices[1]]
        return self.operator.apply(x, y)
