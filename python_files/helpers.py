import itertools

def hom(k, n):
    return list(itertools.product(range(n), repeat=k))
