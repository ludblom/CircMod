#!/usr/bin/env python3

import random


class SBox:
    def substitution_box(self, N):
        S = {}
        S_I = {}
        random_values = [i for i in range(2**N)]
        random.shuffle(random_values)
        for i in range(2**N):
            S[i] = random_values[i]
            S_I[random_values[i]] = i
        return S, S_I
