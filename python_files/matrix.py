import itertools
import time
import os.path
from .helpers import *

class matrix:

    def __init__(self, rows):

        n = len(rows)
        m = len(rows[0]) - 1
        self.rows = rows
        self.columns = [[rows[j][i] for j in range(n)] for i in range(m)]
        self.right_column = [rows[j][m] for j in range(n)]
        self.interpretation_type = [max(row) + 1 for row in rows]
        self.n = n
        self.m = m

    def __lt__(self, M):
        if self.n < M.n:
            return True
        if self.n > M.n:
            return False
        if self.m < M.m:
            return True
        if self.m > M.m:
            return False

        return self.columns < M.columns

    def __eq__(self, M):
        return self.rows == M.rows

    def __str__(self):
        S = ''
        for r in self.rows:
            for x in r[:self.m]:
                S = S + str(x) + ' '
            S = S + '| ' + str(r[self.m]) + '\n'
        return S

    def __hash__(self):
        return hash(tuple(tuple(r) for r in self.rows))


    # methods used for refinement.
    def rows_lexi(self):
        return all(self.rows[i][:self.m] <= self.rows[i+1][:self.m] for i in range(self.n-1))

    def cols_lexi(self):
        return all(self.columns[i] <= self.columns[i+1] for i in range(self.m-1))

    def double_lexi(self):
        return self.rows_lexi() and self.cols_lexi()

    def is_lextop(self):
        return self.right_column in self.columns

    def is_trivial(self):

        funcs = itertools.product(*[hom(self.interpretation_type[i] + 1, 2) for i in range(self.n)])
        num_cols = self.m + 1

        for f in funcs:
            interpretation = matrix([[f[i][self.rows[i][j]] for j in range(num_cols)] for i in range(self.n)])
            if interpretation.is_lextop():
                continue
            else:
                for i in range(interpretation.n):
                    for j in range(i + 1, self.n):
                        if interpretation.rows[i][:self.m] == interpretation.rows[j][:self.m] and not interpretation.rows[i][self.m] == interpretation.rows[j][self.m]:
                            return True
        return False

    def has_zero_row(self):
        return [0] * (self.m + 1) in self.rows

    def has_duplicate_rows(self):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.rows[i] == self.rows[j]:
                    return True
        return False

    def variables_ordered(self):
        for i in range(self.n):
            L = [0] * self.interpretation_type[i]
            for x in self.rows[i]:
                if not x == 0:
                    L[x] = L[x] + 1
            L = L[1:]
            if not all(L[i] <= L[i + 1] for i in range(len(L) - 1)):
                return False
        return True

    # reductions of self with n rows.
    def reductions(self, n):

        reducts = set()

        for reduct in hom(n, self.n):

            reduction = matrix([self.rows[reduct[i]] for i in range(n)])

            if reduction.is_lextop():
                continue

            reducts.add(reduction)

        return reducts

    # all strict_interpretations of all reductions in the given interpretation_type.
    def interpretations(self, interpretation_type):

        interps = set()

        for reduction in self.reductions(len(interpretation_type)):

            interpretation_funcs = itertools.product(*[hom(reduction.interpretation_type[i], interpretation_type[i]) for i in range(len(interpretation_type))])

            for f in interpretation_funcs:

                interpretation = matrix([[f[i][reduction.rows[i][j]] for j in range(reduction.m + 1)] for i in range(reduction.n)])

                if interpretation.is_lextop():
                    continue

                interps.add(interpretation)

        return interps

# the main implies method for matrices.
def implies(N,M):

    Relation = M.columns[:]

    while True:

        size = len(Relation)

        for reduct in hom(M.n, N.n):

            reduction = matrix([N.rows[reduct[i]] for i in range(M.n)])

            if reduction.is_lextop():
                continue

            interpretation_funcs = itertools.product(*[hom(reduction.interpretation_type[i], M.interpretation_type[i]) for i in range(M.n)])

            for f in interpretation_funcs:

                interpretation = matrix([[f[i][reduction.rows[i][j]] for j in range(reduction.m + 1)] for i in range(reduction.n)])

                if interpretation.is_lextop():
                    continue

                if all(c in Relation for c in interpretation.columns):

                    if interpretation.right_column == M.right_column:
                        return True

                    if not interpretation.right_column in Relation:
                        Relation.append(interpretation.right_column)

        if len(Relation) == size:
            return False

def equivalent(N,M):
    return implies(N,M) and implies(M,N)




#mclex(4,5,2)

'''

T =time.time()
mclex(4,4,2)
print(T - time.time())
'''






'''
n = 3
m = 5
k = 4

name = 'mclex[' + str(n) + ',' + str(m) + ',' + str(k) +']'
'''
# Zurabs matrices of interest
'''
L = mclex(3,3,2)
L.append(matrix([[0,0,0,1,0], [0,0,1,1,0], [0,1,1,0,0], [1,0,1,1,0]]))
L.append(matrix([[0,0,0,1,0], [0,0,1,0,0], [0,1,1,1,0], [1,0,1,1,0]]))
L.append(matrix([[0,1,1,1,0], [1,0,1,1,0], [1,1,0,1,0], [1,1,1,0,0]]))
L.append(matrix([[1,0,0,0,0], [0,1,0,0,0], [0,0,1,0,0], [0,0,0,1,0]]))
L.append(matrix([[0,0,0,1,0], [0,0,1,0,0], [0,1,0,0,0], [1,0,0,0,0]]))
L.append(matrix([[0,0,0,1,1,1,0], [0,0,1,0,1,1,0], [0,1,0,1,0,1,0], [1,0,0,1,1,0,0]]))
L.append(matrix([[0,0,0,1,1,0], [0,1,1,0,0,0], [1,0,1,0,1,0]]))
L.append(matrix([[0,0,0,1,1,1,0], [0,1,1,0,0,1,0], [1,0,1,0,1,1,0]]))
'''
'''
difunctional = matrix([[0,0,0,0,1,1,1,0],
                       [0,0,1,1,0,0,1,0],
                       [0,1,0,1,1,1,0,0],
                       [1,1,1,0,0,1,0,0]])
'''

#Matrices = [matrix([[0,0,1,1,0],[0,1,0,1,0],[1,2,2,0,0]])]

#hasse(mclex(n,m,k),name=name, view=True, ranksep=1, nodesep=1, highlighted=Matrices)
'''
file = open('./pictures/' + name)
graph =  graphviz.Source(file.read())
graph.render(name, './pictures', True, False, 'png')
'''
