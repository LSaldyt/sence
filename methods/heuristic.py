from .space import space, python_grammar
from .check import check, listify1
from .utils import flatten

from pprint import pprint

def list_distance(found, known):
    print(found)
    print(known)
    distances  = [abs(a - b) for a, b in zip(found, known)]
    total = 0
    multiplier = 10
    for d in reversed(distances):
        total += multiplier * d
        multiplier *= 10
    total += 10 * multiplier * abs(len(found) - len(known))
    total = total / (10**(len(distances) + 2))
    return total

def ast_distance(a, b):
    print(listify1(a))
    print(b)
    return list_distance(flatten(listify1(a)), b)

def branches(current, goal):
    # goal not used
    return space(current, level=1)

#def astar(branches, start, end, distance=point_distance):
#    paths = { start : Path(0, [start])}
#
#    heuristic = lambda point : paths[point].len * distance(point, end)
#
#    while end not in paths:
#        # min element of keys sorted by heuristic:
#        shortestKey = min([key for key in paths], key=heuristic)
#
#        for adj in branches(shortestKey, end):
#            l = paths[shortestKey].len + 1
#            # add the path if it doesn't exist, update it if a shorter one is found:
#            if adj not in paths or paths[adj].len > l:
#                paths[adj] = Path(l, paths[shortestKey].path + [adj])
#        del paths[shortestKey] # the path to the previously shortest node is now unneeded
#    return paths[end].path

def astar(branches, start, end, distance=ast_distance):
    '''
    branches is a function:
    branches(key, end) -> connected nodes
    start is a syntax element
    end is the desired list
    distance is a heuristic function:
    dist(current, end) -> num
    '''
    paths     = {start : [start]}
    heuristic = lambda node : len(paths[node]) * distance(node, end)

    while True:
        shortest = min(paths.keys(), key=heuristic)
        print(shortest)
        #items = list(map(listify1, branches(start, end)))
        #pprint(items)
        items = branches(start, end)
        for item in branches(start, end):
            if listify1(item) == end:
                return paths[shortest] + item
            l = len(paths[shortest]) + 1
            if item not in paths or len(paths[item]) > 1:
                paths[item] = paths[shortest] + [item]
                #print(item)
                #print(heuristic(item))
        del paths[shortest]

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
