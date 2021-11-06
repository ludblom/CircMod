#!/usr/bin/env python3

from ToyCipher.ToyCipher import ToyCipher
from Attack.HiddenSum import HiddenSum


def find_GL():
    # TODO Rapport, How to determine linearity
    t = ToyCipher(block_len=3)
    hs = HiddenSum(N=3, k=1, t=t)
    while(not hs.lambda_GL_ring(t.P)):
        t.P, t.P_I = t.permutation_box()
    t.save_cipher("found_P_candidate.txt", hard=True, only_P=True)


def get_ring_table(size):
    t = ToyCipher(block_len=3)
    hs = HiddenSum(N=3, k=1, t=t)

    print("o", end="   ")
    for i in range(2**size):
        print("{}".format(i), end=" ")
    print("\n")

    for i in range(2**size):
        print("{}".format(i), end="   ")
        for j in range(2**size):
            print("{}".format(hs.ring(i, j)), end=" ")
        print("")


if __name__ == '__main__':
    # counter = 0
    # while(True):
    #     try:
    #         if counter == 1000:
    #             find_GL()
    #             counter = 0
    #         t = ToyCipher(block_len=3)
    #         t.load_cipher("found_P_candidate.txt")
    #         hs = HiddenSum(N=3, k=1, t=t)
    #         c = t.encrypt("100", "101")
    #         m = hs.attack(c)
    #         if m == "100":
    #             print("Success.")
    #             break
    #         counter += 1
    #     except IndexError:
    #         counter += 1
    #         continue
    t = ToyCipher(block_len=3)
    t.load_cipher("found_P_candidate.txt")
    hs = HiddenSum(N=3, k=1, t=t)
    print(t.encrypt("100", "000"))
    print(t.encrypt("010", "000"))
    print(t.encrypt("001", "000"))
    print(t.encrypt("000", "000"))
    print(hs.M)
    print(hs.M_inv)
    print(t.encrypt("011", "010"))
