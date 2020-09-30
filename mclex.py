from python_files.matrix import *
from python_files.matrix_generation import *
from python_files.matrix_proof import *
from python_files.matrix_visualisation import *

Mal = matrix([[1,0,0,1], [0,0,1,1]])
Maj = matrix([[1,0,0,0], [0,1,0,0], [0,0,1,0]])
Pix = matrix([[1,0,0,1], [0,1,0,0], [0,0,1,1]])
Min =matrix([[1,0,0,1], [0,1,0,1], [0,0,1,1]])

hasse([Mal, Maj, Pix, Min])
