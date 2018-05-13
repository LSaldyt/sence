from .node import Node, score 

inf = float('inf')

def mini_max(node, branches, maximizing=True, depth=1):
    if depth == 0:
        return score(node), [node]
    if maximizing:
        v = -inf
        comp = max
    else:
        v = inf
        comp = min

    result = None 
    bs = branches(node)
    print(depth)
    for b in bs:
        print(b)
    for branch in bs:
        s, r = mini_max(branch, branches, not maximizing, depth - 1)
        if comp(v, s) == s:
            v = s 
            result = r
    return v, [node] + result

def alpha_beta(node, branches, maximizing=True, depth=1, alpha=-inf, beta=inf):
    if depth == 0:
        return score(node), [node] 
    else:
        if maximizing:
            v    = -inf
            comp = max

        else:
            v    = inf
            comp = min

        result = None
        for branch in branches(node):
            s, r = alpha_beta(branch, branches, not maximizing, depth - 1, alpha, beta)
            if comp(v, s) == s:
                v = s
                result = r
            if maximizing:
                alpha = comp(alpha, v)
            else:
                beta  = comp(beta, v)
            if beta <= alpha:
                break
    return v, [node] + result
