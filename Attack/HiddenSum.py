#!/usr/bin/env python3

"""Preform hidden sum attack."""

from .Matrix import Matrix
from .Operations import Operations
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
            o = Operations(N=N, k=k)
            self.t = t
        self.N = N
        self.k = k
        self.key = key
        self.tilde, self.tilde_inv = o.phi_map(t.P)
        self.P_tilde = self.lambda_tilde(t.P)

        # Make sure that S and P is attackable
        self.__is_attackable()

        if key == None:
            M, zero = self.create_M([0 for _ in range(N)])
            M_inv = self.calculate_inverse(M)
            if M_inv == []:
                raise ValueError("The P and S box combination is not attackable, inverse of M undefined.")
        else:
            if type(key) == str:
                self.key = [int(i) for i in key]
            self.M, self.zero = self.create_M(self.key)
            self.M_inv = self.calculate_inverse(self.M)
            if self.M_inv == []:
                raise ValueError("The P and S box combination is not attackable, inverse of M undefined.")

        super().__init__()

    def __is_attackable(self):
        """
        Check that S and P boxes are attackable.
        """
        lam = self.calculate_inverse(self.t.P)
        lam_r = self.lambda_GL_ring(self.t.P)

        if (lam == [] or lam_r == []):
            raise ValueError("P-box is not vulnerable.")

        if not self.__lambda_check():
            raise ValueError("Lambda not in XOR or Circ.")

        self.__check_S_attackability()

    def __check_S_attackability(self):
        """
        Check S box attackability.
        """
        r = Operations(N=self.N, k=self.k)
        for S in self.t.S:
            for x in range(2**int(self.N/self.t.num_of_gamma)):
                for y in range(2**int(self.N/self.t.num_of_gamma)):
                    xry = r.ring(x, y)
                    f_xry = S[xry]

                    fx = S[x]
                    fy = S[y]
                    fx_r_fy = r.ring(fx, fy)

                    if f_xry != fx_r_fy:
                        raise ValueError("S-box is not vulnerable.")

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

    def change_key(self, key):
        """
        Change the M matrix for a new key.

        Parameters
        ----------
        key : list of int

        Returns
        -------
        None

        Raise
        -----
        ValueError
            if M is not invertable
        """
        if type(key) == str:
            self.key = [int(i) for i in key]
        else:
            self.key = key
        self.M, self.zero = self.create_M(self.key)
        self.M_inv = self.calculate_inverse(self.M)
        if self.M_inv == []:
            raise ValueError("The P and S box combination is not attackable.")

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
        if type(c) == str:
            c = [int(i) for i in c]
        if type(k) == int:
            k = self.int_to_binary(k, self.N)
        if type(k) == str:
            k = [int(i) for i in k]

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
