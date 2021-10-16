#!/usr/bin/env python3

from Attack.RingOperator import Ring
from ToyCipher.ToyCipher import ToyCipher
from Attack.HiddenSum import HiddenSum
from Attack.Matrix import Matrix

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

def attacking():
    m = Matrix()
    hs = HiddenSum()
    t = ToyCipher(block_len=6, rounds=5)
    t.load_cipher("tmp_cipher.txt")
    for i in range(64):
        c = t.encrypt(m.int_to_binary(i, 6), "000000")
        ret = hs.attack(c, "000000")
        if ret == []:
            print("{}\t{}\t{}".format(i, m.binary_to_int(c), "Error"))
        else:
            ret_int = m.binary_to_int(ret)
            print("{}\t{}\t{}\t{}".format(i, m.binary_to_int(c), ret_int, i==ret_int))

if __name__ == '__main__':
    # for i in range(10):
    #     attack(3, 1)
    attacking()
