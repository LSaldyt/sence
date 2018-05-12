

class Node(object):
    def __init__(self, state):
        self.state = state

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Node(%s)" % score(self)

def score(node):
    return node.state
