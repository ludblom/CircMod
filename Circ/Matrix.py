#!/usr/bin/env python3


class HiddenSum:
    def __init__(self, N=5, k=2):
        self.biggest_binary = k
        self.Bo = self.generate_Bo(N, k)
        self.Bex = self.generate_Bex()
        super().__init__()

    def __str__(self):
        string = ''
        for j in self.M:
            for i in j:
                string += '{} '.format(str(i))
            string += '\n'
        return string

    def generate_Bex(self):
        Bex = []
        Bo_size = len(self.Bo)
        for i in range(Bo_size):
            tmp = []
            for j in range(Bo_size):
                tmp.append(self.int_to_binary(self.Bo[j][i]))
            Bex.append(tmp)
        return Bex

    def generate_Bo(self, N, k):
        alpha = self.binary_to_int([1 for i in range(k)])
        n = N-k
        Bo = [[0 for i in range(n)] for i in range(n)]
        for j in range(n):
            for i in range(j+1, n):
                Bo[j][i] = alpha
                Bo[i][j] = alpha
            alpha -= 1
        return Bo

    def int_to_binary(self, i):
        b = []
        while i != 0:
            b.append(i%2)
            i = int(i/2)
        while(len(b) < self.biggest_binary):
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




# a = Matrix(M=[3,2])
# b = Matrix(M=[2,2])
# c = a.circ(b)



# def print_matrix(M):
#     for j in M:
#         for i in j:
#             print(i, end=' ')
#         print()
#     print()


# def get_identity(n):
#     I = []
#     one = 0
#     for j in range(n):
#         I_i = []
#         for i in range(n):
#             if one == i:
#                 I_i.append(1)
#             else:
#                 I_i.append(0)
#         one += 1
#         I.append(I_i)
#     return I


# def sum_matrix(x, y):
#     #print("X: {}".format(x))
#     #print("Y: {}".format(y))
#     sum = 0
#     for i in range(len(x)-1, 0, -1):
#         sum = sum + x[i] + y
#         sum = sum%2
#     return sum


# # TODO Do not convert x to a binary list
# def mul_matrix(x, M):
#     val = []

#     for i in range(len(M)):
#         tmp = []
#         for j in range(len(M)):
#             tmp.append(x & M[j][i])

#         val.append(sum(tmp)%2)
#     return val


# def conv_binary(x):
#     num = [0 for i in range(4)]
#     while(True):
#         if x == 0:
#             num.append(x%2)



# def calc_vals():
#     M_1 = [[1,0,0,1],[0,1,1,0],[0,0,1,0],[0,0,0,1]]
#     M_2 = [[1,0,1,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
#     M_3 = get_identity(4)
#     M_n = [[1,0,1,1],[0,1,1,0],[0,0,1,0],[0,0,0,1]]

#     M = []
#     M.append(M_1)
#     M.append(M_2)
#     M.append(M_3)
#     for i in range(3, 16):
#         M.append(M_n)

#     vals = []

#     for y in range(16):
#         vals_tmp = []
#         for x in range(16):
#             vals_tmp.append(sum_matrix(mul_matrix(conv_binary(x), M[x]), y))
#         vals.append(vals_tmp)
#     print(vals)
