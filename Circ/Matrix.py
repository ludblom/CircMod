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

        zeroMatrix = []
        for j in range(Bo_size):
            zeroMatrix.append([0 for k in range(self.k)])

        # First Bex should only be zeros
        Bex.append(zeroMatrix)

        # Generate the different Bex
        for i in range(Bo_size):
            tmp = []
            for j in range(Bo_size):
                tmp.append(self.int_to_binary(self.Bo[j][i], self.k))
            Bex.append(tmp)

        Bex.append(zeroMatrix)

        return Bex

    def get_Bx(self, n):
        I = self.get_identity(self.N)
        Bx = self.Bex[n%len(self.Bex)]
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
        #print("a_m: {}, b_m: {}".format(a_m, b_m))
        Mx = self.get_Bx(b)
        #print("a = {}, b = {}, Mx: {}".format(a, b, Mx))
        aM_b = self.matrix_mul(a_m, Mx)
        #print("aM_b: {}".format(aM_b))
        aM_bb = self.matrix_sum(aM_b, b_m)
        #print(aM_bb)
        #print("aM_bb: {}".format(aM_bb))
        #print("Bex: {}, Mx: {}, aM_b: {}, aM_bb: {}".format(self.Bex, Mx, aM_b, aM_bb))
        done = aM_bb
        return done

    def xor(self, a, b):
        ab = []
        a_m = self.int_to_binary(a, self.N)
        b_m = self.int_to_binary(b, self.N)
        for i in range(len(a_m)):
            ab.append(a_m[i]^b_m[i])
        return self.binary_to_int(ab)
