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

    def row_shift(self, M, x, y):
        tmp = 0
        for i in range(len(M)):
            tmp = M[x][i]
            M[x][i] = M[y][i]
            M[y][i] = tmp
        return M

    def mul_row(self, M, x, y):
        for i in range(len(M)):
            M[y][i] ^= M[x][i]
        return M

    # TODO Not working
    def calculate_inverse(self, A):
        I = self.get_identity(len(A))
        foundPivot = False
        for i in range(len(A)):
            if A[i][i] != 1:
                for j in range(i+1, len(A)):
                    if A[j][i] == 1:
                        foundPivot = True
                        A = self.row_shift(A, i, j)
                        I = self.row_shift(I, i, j)
                        break
                if foundPivot == False:
                    return []
                else:
                    foundPivot = False
            for j in range(i+1, len(A)):
                if A[j][i] == 1:
                    A = self.mul_row(A, i, j)
                    I = self.mul_row(I, i, j)

        for i in range(len(A)-1, 0, -1):
            for j in range(i-1, -1, -1):
                if A[j][i] == 1:
                    A = self.mul_row(A, i, j)
                    I = self.mul_row(I, i, j)
        return I