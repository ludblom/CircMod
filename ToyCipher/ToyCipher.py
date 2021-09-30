#!/usr/bin/env python3

"""Create a ToyCipher."""

from Attack.Matrix import Matrix
from .SBox import SBox
from .PBox import PBox
from .Key import Key


class ToyCipher(Matrix, SBox, PBox, Key):
    """
    A class to represent the ToyCipher.

    ...

    Attributes
    ----------
    block_len : int
        the length of the block
    rounds : int
        how many rounds the cipher has

    Methods
    -------
    __octals(octs):
        Make sure a list or string only contain octals
    __check_input(data, key):
        Check that the inputs are correct (data and key)
    encrypt(data, key):
        encrypt the data
    decrypt(data, key):
        decrypt the data
    """

    def __init__(self, block_len=6, rounds=3):
        """
        Init default parameters.

        Parameters
        ----------
        block_len : int
            the length of the block
        rounds : int
            how many rounds the cipher has
        """
        self.block_len = block_len
        self.rounds = rounds
        super().__init__()

    def __octals(self, octs):
        """
        Make sure a list or string only is ocatals.

        Parameters
        ----------
        octs : list of int

        Returns
        -------
        bool
            True if between 0 and 7, otherwise False
        """
        if(type(octs) != list and type(octs) != str):
            return False

        for o in octs:
            if int(o) < 0 or int(o) > 7:
                return False
        return True

    def __check_input(self, data, key):
        """
        Make sure input is correct.

        Parameters
        ----------
        data : list or string (octals)
            list or string of octals to encrypt
        key : list or string (octals)
            list or string of octals for a key

        Returns
        -------
        None

        Raises
        ------
        ValueError
            when data or key is not octals
        TypeError
            when data or key is not list or string
            when the length of data or key is not correct
        """
        if(len(data) != self.block_len):
            raise TypeError('Data is not of correct size.')

        if(len(key) != self.block_len):
            raise TypeError('Key is not of correct size.')

        if(not self.__octals(data)):
            raise TypeError('Data is not a list or not only octals.')

        if(not self.__octals(key)):
            raise TypeError('Key is not a list, string or not only octals.')

    def encrypt(self, data, key):
        """
        Encrypt data using the key.

        Parameters
        ----------
        data : list or string (octals)
            list or string of octals to encrypt
        key : list or string (octals)
            list or string of octals for a key

        Returns
        -------
        List of encrypted octals

        Raises
        ------
        ValueError
            when data or key is not octals
        TypeError
            when data or key is not list or string
            when the length of data or key is not correct
        """
        try:
            self.__check_input(data, key)
        except Exception as e:
            raise e

        if(type(data) == str):
            data = [int(i) for i in data]

        if(type(key) == str):
            key = [int(i) for i in key]

        self.xor_data_key(data, key)

        for _ in range(self.rounds):
            self.preform_data_substitution(data, True)
            data = self.p_box_multiplication(data, True)
            self.new_key_round(key, True)
            self.xor_data_key(data, key)

        return data

    def decrypt(self, data, key):
        """
        Decrypt data using the key.

        Parameters
        ----------
        data : list or string (octals)
            list or string of octals to decrypt
        key : list or string (octals)
            list or string of octals for a key

        Returns
        -------
        list
            Decrypted octals

        Raises
        ------
        ValueError
            when data or key is not octals
        TypeError
            when data or key is not list or string
            when the length of data or key is not correct
        """
        try:
            self.__check_input(data, key)
        except Exception as e:
            raise e

        if(type(data) == str):
            data = [int(i) for i in data]

        if(type(key) == str):
            key = [int(i) for i in key]

        for _ in range(self.rounds):
            self.new_key_round(key, True)

        self.xor_data_key(data, key)

        for _ in range(self.rounds):
            data = self.p_box_multiplication(data, False)
            self.preform_data_substitution(data, False)
            self.new_key_round(key, False)
            self.xor_data_key(data, key)

        return data
