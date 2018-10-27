
def generate_with(f, N, maxN=2**32):
    included = set()
    excluded = set()
    for i in range(N):
        y = f(i)
        if y > maxN:
            break
        included.add(y)
    i = 0
    while i < max(included) and i < maxN and len(excluded) < N:
        if i not in included:
            excluded.add(i)
        i += 1
    return [(x, True) for x in included] + [(x, False) for x in excluded]
