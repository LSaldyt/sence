from collections import namedtuple

Index = namedtuple('Index', ['i', 'source'])

def RevIndex(l, i, source):
    return Index(len(l) - i, source)
