#!/usr/bin/env python3

"""SBox used in the ToyCipher class."""

import random


class SBox:
    """
    The SBox class.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    substitution_box(block_len):
        Generate the substitution box
    preform_data_substitution(data, encrypt):
        Preform substitution
    """

    def __init__(self):
        """
        Init default parameters.

        Parameters
        ----------
        S : list of ints
            Substitution box for encryption
        S_I : list of ints
            Substitution box for decryption
        """
        self.S, self.S_I = self.substitution_box(self.block_len)
        super().__init__()

    def substitution_box(self, block_len):
        """
        Create the substitution box.

        Parameters
        ----------
        block_len : int
            the size of the block

        Returns
        -------
        tuple of S and S_I
            the encryption (S) and decryption (S_I) substitution box
        """
        if block_len%self.num_of_gamma != 0:
            raise ValueError("Num of gamma is not dividable with length of P.")

        S = [{} for _ in range(self.num_of_gamma)]
        S_I = [{} for _ in range(self.num_of_gamma)]

        random_values = [[i for i in range(2**int(block_len/self.num_of_gamma))] for _ in range(self.num_of_gamma)]
        sorted_values = [i for i in range(2**int(block_len/self.num_of_gamma))]
        [random.shuffle(r) for r in random_values]

        for i in range(self.num_of_gamma):
            for j in range(2**int(block_len/self.num_of_gamma)):
                S[i][sorted_values[j]] = random_values[i][j]
                S_I[i][random_values[i][j]] = sorted_values[j]

        return S, S_I

    def preform_data_substitution(self, data, encrypt, section):
        """
        Preform the substitution.

        Parameters
        ----------
        data : list of int
            the data to substitute
        encrypt : bool
            True if we are to encrypt, False if decryption
        section : int
            which S-box to use

        Returns
        -------
        list of int
        """
        length = len(data)

        if(encrypt):
            data = self.S[section][self.binary_to_int(data)]
        else:
            data = self.S_I[section][self.binary_to_int(data)]

        return self.int_to_binary(data, length)
