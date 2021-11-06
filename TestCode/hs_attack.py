#!/usr/bin/env python3

from ToyCipher.ToyCipher import ToyCipher
from Attack.HiddenSum import HiddenSum


if __name__ == '__main__':
    for i in range(100):
        t = ToyCipher(block_len=6)
        hs = HiddenSum(N=6, k=2, t=t)
        hs.lambda_GL_ring(t.P)
        while(not hs.lambda_GL_ring(t.P)):
            print("Whoooo")
            t.P, t.P_I = t.permutation_box()
