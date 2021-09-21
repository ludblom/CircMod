#!/usr/bin/env python3


class HiddenSum:
    def __init__(self, N=5, k=2):
        self.N = N
        self.k = k
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

        # Generate the different Bex
        for i in range(Bo_size):
            tmp = []
            for j in range(Bo_size):
                tmp.append(self.int_to_binary(self.Bo[j][i], self.k))
            Bex.append(tmp)

        # The last Bex should only have zeros
        tmp = []
        for j in range(Bo_size):
            tmp.append([0 for k in range(self.k)])
        Bex.append(tmp)

        return Bex

    # TODO 1 is 0 for me, have to figure out a good way to convert it
    def get_Bx(self, n):
        I = self.get_identity(self.N)
        if(n > self.N-self.k):
            Bx = self.Bex[0]
            for i in range(1, len(self.Bex)):
                Bx = self.tmp_sum(Bx, self.Bex[i])
        else:
            Bx = self.Bex[n-1]
        for i in range(len(Bx)):
            for j in range(len(Bx[0])-1, -1, -1):
                I[i][self.N-self.k + j] = Bx[i][j]
        return I

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

    def tmp_sum(self, a, b):
        mat = []
        for i in range(len(a)):
            tmp = []
            for j in range(len(a[0])):
                t = a[i][j]+b[i][j]
                tmp.append(t%2)
            mat.append(tmp)
        return mat

    def matrix_sum(self, a, b):
        tmp = []
        for i in range(len(a)):
            t = a[i]+b[i]
            tmp.append(t%2)
        return tmp

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

    def ring(self, a, b):
        a_m = self.int_to_binary(a, self.N)
        b_m = self.int_to_binary(b, self.N)
        print("a_m: {}, b_m: {}".format(a_m, b_m))
        Mx = self.get_Bx(b)
        print("Mx: {}".format(Mx))
        aM_b = self.matrix_mul(a_m, Mx)
        print("aM_b: {}".format(aM_b))
        aM_bb = self.matrix_sum(aM_b, b_m)
        print("aM_bb: {}".format(aM_bb))
        done = aM_bb
        return done




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
