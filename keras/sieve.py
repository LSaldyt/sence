# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/
# Edited by Lucas Saldyt, 25 Sep 2018

def gen_numbers(start=2, primes=True):
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    D = {}

    # The running integer that's checked for primeness
    q = start

    while True:
        #print(q)
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            if primes:
                yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            if not primes:
                yield q
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        q += 1

def gen_primes(start=2):
    for item in gen_numbers(start, primes=True):
        yield item

def gen_composites(start=2):
    for item in gen_numbers(start, primes=False):
        yield item


import itertools
take = lambda l, N : list(itertools.islice(l, N))
