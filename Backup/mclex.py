from python_files.matrix import *
from python_files.matrix_generation import *
from python_files.matrix_proof import *
from python_files.matrix_visualisation import *


T = time.time()
Mats = matrices(4,4,2)
L = fast_refine(Mats)
print(T - time.time())
for m in L:
    print(m)
