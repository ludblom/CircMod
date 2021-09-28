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
        P = {}
        P_I = {}
        random_values = [i for i in range(2**self.N)]
        random.shuffle(random_values)
        for i in range(2**self.N):
            P[i] = random_values[i]
            P_I[random_values[i]] = i
        return P, P_I

    def substitution_box(self):
        S_I = []
        while S_I == []:
            S_tmp = []
            for _ in range(self.N):
                tmp = []
                for _ in range(self.N):
                    rand = random.randint(0, 1)
                    tmp.append(rand)
                S_tmp.append(tmp)
            S = copy.deepcopy(S_tmp)
            S_I = self.calculate_inverse(S_tmp)
        return S, S_I

    def string_to_binary(self, string):
        return str(''.join(format(i, '07b') for i in bytearray(string, encoding = 'utf-8')))

    def binary_to_string(self, binary):
        string = ' '
        for i in range(0, len(binary), 7):
            tmp = binary[i:i + 7]
            string += chr(int(tmp, 2))
        return string[1:]

    def encrypt(self, data, key, armor=False):
        pass
