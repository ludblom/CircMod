#!/usr/bin/env python3

from Circ.Matrix import Matrix

import random


class ToyCipher(Matrix):
    def __init__(self, N=5):
        self.N = N
        self.P = self.permutation_box()
        self.S = self.substitution_box()
        super().__init__()

    def permutation_box(self):
        P = []
        for _ in range(self.N):
            tmp = []
            for _ in range(self.N):
                tmp.append(random.randint(0, 1))
            P.append(tmp)
        return P

    def substitution_box(self):
        S = {}
        random_values = [i for i in range(2**self.N)]
        random.shuffle(random_values)
        for i in range(2**self.N):
            S[i] = random_values[i]
        return S
