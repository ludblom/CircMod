#!/usr/bin/env python3

from ToyCipher.ToyCipher import ToyCipher
from Attack.HiddenSum import HiddenSum


if __name__ == '__main__':
    t = ToyCipher(block_len=3)
    hs = HiddenSum(N=3, k=1, t=t)
    while(not hs.lambda_GL_ring(t.P)):
        t.P, t.P_I = t.permutation_box()
    t.save_cipher("found_P_candidate.txt", hard=True)
