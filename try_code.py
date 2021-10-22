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

def attacking_using_calderi():
    m = Matrix()
    hs = HiddenSum()
    t = ToyCipher(block_len=6, rounds=5)
    t.load_cipher("tmp_cipher.txt")

    for i in range(64):
        c = t.encrypt(m.int_to_binary(i, 6), "110010")
        ret = hs.attack(c, t)
        if ret == []:
            print("{}\t{}\t{}".format(i, m.binary_to_int(c), "Error"))
        else:
            ret_int = m.binary_to_int(ret)
            print("{}\t{}\t{}\t{}".format(i, m.binary_to_int(c), ret_int, i==ret_int))

def attack_creating_unsecure_cipher():
    m = Matrix()
    hs = HiddenSum()
    t = ToyCipher(block_len=6, rounds=5)
    t.load_cipher("tmp_cipher.txt")
    r = Ring(N=6, k=2)
    # Having P[i][j] we linearize it using lambda, ie create it
    # by having a lookup table created by i = 000000 -> ... -> 111111
    # and then replace each row of P with this new number
    #t.P = r.linearize(t.P)
    #t.P_I = m.calculate_inverse(t.P)

    #print("{} {}".format(t.P, t.P_I))

    #c = t.encrypt("011010", "101010")
    #cc = hs.attack(c, t)
    #print("{} {}".format("[0, 1, 1, 0, 1 ,0]", cc))
    print(r.lamb(t.P))

def attack_all(PB):
    m = Matrix()
    hs = HiddenSum()
    r = Ring(N=6, k=2)
    t = ToyCipher(block_len=6, rounds=5)
    t.P = PB
    t.P_I = m.calculate_inverse(PB)
    if t.P_I == []:
        return -1
    c = t.encrypt("101010", "101010")
    cc = hs.attack(c, t)
    if cc == "101010":
        return t.P
    else:
        return -1

def attack_all_p(m, a, b, c, d, e, f):
    PB = []
    PB.append(m.int_to_binary(a, 6))
    PB.append(m.int_to_binary(b, 6))
    PB.append(m.int_to_binary(c, 6))
    PB.append(m.int_to_binary(d, 6))
    PB.append(m.int_to_binary(e, 6))
    PB.append(m.int_to_binary(f, 6))
    ret = attack_all(PB)
    if ret != -1:
        print(ret)

def attack_using_ring():
    m = Matrix()
    hs = HiddenSum()
    r = Ring(N=6, k=2)
    t = ToyCipher(block_len=6, rounds=5, attackable=True)
    l = r.lamb(t.P)
    li = r.lamb(t.P_I)

    for i in range(64):
        c = t.encrypt(m.int_to_binary(i, 6), "110010")
        ret = hs.attack(m.int_to_binary(li[m.binary_to_int(c)], 6), t)
        if ret == []:
            print("{}\t{}\t{}".format(i, m.binary_to_int(c), "Error"))
        else:
            ret_int = m.binary_to_int(ret)
            print("{}\t{}\t{}\t{}".format(i, m.binary_to_int(c), ret_int, i==ret_int))

def save_a_cipher():
    t = ToyCipher(block_len=3, rounds=1)
    t.save_cipher("attack_me.txt", hard=True)

if __name__ == '__main__':
    #attack_creating_unsecure_cipher()
    #attacking_using_calderi()
    # m = Matrix()
    # for a in range(64):
    #     print("a: " + str(a))
    #     for b in range(64):
    #         print("b: " + str(b))
    #         for c in range(64):
    #             print("c: " + str(c))
    #             for d in range(64):
    #                 for e in range(64):
    #                     for f in range(64):
    #                         attack_all_p(m, a, b, c, d, e, f)
    save_a_cipher()
