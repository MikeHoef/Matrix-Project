from python_files.matrix import *
from python_files.matrix_generation import *
from python_files.matrix_proof import *
from python_files.matrix_visualisation import *

T = time.time()
Mats = mclex(3,5,4)
Rels = mclex_relations(3,5,4)
M = matrix([[0,0,1,1,0],[0,1,0,1,0],[1,2,2,0,0]])

hasse('mclex[3,5,4]', Mats, Rels, arrowhead='none',
penwidth=1, nodesep=0.5,ranksep=0.4, highlighted=[M])
