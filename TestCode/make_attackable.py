#!/usr/bin/env python3

import time

"""
Template code to brute force search for a P and S-box combination that are linear
against each other. No key is used here.
"""

from ToyCipher.ToyCipher import ToyCipher
from Attack.RingOperator import Ring
from Attack.HiddenSum import HiddenSum


def checker(r, t):
    # Check that the vulnerability works on the whole set
    for a in range(2**3):
        for b in range(2**3):
            a_o_b = r.ring(a, b)
            lam_aob = r.binary_to_int(t.encrypt(r.int_to_binary(a_o_b, 3), "000"))

            lam_a = t.encrypt(r.int_to_binary(a, 3), "000")
            lam_b = t.encrypt(r.int_to_binary(b, 3), "000")
            lama_o_lamb = r.ring(r.binary_to_int(lam_a), r.binary_to_int(lam_b))

            if(lam_aob != lama_o_lamb):
                return False
    return True


def search_attackable():
    r = Ring(N=3, k=1)
    t = ToyCipher(block_len=3, rounds=1)
    while(not checker(r, t)):
        t.S, t.S_I = t.substitution_box(3)
        t.P, t.P_I = t.permutation_box()
        t.K, t.K_I = t.key_box()
    t.save_cipher("attackable_found.txt", hard=True)

def l():
    hs = HiddenSum()
    r = Ring(N=3, k=1)
    t = ToyCipher(block_len=3, rounds=1)
    t.load_cipher("attackable_found.txt")

    for i in range(2**3):
        i_i = t.int_to_binary(i, 3)
        c = t.encrypt(i_i, t.int_to_binary(i, 3))
        c_tile = hs.tile(c)

        M, zero = hs.create_M(t)
        M_i = t.calculate_inverse(M)
        if M_i == []:
            return False
        c_v = t.xor(c_tile, zero)
        m_tile = t.matrix_mul_row_column(c_v, M_i)
        m = hs.tileInv(m_tile)
        if m != i_i:
            return False
    return True

def te():
    t = ToyCipher()
    t.load_cipher('is_linear.txt')
    print(t.P_I)

# start = time.time()
# search_attackable()
# while(not l()):
#     search_attackable()
# end = time.time()

# print("It took %.2f secounds." % (end-start))

te()
