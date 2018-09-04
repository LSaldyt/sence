from .space import space, python_grammar, Sequence
from .check import check, listify1, listify_seq
from .utils import flatten

from pprint import pprint

def hamming_distance(found, known):
    return sum(abs(a - b) for a, b in zip(found, known))

def hamming_length_distance(found, known):
    return (sum(abs(a - b) for a, b in zip(found, known))
            + abs(len(found) - len(known)))

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

def agreement_distance(a, b):
    agreementRatio = max(1, sum(1 for ai, bi in zip(a, b) if ai == bi)) / ((len(a) + len(b)) / 2)
    hammingLen     = hamming_length_distance(a, b)
    return hammingLen / agreementRatio

def branches(current, goal):
    # goal not used
    return space(current, level=1)


distance = agreement_distance
distance = ast_distance
distance = hamming_length_distance

def astar(branches, start, end, distance=distance):
    '''
    branches is a function:
    branches(key, end) -> connected nodes
    start is a syntax element
    end is the desired list
    distance is a heuristic function:
    dist(current, end) -> num
    '''
    to_seq = lambda seq : tuple(listify_seq(seq))

    print(tuple(end))
    seen      = set()
    paths     = {to_seq(start) : start}
    heuristic = lambda node : paths[node].complexity() * distance(node, end)

    while tuple(end) not in paths:
        shortest = min(paths.keys(), key=heuristic)
        smallest = heuristic(shortest)
        print('{:<30} | {:<20} | {}'.format(str(shortest), str(smallest), paths[shortest]._code()))

        seen.add(shortest)

        for item in branches(paths[shortest], end):
            l = item.complexity()
            if (item not in paths or paths[item].complexity() > l) and \
                to_seq(item) not in seen:
                paths[to_seq(item)] = item
        del paths[shortest]

    shortest = min(paths.keys(), key=heuristic)
    smallest = heuristic(shortest)
    print('{:<30} | {:<20} | {}'.format(str(shortest), str(smallest), paths[shortest]._code()))

    return paths[tuple(end)]

def heuristic(problem):
    astar(branches, Sequence(start='list_def'), problem)
