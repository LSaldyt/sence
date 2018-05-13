from methods import mini_max, alphabeta
from node    import Node
from random  import randint

x = randint(0, 10)
y = randint(0, 10)
def branches(node):
    return [Node(node.state - x), Node(node.state + y)]

if __name__ == '__main__':
    print(mini_max(Node(0), branches, maximizing=False, depth=3))
    print(alphabeta(Node(0), branches, maximizing=False, depth=3))
