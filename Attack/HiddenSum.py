#!/usr/bin/env python3

from .Matrix import Matrix
from ToyCipher.ToyCipher import ToyCipher

import copy


class HiddenSum:
    def __init__(self):
        super().__init__()

    def lambda_six(self, x):
        l = []
        l.append(x[0])
        l.append((x[0]&x[2])^x[1])
        l.append(x[2])
        return l

    def lambdaInv_six(self, l):
        x = []
        x.append(l[0])
        x.append(l[1]^(l[0]&l[2]))
        x.append(l[2])
        return x

    def vprime_six(self, v):
        a = self.lambda_six(v[:3])
        b = self.lambda_six(v[3:])
        return a+b

    def vprimeInv_six(self, v):
        a = self.lambdaInv_six(v[:3])
        b = self.lambdaInv_six(v[3:])
        return a+b

    def attack(self, c, k):
        t = ToyCipher(block_len=6, rounds=5)
        t.load_cipher("tmp_cipher.txt")

        zero = [0 for i in range(6)]
        zeroc = t.encrypt(zero, k)

        mat = Matrix()
        I = mat.get_identity(6)

        Caz = [t.encrypt(i, k) for i in I]

        lCaz = [self.vprime_six(i) for i in Caz]
        lzeroc = self.vprime_six(zeroc)

        lCaz2 = [ [ (lCaz[i][j]^lzeroc[j]) for j in range(6) ] for i in range(6) ]
        lCaz2Inv = mat.calculate_inverse(lCaz2)

        if(lCaz2Inv == []):
            return []

        cc = self.vprime_six(c)

        mm = mat.matrix_mul_row_column([cc[i]^lzeroc[i] for i in range(6)], lCaz2Inv)

        return self.vprimeInv_six(mm)
