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
    permutation_box(num_of_octals):
        Create the encryption (P) and decryption (P_I) permutation matrix
    convert_oct_to_binary(data):
        Convert octals to binary
    convert_binary_to_oct(data):
        Convert binary to octals
    p_box_multiplication(data, encrypt):
        Preform row multiplication
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

    def __check_linearity(self, P_tmp):
        """
        Check that a matrix is linear.

        Parameters
        ----------
        P_tmp : list of int

        Returns
        -------
        bool
        """
        l = self.xor(P_tmp[0], P_tmp[1])
        for i in range(2, len(P_tmp)):
            l = self.xor(l, P_tmp[i])

        zero = [0 for i in range(len(P_tmp))]

        if l == zero:
            return False

        return True

    def permutation_box(self):
        """
        Create the permutation and inverse permutation boxes.

        Parameters
        ----------
        None

        Returns
        -------
        tuple of P and P_I
            the encryption (P) and decryption (P_I) permutation box (binary)
        """
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
            linear = self.__check_linearity(P_tmp)
            if(not linear):
                P_I = []
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
