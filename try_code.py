#!/usr/bin/env python3

from Attack.RingOperator import Ring
from ToyCipher.ToyCipher import ToyCipher


def print_ring_table(c, n):
    for i in range(n):
        for j in range(n):
            print("{}".format(c.ring(i,j)), end=' ')
        print()
    print()


def print_xor_table(c, n):
    for i in range(n):
        for j in range(n):
            print("{}".format(i ^ j), end=' ')
        print()
    print()


def test():
    c = Ring(N=3,k=1)

    print("-- XOR TABLE --")
    print_xor_table(c, 8)

    print("-- RING TABLE --")
    print_ring_table(c, 8)

    # Bex
    # print(c.Bex)


def print_function(N, k):
    c = Ring(N=N, k=k)
    print("$\circ$ & ", end='')
    for i in range(2**N):
        if(i < 2**N-1):
            print("{} & ".format(i), end='')
        else:
            print("{} \\\\".format(i))

    for a in range(2**N):
        print("{} & ".format(a), end='')
        for b in range(2**N):
            if(b < 2**N-1):
                # Ring
                # print("{} & ".format(c.ring(a, b)), end='')
                # Xor
                print("{} & ".format(a ^ b), end='')
            else:
                # Ring
                # print("{} ".format(c.ring(a, b)), end='')
                print("{} ".format(a ^ b), end='')
        print("\\\\")


def toyCode():
    t = ToyCipher()
    print(t.S)
    print(t.S_I)


if __name__ == '__main__':
    toyCode()
