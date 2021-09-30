#!/usr/bin/env python3

"""Key box used in the ToyCipher class."""

import random


class Key:
    """
    The Key class.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    key_box():
        create the encryption (K) and decryption (K_I) keybox
    xor_data_key(data, key):
        preform xor on the data and key
    new_key_round(key, encrypt):
        generate a new key round

    """

    def __init__(self):
        """
        Init default parameters.

        Parameters
        ----------
        K : list of int
            list of all key combinations to another
        K_I : list of int
            inverse list of K
        """
        self.K, self.K_I = self.key_box()
        super().__init__()

    def key_box(self):
        """
        Create the keybox.

        Parameters
        ----------
        None

        Returns
        -------
        tuple of list of int
            the key substitution (K) and its inverse (K_I)
        """
        K = {}
        K_I = {}
        random_values = [i for i in range(8)]
        random.shuffle(random_values)
        for i in range(8):
            K[i] = random_values[i]
            K_I[random_values[i]] = i
        return K, K_I

    def xor_data_key(self, data, key):
        """
        Preform xor on the data and the key.

        Parameters
        ----------
        data : list of int
        key : list of int

        Returns
        -------
        list of int
            list with the data xor the key
        """
        for i in range(len(key)):
            data[i] ^= key[i]
        return data

    def new_key_round(self, key, encrypt):
        """
        Generate a new key round.

        Parameters
        ----------
        key : list of int

        Returns
        -------
        list : int
            the new key round
        """
        tmp_key = []
        for i in range(self.block_len):
            if encrypt:
                tmp_key.append(self.K[key[i]])
            else:
                tmp_key.append(self.K_I[key[i]])

        # Reverse the order
        for i in range(len(tmp_key)):
            key[i] = tmp_key[::-1][i]

        return key
