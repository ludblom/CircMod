#!/usr/bin/env python3

from Circ.Matrix import Matrix
import copy, random


class PBox(Matrix):
    def permutation_box(self, N):
        P_I = []
        while P_I == []:
            P_tmp = []
            for _ in range(N):
                tmp = []
                for _ in range(N):
                    rand = random.randint(0, 1)
                    tmp.append(rand)
                P_tmp.append(tmp)
            P = copy.deepcopy(P_tmp)
            P_I = self.calculate_inverse(P_tmp)
        return P, P_I
