#!/usr/bin/env python3

"""Defines the Ring (o) operator."""

from .Matrix import Matrix

import copy


class Ring(Matrix):
    """
    The Ring class.

    ...

    Attributes
    ----------
    N : int
        size of the matrix in x and y direction
    k : int
        size of the modifying matrix in x direction

    Methods
    -------
    __generate_Bex():
        generate the B_ex matrices
    __generate_Bo(N, k):
        generate the B_o matrix
    get_Bx(b):
        generate the B_x[b]'th matrix
    ring(a, b):
        preform the ring operator
    dot(a, b):
        preform the dot product using ring
    gamma(a, P_a):
        determine gamma substitution using ring
    gamma_xor(a, P_a):
        determine gamma substitution using xor
    lamb(P):
        preform the lambda calculation
    """

    def __init__(self, N=6, k=2):
        """
        Init default parameters.

        Parameters
        ----------
        N : int
            size of the matrix in x and y direction
        k : int
            size of the modifying matrix in x direction
        """
        self.N = N
        self.k = k
        self.Bo = self.__generate_Bo(N, k)
        self.Bex = self.__generate_Bex()
        super().__init__()

    def __generate_Bex(self):
        """
        Generate all B_ex matrices by using the B_o matrix.

        Parameters
        ----------
        None

        Returns
        -------
        list of list of int
            return the B_ex matrices
        """
        Bex = []
        Bo_size = len(self.Bo)

        zeroMatrix = []
        for j in range(Bo_size):
            zeroMatrix.append([0 for k in range(self.k)])

        # Generate the different Bex
        for i in range(Bo_size):
            tmp = []
            for j in range(Bo_size):
                tmp.append(self.int_to_binary(self.Bo[j][i], self.k))
            Bex.append(tmp)

        return Bex

    def __generate_Bo(self, N, k):
        """
        Generate the B_o matrix in alpha notation.

        Parameters
        ----------
        N : int
            the size of the B_o matrix in binary
        k : int
            the size in x direction of the modifying matrix

        Returns
        -------
        list of int
            B_o in alpha notation
        """
        alpha = self.binary_to_int([1 for i in range(k)])
        n = N-k
        Bo = [[0 for i in range(n)] for i in range(n)]
        for j in range(n):
            for i in range(j+1, n):
                Bo[j][i] = alpha
                Bo[i][j] = alpha
            alpha -= 1
        return Bo

    def get_Bx(self, b):
        """
        Get the B_x variable.

        Parameters
        ----------
        b : int or list of int
            the b'th B_x matrix as either binary or int

        Returns
        -------
        list of int
            the B_x matrix
        """
        I = self.get_identity(self.N)
        Bx = []

        for i in range(len(self.Bo)):
            tmp = []
            for j in range(self.k):
                tmp.append(0)
            Bx.append(tmp)

        if type(b) is not list:
            b = self.int_to_binary(b, self.N)

        for i in range(len(b)):
            if b[i] == 1:
                if i < (self.N-self.k):
                    Bx = self.matrix_sum(Bx, self.Bex[i])

        for i in range(len(Bx)):
            for j in range(self.k):
                I[i][self.N-self.k + j] = Bx[i][j]

        return I

    def ring(self, a, b):
        """
        Preform the Ring (o) operation.

        Parameters
        ----------
        a : int
        b : int

        Returns
        -------
        int
            a o b
        """
        a_m = self.int_to_binary(a, self.N)
        b_m = self.int_to_binary(b, self.N)
        Mx = self.get_Bx(b)
        aM_b = self.matrix_mul_row_column(a_m, Mx)
        aM_bb = self.matrix_sum(aM_b, b_m)
        return self.binary_to_int(aM_bb)

    def dot(self, a, b):
        """
        Preform the Dot (.) product using circ.

        Parameters
        ----------
        a : int
        b : int

        Returns
        -------
        int
            a.b
        """
        a_plus_b = self.matrix_sum(self.int_to_binary(a, self.N), self.int_to_binary(b, self.N))
        a_ring_b = self.int_to_binary(self.ring(a, b), self.N)
        a_dot_b = self.matrix_sum(a_plus_b, a_ring_b)
        return self.binary_to_int(a_dot_b)

    def gamma(self, a, P_a):
        """
        Preform gamma using ring.

        Parameters
        ----------
        a : int or list of int
        P_a : list of int

        Returns
        -------
        int
            gamma
        """
        P = copy.deepcopy(P_a)
        if type(a) == int:
            a = self.int_to_binary(a, self.N)
        for i in range(len(a)):
            for j in range(len(P[0])):
                P[i][j] = P[i][j]*a[i]
        gamma = self.ring(self.binary_to_int(P[0]), self.binary_to_int(P[1]))
        for i in range(2, len(P)):
            gamma = self.ring(gamma, self.binary_to_int(P[i]))
        return gamma

    def gamma_xor(self, a, P_a):
        """
        Preform gamma using xor.

        Parameters
        ----------
        a : int or list of int
        P_a : list of int

        Returns
        -------
        int
            gamma
        """
        P = copy.deepcopy(P_a)
        if type(a) == int:
            a = self.int_to_binary(a, self.N)
        for i in range(len(a)):
            for j in range(len(P[0])):
                P[i][j] = P[i][j]*a[i]
        gamma = self.xor(P[0], P[1])
        for i in range(2, len(P)):
            gamma = self.xor(gamma, P[i])
        return self.binary_to_int(gamma)

    def phi(self, P):
        """
        Calculate phi.

        Parameters
        ----------
        P : list of list of int
            The P box

        Returns
        -------
        list of int
            Phi
        """
        phi = [0 for i in range(2**self.N)]

        for i in range(2**self.N):
            ring = self.gamma(i, P)
            xor = self.gamma_xor(i, P)
            if ring != xor:
                phi[ring] = xor
            else:
                phi[ring] = ring
        return phi

    def matrix_mul_row_ring(self, M, x, y):
        """
        Multiplicate row x with y using ring.

        Parameters
        ----------
        M : list of list of int
            the matrix
        x : int
            x pos
        y : int
            y pos

        Returns
        -------
        list of list of int
            the new M
        """
        a_i = self.binary_to_int(M[y])
        b_i = self.binary_to_int(M[x])
        M_t = self.int_to_binary(self.ring(a_i, b_i), len(M))
        for i in range(len(M)):
            M[y][i] = M_t[i]
        return M
