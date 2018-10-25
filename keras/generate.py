
def generate_with(f, N):
    included = set()
    excluded = set()
    for i in range(N):
        included.add(f(i))
    i = 0
    while i < max(included) and len(excluded) < N:
        if i not in included:
            excluded.add(i)
        i += 1
    return [(x, True) for x in included] + [(x, False) for x in excluded]

