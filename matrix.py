import itertools
import time
import random
import os.path




class matrix:

    def __init__(self, rows):

        n = len(rows)
        m = len(rows[0]) - 1
        self.rows = rows
        self.columns = [[rows[j][i] for j in xrange(n)] for i in xrange(m)]
        self.right_column = [rows[j][m] for j in xrange(n)]
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
        return self.rows < M.rows

    def __eq__(self, M):
        return self.rows == M.rows

    def __str__(self):
        S = ''
        for r in self.rows:
            S = S + str(r) + '\n'
        return S

    def __hash__(self):
        return hash(tuple(tuple(r) for r in self.rows))

    def rows_lexi(self):
        return all(self.rows[i][:self.m] <= self.rows[i+1][:self.m] for i in xrange(self.n-1))

    def cols_lexi(self):
        return all(self.columns[i] <= self.columns[i+1] for i in xrange(self.m-1))

    def double_lexi(self):
        return self.rows_lexi() and self.cols_lexi()

    def is_lextop(self):
        return self.right_column in self.columns

    def is_trivial(self):

        funcs = itertools.product(*[hom(self.interpretation_type[i] + 1, 2) for i in xrange(self.n)])
        num_cols = self.m + 1

        for f in funcs:
            interpretation = matrix([[f[i][self.rows[i][j]] for j in xrange(num_cols)] for i in xrange(self.n)])
            if interpretation.is_lextop():
                continue
            else:
                for i in xrange(interpretation.n):
                    for j in xrange(i + 1, self.n):
                        if interpretation.rows[i][:self.m] == interpretation.rows[j][:self.m] and not interpretation.rows[i][self.m] == interpretation.rows[j][self.m]:
                            return True
        return False

    def has_zero_row(self):
        return [0] * (self.m + 1) in self.rows

    def has_duplicate_rows(self):
        for i in xrange(self.n):
            for j in xrange(i + 1, self.n):
                if self.rows[i] == self.rows[j]:
                    return True
        return False

# helper methods.
def hom(k, n):
    return list(itertools.product(xrange(n), repeat=k))

# mslex methods.
def implies(N,M):

    Relation = M.columns[:]

    while True:

        size = len(Relation)

        for reduct in hom(M.n, N.n):

            reduction = matrix([N.rows[reduct[i]] for i in xrange(M.n)])

            if reduction.is_lextop():
                continue

            interpretation_funcs = itertools.product(*[hom(reduction.interpretation_type[i], M.interpretation_type[i]) for i in xrange(M.n)])

            for f in interpretation_funcs:

                interpretation = matrix([[f[i][reduction.rows[i][j]] for j in xrange(reduction.m + 1)] for i in xrange(reduction.n)])

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

def mslex(n,m,k):

    Time = time.time()

    if k < 2:
        return []

    if m < 3:
        return []

    if n < 2:
        return []

    if m >= k ** n:
        return mslex(n, k ** n - 1, k)

    path = './data/mslex[' + str(n) + ',' + str(m) + ',' + str(k) + '].ms'

    if os.path.isfile(path):
        L = read_in_matrices(open(path, 'r'))
        L.sort()
        f = open(path, 'w')
        for m in L:
            write_matrix(m, f)
        f.close()
        return L

    else:

        Matrices = mslex(n-1,m,k) + mslex(n,m-1,k) + mslex(n,m,k-1)+ strict_matrices(n,m,k)
        Matrices = set(Matrices)
        Final = []

        # --- refining matrices up to equivalence ---
        while len(Matrices):
            print(len(Matrices))
            M = min(Matrices)
            Matrices = [N for N in Matrices if not equivalent(N,M)]
            Final.append(M)

        # --- save results to file ---
        f = open(path, 'w')

        for mat in Final:
            write_matrix(mat, f)
        f.close()
        return Final

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

    for mat in itertools.combinations(cols, m):

        matr = to_matrix(mat)

        if matr.is_lextop():
            continue

        if matr.has_zero_row():
            continue

        if not matr.rows_lexi():
            continue

        if matr.has_duplicate_rows():
            continue

        if matr.is_trivial():
            continue

        Mats.append(matr)

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

# --- main ---
T = time.time()
L    = mslex(3,6,3)
print(time.time() - T)
for m in L:
    print(m)
print(len(L))
