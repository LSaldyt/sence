

class Partial:
    def __init__(self, operator, indices, arguments):
        self.operator  = operator
        self.arguments = arguments
        self.indices   = indices

    def __str__(self):
        format_source_str = lambda s : 'x' if s == 'inputs' else 'y'
        format_index = lambda i : (format_source_str(self.indices[i].source) + '_n-{}'.format(self.indices[i])
                                   if self.indices[i].source != 'arguments' else
                                   str(self.arguments[self.indices[i].i]))
        return self.operator.expand(format_index(0), format_index(1))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.operator, tuple(self.arguments)))

    def retrieve(self, index, inputs, outputs):
        if index.source == 'inputs':
            return inputs[-index.i]
        elif index.source == 'outputs':
            return outputs[-index.i]
        elif index.source == 'arguments':
            return self.arguments[-index.i]
        else:
            raise ValueError('Index.source must be inputs, outputs or arguments')

    def apply(self, inputs, outputs):
        return self.operator.apply(*map(lambda i : self.retrieve(i, inputs, outputs), self.indices))
