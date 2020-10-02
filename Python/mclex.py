from python_files.matrix import *
from python_files.matrix_generation import *


Mats = matrices(4,9,2)
Reps = mclex(4,9,2)

Sizes = []
for m in Reps:
    Sizes.append(len([n for n in Mats if equivalent(n,m)]))

Sizes.sort()
for x in Sizes:
    print(x)
