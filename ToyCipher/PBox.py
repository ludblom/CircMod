#!/usr/bin/env python3

"""PBox used in the ToyCipher class."""

import copy
import random


class PBox:
    """
    The PBox class.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    __verify_validity(P):
        Verify that P is a valid gamma in terms of content and size.
    permutation_box(num_of_octals):
        Create the encryption (P) and decryption (P_I) permutation matrix
    p_box_multiplication(data, encrypt):
        Preform row multiplication
    find_attackable_lambda(N, k):
        faster way to find attackable lambda
    """

    def __init__(self):
        """
        Init default parameters.

        Parameters
        ----------
        P : list of int
            a binary matrix
        P_I : list of int
            inverse matrix of P
        """
        self.P, self.P_I = self.permutation_box()
        super().__init__()

    def __verify_validity(self, P):
        """
        Verify that P is a valid gamma in terms of content and size.

        Parameters
        ----------
        P : list of int
            a gamma matrix

        Returns
        -------
        None

        Raises
        ------
        ValueError
            if P is not valid
        """
        counter = 0
        for row in P:
            counter += 1
            if len(row) != self.block_len:
                raise ValueError("P is not of correct size.")
            for elem in row:
                if type(elem) != int:
                    raise ValueError("P contain illegal characters.")
        if counter != self.block_len:
            raise ValueError("P is not of correct size.")

    def permutation_box(self, P=None):
        """
        Create the permutation and inverse permutation boxes.

        Parameters
        ----------
        P : list of int
            if P is defined use that as the gamma

        Returns
        -------
        tuple of P and P_I
            the encryption (P) and decryption (P_I) permutation box (binary)

        Raises
        ------
        ValueError
            if the matrix given is non-linear, in the wrong size
            or contain illegal characters
        """
        if P != None:
            self.__verify_validity(P)
            P_I = self.calculate_inverse(P)
            if P_I == []:
                raise ValueError("The P matrix given is non-linear.")
            else:
                self.P = P
                self.P_I = P_I
            return P, P_I

        P_I = []
        while P_I == []:
            P_tmp = []
            for _ in range(self.block_len):
                tmp = []
                for _ in range(self.block_len):
                    rand = random.randint(0, 1)
                    tmp.append(rand)
                P_tmp.append(tmp)
            P = copy.deepcopy(P_tmp)
            P_I = self.calculate_inverse(P_tmp)
        return P, P_I

    def p_box_multiplication(self, data, encrypt):
        """
        Preform multiplication of data on P or P_I.

        Parameters
        ----------
        data : list of octals
            the data to permutate
        encrypt : boolean
            True in encryption and False if decryption
        """
        if encrypt:
            res_data = self.matrix_mul_row_column(data, self.P)
        else:
            res_data = self.matrix_mul_row_column(data, self.P_I)
        return res_data

    def find_attackable_lambda(self, N, k):
        """
        Faster way to find attackable lambda.

        Parameters
        ----------
        N : int
            total size of the matrix
        k : int
            size of the k part

        Returns
        -------
        list of list of int

        Raises
        ------
        ValueError
            If the N and k combination is not correct
        """
        if N < k:
            raise ValueError('K cannot be greater or equal to N.')
        elif k <= 0:
            raise ValueError('K cannot be less than or equal to 0.')

        while True:
            M = [[0 for _ in range(N)] for _ in range(N)]

            l_Mi = []
            while l_Mi == []:
                l_M = [[random.randint(0, 1) for _ in range(N-k)] for _ in range(N-k)]
                l_Mi = self.calculate_inverse(l_M)

            r_Mi = []
            while r_Mi == []:
                r_M = [[random.randint(0, 1) for _ in range(k)] for _ in range(k)]
                r_Mi = self.calculate_inverse(r_M)

            right = [[random.randint(0, 1) for _ in range(k)] for _ in range(N-k)]

            for i in range(N):
                for j in range(N):
                    if i < N-k and j < N-k:
                        M[i][j] = l_M[i][j]
                    elif i < N-k and j >= N-k:
                        M[i][j] = right[i][j-(N-k)]
                    elif i >= N-k and j >= N-k:
                        M[i][j] = r_M[i-(N-k)][j-(N-k)]
                    else:
                        continue
            M_i = self.calculate_inverse(M)
            if M_i != []:
                break
        return M, M_i
