#!/usr/bin/env python3

"""Preform hidden sum attack."""

from .Matrix import Matrix
from ToyCipher.ToyCipher import ToyCipher
from .Operations import Operations

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
    t : Class
        a ToyCipher class

    Methods
    -------
    __is_attackable():
        check that S and P boxes are attackable
    __check_S_attackability():
        check S box attackability
    __lambda_check():
        make sure that lambda are in XOR and Ring
    phi_pos_a(a, P_a):
        determine Phi val at pos a substitution using ring
    phi_pos_a_xor(a, P_a):
        determine Phi val at pos a substitution using xor
    phi_map(P):
        calculate the Phi and Phi inverse map
    lambda_tilde(P):
        generate the lambda tilde matrix from P
    lambda_GL_ring(A_t):
        calculate that GL_\circ of A is true
    create_M(t):
        create the M matrix from ToyCipher class t
    attack(c, key):
        decrypt the cipher c
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
        key : list of int or string
            the key used to encrypt

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
        self.key = key
        self.tilde, self.tilde_inv = self.phi_map(t.P)
        self.P_tilde = self.lambda_tilde(t.P)
        # if key == None:
        #     M, zero = self.create_M([0 for _ in range(N)])
        #     M_inv = self.calculate_inverse(M)
        #     if M_inv == []:
        #         raise ValueError("The P and S box combination is not attackable.")
        # else:
        #     self.M, self.zero = self.create_M([0 for _ in range(N)])
        #     self.M_inv = self.calculate_inverse(self.M)
        #     if self.M_inv == []:
        #         raise ValueError("The P and S box combination is not attackable.")

        if not self.__lambda_check():
            raise ValueError("Lambda not in XOR or Circ.")

        check = self.__is_attackable()

        if check == 1:
            raise ValueError("P-box is not vulnerable.")
        # elif check == 2:
        #    raise ValueError("S-box is not vulnerable.")
        super().__init__()

    def __is_attackable(self):
        """
        Check that S and P boxes are attackable.
        """
        lam = self.calculate_inverse(self.t.P)
        lam_r = self.lambda_GL_ring(self.t.P)
        P_check = 0 if (lam != [] and lam_r != []) else 1
        if P_check == 1:
            return 1
        #S_check = self.__check_S_attackability()
        #if S_check == 2:
        #    return 2
        return 0

    def __check_S_attackability(self):
        """
        Check S box attackability.
        """
        r = Operations(N=self.N, k=self.k)
        for x in range(2**self.N):
            for y in range(2**self.N):
                xry = r.ring(x, y)
                f_xry = self.t.S[xry]

                fx = self.t.S[x]
                fy = self.t.S[y]
                fx_r_fy = r.ring(fx, fy)

                if f_xry != fx_r_fy:
                    return 2
        return 0

    def __lambda_check(self):
        """
        Make sure that lambda are in XOR and Ring.
        """
        r = Operations(N=self.N, k=self.k)
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
                x_o_y = self.int_to_binary(r.ring(x, y), self.N)
                x_o_y_l = self.binary_to_int(self.matrix_mul_row_column(x_o_y, self.t.P))

                # x\lam o y\lam
                x_lo = self.binary_to_int(self.matrix_mul_row_column(self.int_to_binary(x, self.N), self.t.P))
                y_lo = self.binary_to_int(self.matrix_mul_row_column(self.int_to_binary(y, self.N), self.t.P))
                xl_o_yl = r.ring(x_lo, y_lo)

                if x_o_y_l != xl_o_yl:
                    return False
        return True

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
        r = Operations(N=self.N, k=self.k)
        P = copy.deepcopy(P_a)
        if type(a) == int:
            a = self.int_to_binary(a, self.N)
        for i in range(len(a)):
            for j in range(len(P[0])):
                P[i][j] = P[i][j]*a[i]
        gamma = r.ring(self.binary_to_int(P[0]), self.binary_to_int(P[1]))
        for i in range(2, len(P)):
            gamma = r.ring(gamma, self.binary_to_int(P[i]))
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

    def lambda_tilde(self, P):
        """
        Generate the lambda tilde matrix from P.

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
        r = Operations(N=self.N, k=self.k)
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
                                r.ring(self.binary_to_int(A_t[j]),
                                          self.binary_to_int(A_t[i])),
                                          self.N
                                )
                    A = A_t

                    I_t = copy.deepcopy(I)
                    I_t[j] = self.int_to_binary(
                                r.ring(self.binary_to_int(I_t[j]),
                                          self.binary_to_int(I_t[i])),
                                          self.N
                                )
                    I = I_t

        for i in range(len(A)-1, 0, -1):
            for j in range(i-1, -1, -1):
                if A[j][i] == 1:
                    A_t = copy.deepcopy(A)
                    A_t[j] = self.int_to_binary(
                                r.ring(self.binary_to_int(A_t[j]),
                                       self.binary_to_int(A_t[i])),
                                       self.N
                                )
                    A = A_t

                    I_t = copy.deepcopy(I)
                    I_t[j] = self.int_to_binary(
                                r.ring(self.binary_to_int(I_t[j]),
                                       self.binary_to_int(I_t[i])),
                                       self.N
                                )
                    I = I_t
        return I

    def create_M(self, key):
        """
        Create the M used to traverse inbetween ciphertext and message.

        Parameters
        ----------
        key : list of int
            the key to the cipher

        Returns
        -------
        tuple
            M : the M matrix
            zero : the zero matrix used to mul with the cipher
        """
        zero = [0 for _ in range(self.N)]
        zero = self.t.encrypt(zero, key)
        zero = self.tilde[self.binary_to_int(zero)]
        zero = self.int_to_binary(zero, self.N)

        I = self.get_identity(self.N)
        M = []
        for e in I:
            v = self.t.encrypt(e, key)
            v_tilde = self.int_to_binary(self.tilde[self.binary_to_int(v)], self.N)
            M.append(self.xor(v_tilde, zero))

        return M, zero

    def attack(self, c, k=None):
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

        Raises
        ------
        ValueError
            When a key is neither provided to the function
            nor the class.
        """
        if type(c) == int:
            c = self.int_to_binary(c, self.N)
        if type(k) == int:
            c = self.int_to_binary(k, self.N)

        if k != None:
            M, zero = self.create_M(k)
            M_inv = self.calculate_inverse(M)
            if M_inv == []:
                raise ValueError("M is not invertable.")

            c_tilde = self.int_to_binary(self.tilde[self.binary_to_int(c)], self.N)
            c_t = self.xor(c_tilde, zero)
            m_tilde = self.matrix_mul_row_column(c_t, M_inv)
            m = self.tilde_inv[self.binary_to_int(m_tilde)]
        elif self.key != None:
            c_tilde = self.int_to_binary(self.tilde[self.binary_to_int(c)], self.N)
            c_t = self.xor(c_tilde, self.zero)
            m_tilde = self.matrix_mul_row_column(c_t, self.M_inv)
            m = self.tilde_inv[self.binary_to_int(m_tilde)]
        else:
            raise ValueError("No key defined.")

        return m
