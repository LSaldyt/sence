#!/usr/bin/env python3

function_body = \
'''
def f(x):
    return {}
'''

def create_inner(rule):
    print(rule)
    return 'x'

def create(rule):
    return function_body.format(create_inner(rule))

'''
From Seqsee:
A few sequences and their rules:

    Standard
      1 2 3..       (identity)
      1 1 2 2 3 3.. (repeat 2)
      1 2 2 3 3 3.. (repeat x)
      1 1 1 2 1 1 2 1 2 3 1 1 2 1 2 3 1 2 3.. (concat ((recur x - 1) (range 1 x)))
    Full run
      6 1 2 7 1 2 3 8 1 2 3 4 (concat ((x + 1) (range 1 (x + 1))))
    Garden path
      1 4 1 5 1 6.. (concat ([1] (x + 3)))
      1 1 1 2 1 3.. (concat ([1] (x))
      2 1 2 2 2 2 2 3 2 2 4 2 2 5 2.. (concat ([2] x [2]))
      1 2 2 2 2 2 3 2 2 4 2 2 5 2 2.. (concat ([x] [2] [2]))
      1 1 1 2 1 3..     (concat ([1] [x]))
      1 1 1 2 1 3 1 4.. (concat ([1] [x]))
      1 1 1 1 2 2 1 1 2 2 3 3.. (map repeat (range 1 x)))
    Quasi-Periodic
      1 7 1 2 8 1 2 3 9.. (concat ((range 1 x) (x + 6)))
      1 7 5 2 7 8 4 5 3 7 8 9 3 4 5 4 7 8 9 10 2 3 4 5.. (concat (x (range 7 (x + 6)) (range (6 - x) 5 (-1))))
    Seeing as
      1 1 2 3 1 2 2 3 4 1 2 3 3 4 5.. (repeat-xth (range 1 (x + 2)))
      1 2 2 2 2 2 3 2 2 4 2 2 5 2 2.. (x 2 2)
      1 2 2 3 4 4 5 6 7 7 8 9 10 11..
      (1 2) (2 3 4) (4 5 6 7) (7 8 9 10 11)
    Remindings
      1 1 1 2 3 1 2 2 2 3 4 1 2 3 3 3 4 5
      1 1 2 3 1 2 2 3 4 1 2 3 3 4 5
      2 3 3 4 2 3 4 4 5 2 3 4 5 5 6
      1 1 2 3 1 1 2 3 4 1 1 2 3 4 5 (1 (range 1 (x + 2)))
    Primes
      2 3 5 7 11 13
      1 2 2 3 3 5 4 7 5 11
      2 3 4 5 3 4 5 6 7 5 6 7 8 9 10 11
      1 1 2 2 2 3 3 3 3 3
    Human Comparison
      6 2 6 7 2 7 8 2 8
      6 2 6 5 2 5 4 2 4
      6 2 6 7 2 5 8 2 4
      6 2 6 5 2 7 4 2 8

      1 7 19 2 8 19 20 3 9 19 20 21
      1 7 19 2 8 20 21 3 9 22 23 24

Wolfram like labelling of sequences?
'''

print(create('repeate x 2'))
