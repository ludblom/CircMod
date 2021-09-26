#!/usr/bin/env python3

import random
from HiddenSum import HiddenSum


class ToyCipher(HiddenSum):
    def __init__(self, N=5):
        self.N = N
        self.P = self.permutation_box()
        self.S = 0 # TODO Substitution box
        super().__init__()

    def permutation_box(self):
        P = []
        k = random.randint(0, 1)
        for _ in range(self.N):
            tmp = []
            for _ in range(self.N):
                tmp.append(k)
            P.append(tmp)
        return P

    def substitution_box(self):
        all_values = [1 for i in range(self.N)]
