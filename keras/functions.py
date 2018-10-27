from functools import wraps

from .sieve import take, gen_primes

def cached_from(d):
    def decorator(f):
        f.__cache__ = d
        @wraps(f)
        def inner(x):
            if x not in f.__cache__:
                f.__cache__[x] = f(x)
            return f.__cache__[x]
        return inner
    return decorator


@cached_from({0 : 1, 1 : 1})
def fibbonacci(x):
    return fibbonacci(x - 1) + fibbonacci(x - 2)

@cached_from({0 : 1, 1 : 1})
def factorial(x):
    return x * factorial(x - 1)

# Recaman numbers:
# a(0) = 0
# for n > 0, a(n) = a(n-1) - n if positive and not already in the sequence,
# otherwise a(n) = a(n-1) + n
__recaman_set__ = set()
@cached_from({0 : 0})
def recaman(n):
    candidate =  recaman(n - 1) - n
    if candidate > 0 and candidate not in __recaman_set__:
        pass
    else:
        candidate = recaman(n - 1) + n
    __recaman_set__.add(candidate)
    return candidate

@cached_from({})
def catalan(n):
    return factorial(2 * n) // (factorial(n) * factorial(n + 1))

@cached_from({})
def prime(n):
    result = take(gen_primes(2), n+1)
    return result[-1]

def alternating(n):
    return int(n % 2 == 0)

functions = {
        'evens'       : lambda x : x * 2,
        'squares'     : lambda x : x ** 2,
        'triangular'  : lambda x : (x * (x - 1)) // 2,
        #'alternating' : alternating,
        'fibonacci'  : fibbonacci,
         'factorial'  : factorial,
         'recaman'    : recaman,
         #'catalan'    : catalan,
         'primes'     : prime
        }
