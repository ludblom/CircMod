#!/usr/bin/env python3

from Attack.RingOperator import Ring
from ToyCipher.ToyCipher import ToyCipher

import copy


def attack(N, k):
    t = ToyCipher(block_len=int(N/3))
    r = Ring(N=N, k=k)

    print(r.lam(t.P))
    l = []
    for i in range(2**N):
        l.append(r.gamma_xor(i, t.P))
    print(l)
    print()
    print(t.P)
    print(t.P_I)
    print()


if __name__ == '__main__':
    attack(6, 2)
