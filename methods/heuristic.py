from .space import space, python_grammar
from .check import check, listify1
from .utils import flatten

from pprint import pprint

def list_distance(found, known):
    #print(found)
    #print(known)
    distances  = [abs(a - b) for a, b in zip(found, known)]
    total = 0
    factor = 10
    multiplier = factor
    for d in reversed(distances):
        total += multiplier * d
        multiplier *= factor
    total += (multiplier * factor) * abs(len(found) - len(known))
    total = total / (factor**(len(distances) + 2))
    return total

#def list_distance(found, known):
#    dist = abs(len(found) - len(known))
#    dist += sum(abs(a - b) for a, b in zip(found, known))
#    return dist

def ast_distance(a, b):
    #print(listify1(a))
    #print(b)
    #return list_distance(flatten(listify1(a)), b)
    return list_distance(a, b)

def branches(current, goal):
    # goal not used
    return space(current, level=1)

to_seq = lambda x : tuple(flatten(listify1(x)))

def astar(branches, start, end, distance=ast_distance):
    '''
    branches is a function:
    branches(key, end) -> connected nodes
    start is a syntax element
    end is the desired list
    distance is a heuristic function:
    dist(current, end) -> num
    '''

    print(tuple(end))
    seen      = set()
    paths     = {to_seq(start) : start}
    heuristic = lambda node : paths[node].complexity() * distance(node, end)

    while tuple(end) not in paths:
        shortest = min(paths.keys(), key=heuristic)
        smallest = heuristic(shortest)
        print(shortest)
        print(smallest)

        seen.add(shortest)

        for item in branches(paths[shortest], end):
            l = item.complexity()
            if (item not in paths or item.complexity() > l) and \
                to_seq(item) not in seen:
                paths[to_seq(item)] = item
        del paths[shortest]

    return paths[tuple(end)]

#def ast_distance(a, b):

#pprint(space(level=5))
#pprint(space(python_grammar['atom'], level=5))
#pprint(space(python_grammar['expression'], level=2))
#pprint(space(python_grammar['expression'], level=5))
#pprint(space(python_grammar['list_def'], level=5))
#pprint(space(python_grammar['concat_def'], level=4))


def heuristic():
    #check(space(python_grammar['concat_def'], level=2))
    astar(branches, python_grammar['concat_def'], [2, 3, 4, 5])
