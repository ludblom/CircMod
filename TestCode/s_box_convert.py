#!/usr/bin/env python3

from Attack.Matrix import Matrix

S_b = [[0,0,0],[1,1,0],[0,1,1],[1,1,1],[1,0,0],[0,0,1],[1,0,1],[0,1,0]]

m = Matrix()

for i in range(2**6):
    b = m.int_to_binary(i, 6)[::-1]
    b_1 = S_b[m.binary_to_int(b[3:])]
    b_2 = S_b[m.binary_to_int(b[:3])]
    bb = b_2+b_1
    bbb = bb[::-1]
    print("{} {}".format(i, m.binary_to_int(bbb)))
