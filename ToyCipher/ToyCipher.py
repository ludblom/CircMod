#!/usr/bin/env python3

from Circ.Matrix import Matrix

import random, copy


class ToyCipher(Matrix):
    def __init__(self, N=3):
        self.N = N
        self.P, self.P_I = self.permutation_box()
        self.S, self.S_I = self.substitution_box()
        super().__init__()

    def permutation_box(self):
        P_I = []
        while P_I == []:
            P_tmp = []
            for _ in range(self.N):
                tmp = []
                for _ in range(self.N):
                    rand = random.randint(0, 1)
                    tmp.append(rand)
                P_tmp.append(tmp)
            P = copy.deepcopy(P_tmp)
            P_I = self.calculate_inverse(P_tmp)
        return P, P_I

    def substitution_box(self):
        S = {}
        S_I = {}
        random_values = [i for i in range(2**self.N)]
        random.shuffle(random_values)
        for i in range(2**self.N):
            S[i] = random_values[i]
            S_I[random_values[i]] = i
        return S, S_I
