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
        S = {}
        S_I = {}
        random_values = [i for i in range(2**block_len)]
        sorted_values = [i for i in range(2**block_len)]
        random.shuffle(random_values)
        for i in range(2**block_len):
            S[sorted_values[i]] = random_values[i]
            S_I[random_values[i]] = sorted_values[i]
        return S, S_I

    def preform_data_substitution(self, data, encrypt):
        """
        Preform the substitution.

        Parameters
        ----------
        data : the data to substitute
        encrypt : True if we are to encrypt, False if decryption
        """
        if(encrypt):
            data = self.S[self.binary_to_int(data)]
        else:
            data = self.S_I[self.binary_to_int(data)]

        return data
