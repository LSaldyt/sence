from functools import wraps

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

functions = {
        'evens'      : lambda x : x * 2,
        'squares'    : lambda x : x ** 2,
        'triangular'  : lambda x : (x * (x - 1)) // 2,
        #'fibbonacci' : fibbonacci
        # 'factorial'  : factorial (Grow too fast for neural nets)
        }
