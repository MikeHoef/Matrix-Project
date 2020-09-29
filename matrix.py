import itertools
import math
import sys
import time
import random
import os
import os.path
import matrix_draw
from misc import *
import graphviz


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

    # all strict_interpretations of all reductions in interpretation_type.
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

# mclex methods.
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
# matrix equivalence.
def equivalent(N,M):
    return implies(N,M) and implies(M,N)

# all non-degenerate matrices with at most n rows, m columns and k variables.
def mclex(n,m,k):

    if k < 2:
        return []

    if m < 3:
        return []

    if n < 2:
        return []

    if m >= k ** n:
        return mclex(n, k ** n - 1, k)

    path = './data/mclex[' + str(n) + ',' + str(m) + ',' + str(k) + '].mc'

    if os.path.isfile(path):

        return read_in_matrices(open(path, 'r'))

    else:

        Matrices = mclex(n-1,m,k) + mclex(n,m-1,k) + mclex(n,m,k-1)+ strict_matrices(n,m,k)
        Matrices = set(Matrices)
        Final = []

        # --- refining matrices up to equivalence ---
        name = 'final refinement of mclex(' + str(n) + ',' + str(m) + ',' + str(k) +')'
        progress = progress_bar(name, len(Matrices), 50, size_of_extra_info=2)
        size  = len(Matrices)
        delta_time  = 0
        Relations = list(set(max_list_relations(n,m,k)))
        for r in Relations:
            print(r)
        while len(Matrices):

            T = time.time()
            progress.update(size - len(Matrices))
            extra_info = ['Matrices left: ' + str(len(Matrices)), 'Time for single refinement: ' + str(int(delta_time))]
            progress.display(extra_info)
            M = min(Matrices)
            temp_mats = []
            Final.append(M)

            for N in Matrices:

                if N == M:
                    continue

                if (M, N) in Relations:

                    transitively_close(Relations)

                    if (N,M) in Relations:
                        continue

                    if implies(N,M):
                        Relations.append((N,M))
                        continue

                    temp_mats.append(N)

                if implies(M, N):

                    Relations.append((M,N))
                    transitively_close(Relations)

                    if (N, M) in Relations:
                        continue

                    if implies(N,M):
                        Relations.append((N,M))
                        continue

                temp_mats.append(N)


            Matrices = temp_mats
            delta_time = time.time() - T

        progress.finish()
        # --- save results to file ---
        f = open(path, 'w')
        Final.sort()
        for mat in Final:
            write_matrix(mat, f)
        f.close()

        path_rels = './data/mclex[' + str(n) + ',' + str(m) + ',' + str(k) + '].rels'

        if os.path.isfile(path_rels):
            return Final
        else:
            Rels = set()
            for m in Final:
                for n in Final:
                    if implies(m,n):
                        Rels.add((m,n))
            f = open(path_rels, 'w')
            for r in Rels:
                if r[0] == r[1]: continue
                write_matrix(r[0], f)
                write_matrix(r[1], f)
            f.close()
            return Final


def max_list_relations(n,m,k):

    if k < 2:
        return []

    if m < 3:
        return []

    if n < 2:
        return []

    if m >= k ** n:
        return mclex(n, k ** n - 1, k)

    path_rels = './data/mclex[' + str(n) + ',' + str(m) + ',' + str(k) + '].rels'

    if os.path.isfile(path_rels):
        return read_in_relations(n,m,k)

    return max_list_relations(n-1,m,k) + max_list_relations(n,m-1,k) + max_list_relations(n,m,k-1)

# helper for mclex method.
def transitively_close(Relation):

    while True:
        size = len(Relation)
        for x in Relation:
            for y in Relation:
                if x[1] == y[0] and not (x[0], y[1]) in Relation:
                    Relation.append((x[0], y[1]))
        if size == len(Relation):
            break
# matrix generation.
def Lexi(n,m,k):

    def to_matrix(mat):
        Rows = []
        for i in range(n):
            Rows.append([c[i] for c in mat] + [0])
        return matrix(Rows)

    Mats = []
    cols = hom(n, k)

    for mat in itertools.combinations_with_replacement(cols, m):

        matr = to_matrix(mat)

        if matr.is_lextop():
            continue

        if not matr.rows_lexi():
            continue

        if matr.is_trivial():
            continue

        Mats.append(matr)

    return Mats

def matrices(n,m,k):

    if k < 2:
        return []

    if m < 3:
        return []

    if n < 2:
        return []

    if m >= k ** n:
        return matrices(n, k ** n - 1, k)

    return matrices(n-1,m,k) + matrices(n,m-1,k) + matrices(n,m,k-1) + strict_matrices(n,m,k)

def strict_matrices(n,m,k):

    def to_matrix(mat):
        Rows = []
        for i in range(n):
            Rows.append([c[i] for c in mat] + [0])
        return matrix(Rows)

    Mats = []
    cols = hom(n, k)
    N = k ** n
    size_bar = (math.factorial(N)/math.factorial(N - m))/math.factorial(m)
    name_bar = 'generating strict_matrices(' + str(n) + ',' + str(m) + ',' + str(k) +')'
    progress = progress_bar(name_bar, size_bar, 50)
    count = 0
    for mat in itertools.combinations(cols, m):
        count = count + 1
        progress.update(count)
        progress.display()
        matr = to_matrix(mat)

        if matr.is_lextop():
            continue

        if matr.has_zero_row():
            continue

        if not matr.rows_lexi():
            continue

        if matr.has_duplicate_rows():
            continue

        if not matr.variables_ordered():
            continue

        if matr.is_trivial():
            continue

        Mats.append(matr)
    progress.finish()
    return Mats

# io
def convert_line_to_row(line):
    P = []
    for a in line:
        if (a != '\n'):
            P.append(int(a))
    return P

def write_matrix(M, f):
    f.write('\n')
    for r in M.rows:
        for x in r:
            f.write(str(x))
        f.write('\n')

def read_in_matrices(file):

    Lines = file.readlines()
    R = []

    for line in Lines:
        R.append(convert_line_to_row(line))

    n = len(R)

    i = 0
    Matrices = []
    while i < n - 1:
        if not R[i]:
            i = i + 1
            continue
        else:
            j = 0
            Rows = []
            while R[i + j]:
                Rows.append(R[i + j])
                j = j + 1
                if i + j == n - 1:
                    Rows.append(R[i + j])
                    break
            Matrices.append(matrix(Rows[:]))
            i = i + j
    return Matrices

def read_in_relations(n,m,k):

    path_rels = './data/mclex[' + str(n) + ',' + str(m) + ',' + str(k) + '].rels'
    Relations = []

    if os.path.isfile(path_rels):
        Rels = read_in_matrices(open(path_rels, 'r'))
        for i in range(int(len(Rels)/2)):
            Relations.append((Rels[2*i], Rels[2*i + 1]))

    return Relations

# poset visualization
def hasse(Matrices,view=True, name=None, orient='BT', splines='lines', ranksep=1, nodesep=1,highlighted=[]):

    L = Matrices[:]
    L.sort()

    n = len(L)
    rels = []
    progress = progress_bar('generating poset ' + str(name), n * n, 50)
    count = 0
    for i in range(n):
        for j in range(n):
            count = count + 1
            progress.update(count)
            progress.display()
            if not i == j:
                if implies(L[i], L[j]):
                    rels.append((i,j))
    print(matrix_draw.graphviz_hasse(Matrices, rels, splines=splines,ranksep=ranksep,nodesep=nodesep))
    graph =  graphviz.Source(matrix_draw.graphviz_hasse(Matrices, rels, splines=splines,ranksep=ranksep,nodesep=nodesep, highlighted=highlighted))

    if name == None:
        graph.view(directory='./temp', cleanup=True)
    else:
        graph.render(name, './pictures', view, False, 'png')









mclex(3,7,2)
relations = max_list_relations(3,4,2)
for r in relations:
    print(r)









'''
n = 3
m = 6
k = 3

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

Matrices = [M for M in mclex(4,7,2) if implies(M,difunctional)]
'''

#hasse(mclex(n,m,k),name=name, view=True, ranksep=1, nodesep=1)
'''
file = open('./pictures/' + name)
graph =  graphviz.Source(file.read())
graph.render(name, './pictures', True, False, 'png')
'''
