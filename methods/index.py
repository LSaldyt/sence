from collections import namedtuple

Index = namedtuple('Index', ['i', 'source'])
Index.__str__  = lambda self : str(self.i)
Index.__repr__ = lambda self : str(self)

def RevIndex(l, i, source):
    return Index(len(l) - i, source)
