#!/usr/bin/env python3
"""
seqsee_analyzed = dict(
standard = '''
1 2 3
1 1 2 2 3 3
1 2 2 3 3 3
1 1 1 2 1 1 2 1 2 3 1 1 2 1 2 3 1 2 3
6 1 2 7 1 2 3 8 1 2 3 4
''',
garden = '''
1 4 1 5 1 6
1 1 1 2 1 3
2 1 2 2 2 2 2 3 2 2 4 2 2 5 2
1 2 2 2 2 2 3 2 2 4 2 2 5 2 2
1 1 1 2 1 3
1 1 1 2 1 3 1 4
1 1 1 1 2 2 1 1 2 2 3 3
''',
quasi_periodic = '''
1 7 1 2 8 1 2 3 9
1 7 5 2 7 8 4 5 3 7 8 9 3 4 5 4 7 8 9 10 2 3 4 5
''',
seeing_as = '''
1 1 2 3 1 2 2 3 4 1 2 3 3 4 5
1 2 2 2 2 2 3 2 2 4 2 2 5 2 2
1 2 2 3 4 4 5 6 7 7 8 9 10 11
''',
remindings = '''
1 1 1 2 3 1 2 2 2 3 4 1 2 3 3 3 4 5
1 1 2 3 1 2 2 3 4 1 2 3 3 4 5
2 3 3 4 2 3 4 4 5 2 3 4 5 5 6
1 1 2 3 1 1 2 3 4 1 1 2 3 4 5
''',
primes = '''
2 3 5 7 11 13
1 2 2 3 3 5 4 7 5 11
2 3 4 5 3 4 5 6 7 5 6 7 8 9 10 11
1 1 2 2 2 3 3 3 3 3
''',
human_comparison = '''
6 2 6 7 2 7 8 2 8
6 2 6 5 2 5 4 2 4
6 2 6 7 2 5 8 2 4
6 2 6 5 2 7 4 2 8
1 7 19 2 8 19 20 3 9 19 20 21
1 7 19 2 8 20 21 3 9 22 23 24
''')

"""
seqsee_analyzed = dict()

with open('problems.txt') as infile:
    seqsee_analyzed['all'] = infile.read()

def process(s):
    lines = filter(lambda line : len(line) > 0, s.split('\n'))
    lines = [list(map(int, line.split(' '))) for line in lines]

    return lines

seqsee_analyzed = {k : process(v) for k, v in seqsee_analyzed.items()}
known_lookup = {tuple(subv) : k for k, v in seqsee_analyzed.items() for subv in v}
