#!/usr/bin/env python3

from Circ.HiddenSum import HiddenSum


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


def print_function(N, k):
    c = HiddenSum(N=N, k=k)
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
                print("{} & ".format(c.xor(a, b)), end='')
            else:
                # Ring
                # print("{} ".format(c.ring(a, b)), end='')
                print("{} ".format(c.xor(a, b)), end='')
        print("\\\\")


if __name__ == '__main__':
    print_function(3, 1)
