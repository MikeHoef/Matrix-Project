import pathlib
import time
import os
import itertools
from .matrixio import *
from .helpers import *
from .matrix import *



# returns a representative list of non-degenerate matrices with at most n rows, m columns and k variables.
def mclex(n,m,k):

    # base conditions.
    if k < 2:
        return []

    if m < 3:
        return []

    if n < 2:
        return []

    if m >= k ** n:
        return mclex(n, k ** n - 1, k)

    # fetch it if it already exists.
    path = str(pathlib.Path().absolute()) + '/python_files/data/mclex[' + str(n) + ',' + str(m) + ',' + str(k) + '].mc'

    if os.path.isfile(path):

        return read_in_matrices(open(path, 'r'))

    else:

        # fetch matrices that need to be refined.
        Matrices = mclex(n-1,m,k) + mclex(n,m-1,k) + mclex(n,m,k-1)+ strict_matrices(n,m,k)
        Matrices = set(Matrices)
        Final = []
        size  = len(Matrices)
        T = time.time()
        Relations = set(mclex_relations(n,m,k))       # used to minimize calls to imlpies method.

        print(' --------- refining ---------')

        # refine Matrices.
        while len(Matrices):

            M = min(Matrices)                      # represetative is always chosen to be min according the order on matrices. Random is sometimes better.
            temp_mats = []
            Final.append(M)

            print('matrices left: ' + str(len(Matrices)) + ' | time elapsed: ' + str(time.time() - T))

            for N in Matrices:

                if (M,N) in Relations:

                    M_implies_N = True

                else:

                    M_implies_N = implies(M,N)

                if (N,M) in Relations:

                    N_implies_M = True

                else:

                    N_implies_M = implies(N,M)


                if M_implies_N and N_implies_M:
                    continue

                temp_mats.append(N)

                if M_implies_N:
                    Relations.add((M, N))
                    continue

                if N_implies_M:
                    Relations.add((N,M))
                    continue

            # restrict domain of relation.
            domain = set(temp_mats + Final)
            Relations = set((x,y) for (x,y) in Relations if x in domain and y in domain)
            Matrices = temp_mats

        # --- save results to .mc and .rels files ---
        f = open(path, 'w')
        Final.sort()
        for mat in Final:
            write_matrix(mat, f)
        f.close()
        path_rels = str(pathlib.Path().absolute()) + '/python_files/data/mclex[' + str(n) + ',' + str(m) + ',' + str(k) + '].rels'

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

# helper used in mclex method. Returns the most relations possible given whats in .data
def mclex_relations(n,m,k):

    if k < 2:
        return []

    if m < 3:
        return []

    if n < 2:
        return []

    if m >= k ** n:
        return mclex_relations(n, k ** n - 1, k)

    path_rels = './python_files/data/mclex[' + str(n) + ',' + str(m) + ',' + str(k) + '].rels'

    if os.path.isfile(path_rels):
        return read_in_relations(n,m,k)

    path = './python_files/data/mclex[' + str(n) + ',' + str(m) + ',' + str(k) + '].mc'

    rels = []
    if os.path.isfile(path):

        mats = read_in_matrices(open(path, 'r'))
        print(' --- generating relations -- ')
        for m in mats:
            for n in mats:
                if not n == m:
                    if implies(n,m):
                        rels.append((n,m))
        f = open(path_rels, 'w')

        for r in rels:
            write_matrix(r[0],f)
            write_matrix(r[1],f)

        f.close()
        return rels

    return mclex_relations(n-1,m,k) + mclex_relations(n,m-1,k) + mclex_relations(n,m,k-1)

# all matrices with at most n rows, m columns and k variables (no refinement).
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

# a matrix is (n,m,k)-strict if it has n rows, m columns (no duplicates).
# moreover it must satisfy a further condition on the number of occurences of its variables.
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

        if not matr.variables_ordered():
            continue

        if matr.is_trivial():
            continue

        Mats.append(matr)
    return Mats
