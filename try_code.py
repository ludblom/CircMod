#!/usr/bin/env python3

from Attack.RingOperator import Ring
from ToyCipher.ToyCipher import ToyCipher


def attack(N, k):
    r = Ring(N=N, k=k)
    t = ToyCipher(block_len=(N/3))

    print(t.P)


if __name__ == '__main__':
    attack(3, 1)
