
from .matrix import *
import os.path

# input and output methods
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

    path_rels = './python_files/data/mclex[' + str(n) + ',' + str(m) + ',' + str(k) + '].rels'
    Relations = []

    if os.path.isfile(path_rels):
        Rels = read_in_matrices(open(path_rels, 'r'))
        for i in range(int(len(Rels)/2)):
            Relations.append((Rels[2*i], Rels[2*i + 1]))

    return Relations
