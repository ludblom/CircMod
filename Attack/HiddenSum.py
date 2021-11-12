#!/usr/bin/env python3

"""Preform hidden sum attack."""

from .Matrix import Matrix
from ToyCipher.ToyCipher import ToyCipher

import copy


class HiddenSum(Matrix):
    """
    A class to preform hidden sum attack.

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
    phi_pos_a(a, P_a):
        determine Phi val at pos a substitution using ring
    phi_pos_a_xor(a, P_a):
        determine Phi val at pos a substitution using xor
    lamb(P):
        preform the lambda calculation
    create_M(t):
        create the M matrix from ToyCipher class t
    """

    def __init__(self, N=3, k=1, t=None, key=None):
        """
        Init default parameters.

        Parameters
        ----------
        N : int
            size of the matrix in x and y direction
        k : int
            size of the modifying matrix in x direction
        t : Class ToyCipher
            a ToyCipher class
        key : list of int
            the key

        Raises
        ------
        ValueError
            if no ToyCipher class is defined
        """
        if t == None:
            raise ValueError("No ToyCipher defined.")
        else:
            self.t = t
        self.N = N
        self.k = k
        self.Bo = self.__generate_Bo(N, k)
        self.Bex = self.__generate_Bex()
        self.tilde, self.tilde_inv = self.phi_map(t.P)
        self.P_tilde = self.lambda_tilde(t.P)
        self.M, self.zero = self.create_M(t, key)
        self.M_inv = self.calculate_inverse(self.M)
        if self.M_inv == []:
            raise ValueError("The P and S box combination is not attackable.")
        if not self.__lambda_check():
            raise ValueError("Lambda not in XOR or Circ.")
        check = self.__is_attackable()
        if check == 1:
            raise ValueError("P-box is not vulnerable.")
        elif check == 2:
            raise ValueError("S-box is not vulnerable.")
        super().__init__()

    def __is_attackable(self):
        lam = self.calculate_inverse(self.t.P)
        lam_r = self.lambda_GL_ring(self.t.P)
        P_check = 0 if (lam != [] and lam_r != []) else 1
        if P_check == 1:
            return 1
        S_check = self.__check_S_attackability()
        if S_check == 2:
            return 2
        return 0

    def __check_S_attackability(self):
        for x in range(2**self.N):
            for y in range(2**self.N):
                xry = self.ring(x, y)
                f_xry = self.t.S[xry]

                fx = self.t.S[x]
                fy = self.t.S[y]
                fx_r_fy = self.ring(fx, fy)

                if f_xry != fx_r_fy:
                    return 2
        return 0

    def __lambda_check(self):
        for x in range(2**self.N):
            for y in range(2**self.N):
                # (x + y)\lam = x\lam + y\lam
                # (x + y)\lam
                x_p_y = self.int_to_binary(x^y, self.N)
                x_p_y_l = self.binary_to_int(self.matrix_mul_row_column(x_p_y, self.t.P))

                # x\lam + y\lam
                x_l = self.binary_to_int(self.matrix_mul_row_column(self.int_to_binary(x, self.N), self.t.P))
                y_l = self.binary_to_int(self.matrix_mul_row_column(self.int_to_binary(y, self.N), self.t.P))
                xl_p_yl = x_l^y_l

                if xl_p_yl != x_p_y_l:
                    return False

                # (x o y)\lam = x\lam o y\lam
                # (x o y)\lam
                x_o_y = self.int_to_binary(self.ring(x, y), self.N)
                x_o_y_l = self.binary_to_int(self.matrix_mul_row_column(x_o_y, self.t.P))

                # x\lam o y\lam
                x_lo = self.binary_to_int(self.matrix_mul_row_column(self.int_to_binary(x, self.N), self.t.P))
                y_lo = self.binary_to_int(self.matrix_mul_row_column(self.int_to_binary(y, self.N), self.t.P))
                xl_o_yl = self.ring(x_lo, y_lo)

                if x_o_y_l != xl_o_yl:
                    return False
        return True

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

    def phi_pos_a(self, a, P_a):
        """
        Calculate Phi for indent a using ring.

        Parameters
        ----------
        a : int or list of int
        P_a : list of int

        Returns
        -------
        int
            Phi on pos a using ring
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

    def phi_pos_a_xor(self, a, P_a):
        """
        Calculate Phi for indent a using XOR.

        Parameters
        ----------
        a : int or list of int
        P_a : list of int

        Returns
        -------
        int
            Phi at position a using XOR
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

    def phi_map(self, P):
        """
        Calculate the Phi and Phi inverse map.

        Parameters
        ----------
        P : list of list of int
            The P box

        Returns
        -------
        tuple of list of int
            Phi and Phi inverse
        """
        # TODO Only for 3x3 matrix atm
        r = []
        x = []
        phi = [0 for i in range(2**self.N)]
        phi_inv = [i for i in range(2**self.N)]

        for i in range(2**self.N):
            ring = self.phi_pos_a(i, P)
            xor = self.phi_pos_a_xor(i, P)
            r.append(ring)
            x.append(xor)
            if ring != xor:
                phi[ring] = xor
            else:
                phi[ring] = ring

        pos = []
        for i in range(2**self.N):
            if r[i] != x[i]:
                pos.append(i)

        phi_inv[pos[0]] = pos[1]
        phi_inv[pos[1]] = pos[0]

        return phi, phi_inv

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

    def lambda_tilde(self, P):
        """
        Generate the lambda tilde matrix from P

        Parameters
        ----------
        P : list of int
            the permutation matrix (lambda)

        Returns
        -------
        list of int
            the lambda_tilde matrix
        """
        P_tilde = []
        for i in P:
            P_tilde.append(self.int_to_binary(self.tilde[self.binary_to_int(i)], self.N))
        return P_tilde

    def lambda_GL_ring(self, A_t):
        """
        Calculate that GL_\circ of A is true.

        Parameters
        ----------
        A_t : list of int

        Returns
        -------
        list of int
            the inverse of A_t
        """
        A = copy.deepcopy(A_t)
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
                    A_t = copy.deepcopy(A)
                    A_t[j] = self.int_to_binary(
                                self.ring(self.binary_to_int(A_t[j]),
                                          self.binary_to_int(A_t[i])),
                                          self.N
                                )
                    A = A_t

                    I_t = copy.deepcopy(I)
                    I_t[j] = self.int_to_binary(
                                self.ring(self.binary_to_int(I_t[j]),
                                          self.binary_to_int(I_t[i])),
                                          self.N
                                )
                    I = I_t

        for i in range(len(A)-1, 0, -1):
            for j in range(i-1, -1, -1):
                if A[j][i] == 1:
                    A_t = copy.deepcopy(A)
                    A_t[j] = self.int_to_binary(
                                self.ring(self.binary_to_int(A_t[j]),
                                          self.binary_to_int(A_t[i])),
                                          self.N
                                )
                    A = A_t

                    I_t = copy.deepcopy(I)
                    I_t[j] = self.int_to_binary(
                                self.ring(self.binary_to_int(I_t[j]),
                                          self.binary_to_int(I_t[i])),
                                          self.N
                                )
                    I = I_t
        return I

    def create_M(self, t, key):
        """
        Create the M used to traverse inbetween ciphertext and message.

        Parameters
        ----------
        t : Class ToyCipher
            the already created ToyCipher class
        key : list of int
            the key to the cipher

        Returns
        -------
        tuple
            M : the M matrix
            zero : the zero matrix used to mul with the cipher
        """
        zero = [0 for _ in range(self.N)]
        zero = t.encrypt(zero, key)
        zero = self.tilde[self.binary_to_int(zero)]
        zero = self.int_to_binary(zero, self.N)

        I = self.get_identity(self.N)
        M = []
        for e in I:
            v = t.encrypt(e, key)
            v_tilde = self.int_to_binary(self.tilde[self.binary_to_int(v)], self.N)
            M.append(self.xor(v_tilde, zero))

        return M, zero

    def attack(self, c):
        """
        Decrypt the cipher c.

        Parameters
        ----------
        c : list of int or int
            the cipher

        k : list of int or int
            the key

        Returns
        -------
        int
        """
        if type(c) == int:
            c = self.int_to_binary(c, self.N)
        c_tilde = self.int_to_binary(self.tilde[self.binary_to_int(c)], self.N)
        c_t = self.xor(c_tilde, self.zero)
        m_tilde = self.matrix_mul_row_column(c_t, self.M_inv)
        m = self.tilde_inv[self.binary_to_int(m_tilde)]

        return m
