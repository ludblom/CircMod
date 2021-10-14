#!/usr/bin/env python3

"""Matrix modification classes."""


class Matrix:
    """
    The Matrix class containing functions to modify matrices.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    int_to_binary(i, l):
        convert int to binary
    binary_to_int(b):
        convert binary to int
    matrix_mul(a, b):

    matrix_sum(a, b):
    get_identity(n):
    row_shift(M, x, y):
    mul_row(M, x, y):
    mul_row_column(x, M):
    calculate_inverse(A):
    xor(a, b):
    """

    def int_to_binary(self, i, l):
        """
        Convert an integer to binary.

        Parameters
        ----------
        i : int
            the integer to convert
        tot_num_of_bits : int
            total length of the binary

        Returns
        -------
        list of int
            the converted integer
        """
        b = []
        while i != 0:
            b.append(i % 2)
            i = int(i/2)
        while(len(b) < l):
            b.append(0)
        return b

    def binary_to_int(self, b):
        """
        Convert a binary to an integer.

        Parameters
        ----------
        b : list of int
            number of binary

        Returns
        -------
        int
        """
        i = 0
        p = 0
        for j in b:
            if j == 1:
                i += 2**p
            p += 1
        return i

    def matrix_sum(self, a, b):
        """
        Sum two matrices.

        Parameters
        ----------
        a : list of int
        b : list of int

        Returns
        -------
        list of int
        """
        mat = []
        if type(a[0]) == list:
            for i in range(len(a)):
                tmp = []
                for j in range(len(a[0])):
                    t = a[i][j]+b[i][j]
                    tmp.append(t % 2)
                mat.append(tmp)
        else:
            for i in range(len(a)):
                t = a[i]+b[i]
                mat.append(t % 2)
        return mat

    def get_identity(self, n):
        """
        Generate an identity matrix (size nxn).

        Parameters
        ----------
        n : int
            the size in x and y direction

        Returns
        -------
        list of int
            the identity matrix
        """
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
        """
        Shift the row of a matrix.

        Parameters
        ----------
        M : list of int
        x : int
        y : int

        Returns
        -------
        list of int
            shift row x with y
        """
        tmp = 0
        for i in range(len(M)):
            tmp = M[x][i]
            M[x][i] = M[y][i]
            M[y][i] = tmp
        return M

    def matrix_mul_row(self, M, x, y):
        """
        Multiplicate row x with y.

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
        for i in range(len(M)):
            M[y][i] ^= M[x][i]
        return M

    def matrix_mul_row_column(self, x, M):
        """
        Multiplicate [] with [[..]..] matrix.

        Parameters
        ----------
        a : list of int
        b : list of list of int

        Returns
        -------
        list of int
            the matrix product
        """
        row_col = []
        for j in range(len(x)):
            tmp = 0
            for i in range(len(x)):
                tmp ^= x[i] & M[i][j]
            row_col.append(tmp)
        return row_col

    def calculate_inverse(self, A):
        """
        Calculate the inverse of A.

        Parameters
        ----------
        A : list of int

        Returns
        -------
        list of int
            the inverse of A
        """
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
                    A = self.matrix_mul_row(A, i, j)
                    I = self.matrix_mul_row(I, i, j)

        for i in range(len(A)-1, 0, -1):
            for j in range(i-1, -1, -1):
                if A[j][i] == 1:
                    A = self.matrix_mul_row(A, i, j)
                    I = self.matrix_mul_row(I, i, j)
        return I

    def xor(self, a, b):
        """
        Xor two lists togother.

        Parameters
        ----------
        a : list of int
        b : list of int

        Returns
        -------
        list of int
            a XOR b

        Raises
        ------
        SyntaxError
            If lists are not of equal length
        """
        if len(a) != len(b):
            raise SyntaxError("Lists not of equal length.")
        c = []
        for i in range(len(a)):
            c.append(a[i]^b[i])
        return c
