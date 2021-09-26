#!/usr/bin/env python3

class Matrix:
    def int_to_binary(self, i, l):
        b = []
        while i != 0:
            b.append(i%2)
            i = int(i/2)
        while(len(b) < l):
            b.append(0)
        return b

    def binary_to_int(self, b):
        i = 0
        p = 0
        for j in b:
            if j == 1:
                i += 2**p
            p += 1
        return i

    def matrix_mul(self, a, b):
        prod = []
        for j in range(len(a)):
            tmp = []
            for i in range(len(b)):
                tmp.append(a[i]&b[i][j])
            prod.append(sum(tmp)%2)
        return prod

    def matrix_sum(self, a, b):
        mat = []
        if type(a[0]) == list:
            for i in range(len(a)):
                tmp = []
                for j in range(len(a[0])):
                    t = a[i][j]+b[i][j]
                    tmp.append(t%2)
                mat.append(tmp)
        else:
            for i in range(len(a)):
                t = a[i]+b[i]
                mat.append(t%2)
        return mat

    def get_identity(self, n):
        I = []
        one = 0
        for j in range(n):
            I_i = []
            for i in range(n):
                if one == i:
                    I_i.append(1)
                else:
                    I_i.append(0)
            one += 1
            I.append(I_i)
        return I
