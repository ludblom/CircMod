#!/usr/bin/env python3

from Circ.Matrix import HiddenSum


def print_ring_table(c, n):
    for i in range(n):
        for j in range(n):
            print("{}".format(c.ring(i,j)), end=' ')
        print()
    print()


def print_xor_table(c, n):
    for i in range(n):
        for j in range(n):
            print("{}".format(c.xor(i,j)), end=' ')
        print()
    print()


def test():
    c = HiddenSum(N=3,k=1)

    print("-- XOR TABLE --")
    print_xor_table(c, 8)

    print("-- RING TABLE --")
    print_ring_table(c, 8)

    # Bex
    # print(c.Bex)


if __name__ == '__main__':
    test()
