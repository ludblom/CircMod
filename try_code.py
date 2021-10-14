#!/usr/bin/env python3

from Attack.RingOperator import Ring
from ToyCipher.ToyCipher import ToyCipher

import copy


def lamb_xor(t, r, papp):
    l = []
    for i in range(2**r.N):
        if papp == "P":
            l.append(r.gamma_xor(i, t.P))
        else:
            l.append(r.gamma_xor(i, t.P_I))
    return l

def trying():
    t = ToyCipher(block_len=6, rounds=5)
    r = Ring(N=6, k=2)
    t.load_cipher("tmp_cipher.txt")
    print("Message: {}".format("101010"))
    print("Cipher: {}".format(t.encrypt("101010", "000000")))
    print()
    print("Key: {}".format("000000"))
    print()
    print("P: {}".format(t.P))
    print("P_I: {}".format(t.P_I))
    print()
    print("lam P: " + str(r.lamb(t.P)))
    print("lxorR: " + str(lamb_xor(t, r, "P")))
    print()
    print("lam P_i: " + str(r.lamb(t.P_I)))
    print("lxorR_I: " + str(lamb_xor(t, r, "P_I")))
    print()
    print("S: " + str(t.S))
    print("S_I " + str(t.S_I))

if __name__ == '__main__':
    # for i in range(10):
    #     attack(3, 1)
    trying()
