from python_files.matrix import *
from python_files.matrix_generation import *
from python_files.matrix_proof import *
from python_files.matrix_visualisation import *

Mal = matrix([[1,0,0,1], [0,0,1,1]])
Maj = matrix([[1,0,0,0], [0,1,0,0], [0,0,1,0]])
Pix = matrix([[1,0,0,1], [0,1,0,0], [0,0,1,1]])
Min =matrix([[1,0,0,1], [0,1,0,1], [0,0,1,1]])


print ('Some true implications..')
print('---')
print(implies(Pix, Mal))
print(implies(Pix, Maj))
print('---')
print ('Some false ones...')
print('---')
print(implies(Mal, Maj))
print(implies(Maj, Mal))
print(implies(Mal, Pix))
print('---')
print ('Proof that Pixley implies Minority...')
print('---')
print(proof(Pix, Min))
print('')
print('Generation of hasse diagram')
matrices = mclex(3,4,3)
relations = relations(3,4,3)
highlighted_matrices = mclex(3,4,2)
hasse(matrices, relations, penwidth=3, highlighted=highlighted_matrices)
