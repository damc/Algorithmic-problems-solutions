"""Solve find-the-access-codes

Time complexity: n^2,
Space complexity: n
n - length of the list
"""


def solution(l):
    """Solve find-the-access-codes

    The algorithm is based on the observation that a "lucky triple" can
    be only created out of adding another number to a "lucky pair". The
    added number must be multiplication of the previous number.

    If we find a number that divides another number, then we can create
    a "lucky triple" by adding that number to each "lucky pair", in which
    the divisor is the second number.
    """
    pairs = [0] * len(l)
    triples = [0] * len(l)
    for i in range(len(l)):
        for j in range(i + 1, len(l)):
            if l[j] >= l[i] and l[j] % l[i] == 0:
                pairs[j] += 1
                triples[j] += pairs[i]

    return sum(triples)
