from matrix import *
import sys

class matrix_proof:

    def __init__(self,N,M,steps):

        self.N = N
        self.M = M
        self.steps   = steps

    def trim(self):

        while True:

            Rel = self.M.columns[:]
            size = len(self.steps)
            for i in range(size):
                if self.steps[i].right_column == self.M.right_column:
                    self.steps = self.steps[:i]
                    break
                if self.steps[i].right_column in Rel:
                    self.steps.remove(self.steps[i])
                else:
                    Rel.append(self.steps)
            if size == len(self.steps):
                break


    def valid(self):

            Rel = set(tuple(c) for c in self.M.columns[:])

            for i in range(len(self.steps)):

                if not set([tuple(c) for c in self.steps[i].columns]).issubset(Rel):
                    return False

                if self.steps[i].right_column == self.M.right_column:
                    return True
                else:
                    Rel.add(tuple(self.steps[i].right_column))

            return False

    def __str__(self):
        size = self.N.m + self.M.m
        S = ''
        S = S + '\n'
        S = S + '--' * size
        S = S + '\n'
        S = S + 'Premise \n'
        S = S + '--' * size
        S = S + '\n'
        S = S + str(self.N)
        S = S + '--' * size + '\n'
        S = S + 'Conclusion \n'
        S = S + '--' * size + '\n'
        S = S + str(self.M)
        S = S + '--' * size + '\n'
        S = S + 'Steps \n'
        S = S + '--' * size + '\n \n'

        for step in self.steps:
            S = S + str(step) + '\n'

        S = S + '--' * size + '\n'
        return S

def prove(N,M):

    proofs = []

    if not implies(N,M):
        return False

    interps = N.interpretations(M.interpretation_type)

    num_steps = 0

    while True:

        attempts = list(itertools.product(interps, repeat=num_steps))

        for attempt in attempts:

            proof = matrix_proof(N,M,attempt)

            if proof.valid():
                return proof

        num_steps = num_steps + 1



''' This is the matrix in the begining of the paper
First = matrix([[1,1,0,2,2,0],[0,0,1,1,0,0],[2,0,1,2,1,0]])

Second = matrix([[0,0,1,1,0], [0,1,0,1,0],[1,2,2,0,0]])

proof = prove(Second, First)
'''
'''
First =  matrix([[0,0,0,1,0], [0,0,1,1,0],[0,1,1,0,0], [1,0,1,1,0]])

Second = matrix([[0,0,0,1,1,0], [0,0,1,1,1,0],[0,1,1,0,1,0], [1,0,1,1,0,0]])

proof = prove(Second, First)
'''





print(proof)
