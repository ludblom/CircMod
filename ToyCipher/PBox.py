#!/usr/bin/env python3

from Circ.Matrix import Matrix
import copy, random


class PBox(Matrix):
    def permutation_box(self, num_of_octals):
        P_I = []
        while P_I == []:
            P_tmp = []
            for _ in range(num_of_octals*3):
                tmp = []
                for _ in range(num_of_octals*3):
                    rand = random.randint(0, 1)
                    tmp.append(rand)
                P_tmp.append(tmp)
            P = copy.deepcopy(P_tmp)
            P_I = self.calculate_inverse(P_tmp)
        return P, P_I
