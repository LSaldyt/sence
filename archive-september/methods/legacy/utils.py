def flatten(l):
    if type(l) == int:
        return [l]
    if len(l) > 0 and type(l[0]) == int:
        return l
    return [item for sublist in l for item in sublist]

