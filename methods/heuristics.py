def better_distance(found, known):
    distances  = [abs(a - b) for a, b in zip(found, known)]
    total = 0
    multiplier = 10
    for d in reversed(distances):
        total += multiplier * d
        multiplier *= 10
    total += 10 * multiplier * abs(len(found) - len(known))
    total = total / (10**(len(distances) + 2))
    return total
