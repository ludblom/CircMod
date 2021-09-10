#!/usr/bin/env python3


def int_to_binary(i):
    b = []
    while i != 0:
        b.append(i%2)
        i = int(i/2)
    return b


def binary_to_int(b):
    i = 0
    p = 0
    for j in b:
        if j == 1:
            i += 2**p
        p += 1
    return i


def generate_Bo(N, k):
    Bex =  [[0 for i in range(N)] for j in range(N)]
    alpha = k
    for i in range(N-k):
        for j in range(i+1, N-k):
            print("i: {}, j: {}".format(i, j))
            Bex = insert_alpha(alpha, i, j, Bex)
        alpha -= 1


class Matrix:
    def __init__(self, gen_Bo=0, N=5, k=2, M=[]):
        if(gen_Bo == 1):
            self.M = generate_Bo(N, k)
        else:
            self.M = M
        super().__init__()

    def __str__(self):
        return str(self.M)



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
