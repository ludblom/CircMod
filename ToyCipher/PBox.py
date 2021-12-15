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
