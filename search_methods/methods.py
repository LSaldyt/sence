'''
Reference methods for maze-solving
'''

point_distance = lambda current, end : sqrt((end[0] - current[0]) ** 2 + (end[1] - current[1]) ** 2)

def hill_climbing(branches, current, end, seen=None, distance=point_distance):
    if seen is None:
        seen = [current]
    if end in branches(current, end):
        return seen + [end]
    else:
        possible = sorted([point for point in branches(current, end) if point not in seen],
                        key=lambda p : distance(p, end))
        for next_point in possible:
            result = hill_climbing(branches, next_point, end,
                                   seen=seen +[next_point], distance=distance)
            if result:
                return result
        return []


def beam_search(branches, start, end, width=2, distance=point_distance):
    if start == end:
         return [end]
    seen    = []
    extend  = lambda paths : [path + [p] for path in paths for p in branches(path[-1], end) if p not in path and p not in seen]
    limit   = lambda paths : sorted(paths, key=lambda path : distance(path[-1], end))[:width]
    paths   = limit(extend([[start]]))
    results = [path for path in paths if path[-1] == end]

    while len(results) < 1:
        results = [path for path in paths if path[-1] == end]
        paths   = limit(extend(paths))
        seen    = seen + [path[-1] for path in paths]

    if len(results) > 0:
        return results[0]
    else:
        return []

def branch_and_bound(branches, start, end):
    if start == end:
         return [end]
    paths = { start : Path(0, [start])}

    while end not in paths:
        shortest = min([(paths[key][0], key) for key in paths])
        for p in branches(shortest[1], end):
            if p not in paths:
                paths[p] = (shortest[0]+1, paths[shortest[1]][1] + [p])
            elif paths[p][0] > shortest[0]+1:
                paths[p] = (shortest[0]+1, paths[shortest[1]][1] + [p])
        del paths[shortest[1]]
