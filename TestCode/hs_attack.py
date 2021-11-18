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
    t.load_cipher("found_P_candidate.txt")
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


#if __name__ == '__main__':
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
# while(True):
#     t = ToyCipher(block_len=3)
#     #t.load_cipher("found_P_candidate.txt")
#     try:
#         hs = HiddenSum(N=3, k=1, t=t)
#         print(t.S)
#     except ValueError:
#         continue
    # print(t.encrypt("100", "000"))
    # print(t.encrypt("010", "000"))
    # print(t.encrypt("001", "000"))
    # print(t.encrypt("000", "000"))
    # print(hs.M)
    # print(hs.M_inv)
    # print(t.encrypt("011", "010"))



## LOAD ENC
# while(True):
#     t = ToyCipher(block_len=3, rounds=1)
#     t.load_cipher("wohoop.txt")
#     try:
#         hs = HiddenSum(N=3, k=1, t=t)
#         ti = True
#         for i in range(2**3):
#             c = t.encrypt(t.int_to_binary(i, 3), "001")
#             if i != hs.attack(c):
#                 ti = False
#         if ti:
#             t.save_cipher("found_one.txt")
#             break
#     except ValueError:
#         continue

## FIND ATTACKABLE
# while(True):
#     try:
#         t = ToyCipher()
#         hs = HiddenSum(t=t)
#         c = t.encrypt("110", "101")
#         if hs.attack(c) == 3:
#             t.save_cipher("wohoop.txt")
#             break
#     except ValueError:
#         continue

# while(True):
#     t = ToyCipher()
#     t.load_cipher("found.txt")
#     try:
#         hs = HiddenSum(t=t)
#         equality = True
#         for i in range(2**3):
#             c = t.encrypt(t.int_to_binary(i, 3), "000")
#             m = hs.attack(c)
#             if m != i:
#                 equality = False
#         if equality:
#             t.save_cipher("YAAAAAAY.txt")
#             break
#     except ValueError:
#         continue

# t = ToyCipher(block_len=3, rounds=5)
# t.load_cipher("found_P_candidate_2.txt")
# hs = HiddenSum(t=t, key=[0, 0, 0])

#for i in range(2**3):
#    c = t.encrypt(t.int_to_binary(i, 3), "110")
#    m = hs.attack(c)
#    print("{} {} {}".format(i, c, m))

# k = "000"

# for i in range(2**3):
#     c = t.encrypt(t.int_to_binary(i, 3), k)
#     m = hs.attack(c)
#     print("{} {} {}".format(i, c, m))

while True:
    t = ToyCipher(block_len=5, rounds=1)
    try:
        hs = HiddenSum(N=5, k=2, t=t, key="00000")
        print("P: {}, S: {}".format(t.P, t.S))
    except ValueError as e:
        continue
