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
        return P, P_I

    def convert_oct_to_binary(self, data):
        """
        Convert a list of octals to list of ints.

        Parameters
        ----------
        data : list of int
            a list of ints representing octals

        Returns
        -------
        list of int
            the binary representation of the octals
        """
        bin_data = []
        # Convert to string binary of size 3 (octal)
        bin_tmp = [format(i, '03b') for i in data]
        # Convert the strings to int
        for bin_part in bin_tmp:
            for b in bin_part:
                bin_data.append(int(b))
        return bin_data

    def convert_binary_to_oct(self, data):
        """
        Convert a list of binary ints to octals.

        Parameters
        ----------
        data : list of int
            a list of 1 and 0 ints

        Returns
        -------
        list of int
            list of octals
        """
        oct_data = []
        for i in range(0, len(data), 3):
            tmp = [str(j) for j in data[i:i+3]]
            oct_data.append(int('0b{}'.format(''.join(tmp)), 2))
        return oct_data

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
