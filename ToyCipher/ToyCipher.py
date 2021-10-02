#!/usr/bin/env python3

"""Create a ToyCipher."""

from Attack.Matrix import Matrix
from .SBox import SBox
from .PBox import PBox
from .Key import Key

from pathlib import Path
import copy


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
            when the length of data or key is not correct
        TypeError
            when data or key is not list or string
            when data or key is not octals
        """
        if(len(data) != self.block_len):
            raise ValueError('Data is not of correct size.')

        if(len(key) != self.block_len):
            raise ValueError('Key is not of correct size.')

        if(not self.__octals(data)):
            raise TypeError('Data is not a list, string or not only octals.')

        if(not self.__octals(key)):
            raise TypeError('Key is not a list, string or not only octals.')

    def save_currect_cipher(self, file_name):
        """
        Save the current cipher to a text file.

        Parameters
        ----------
        file_name : string
            path to where the cipher is to be saved

        Returns
        -------
        None

        Raises
        ------
        None
        """
        create = Path.cwd().joinpath(file_name)
        with open(create, 'a') as f:
            f.write('## P BOX\n')
            for row in self.P:
                for elem in row:
                    f.write('{} '.format(elem))
                f.write('\n')
            f.write('\n')

            f.write('## P_I BOX\n')
            for row in self.P_I:
                for elem in row:
                    f.write('{} '.format(elem))
                f.write('\n')
            f.write('\n')

            f.write('## S BOX\n')
            for key in self.S:
                f.write('{}: {}\n'.format(key, self.S[key]))
            f.write('\n')

            f.write('## S_I BOX\n')
            for key in self.S_I:
                f.write('{}: {}\n'.format(key, self.S_I[key]))
            f.write('\n')

            f.write('## K BOX\n')
            for key in self.K:
                f.write('{}: {}\n'.format(key, self.K[key]))
            f.write('\n')

            f.write('## K_I BOX\n')
            for key in self.K:
                f.write('{}: {}\n'.format(key, self.K_I[key]))
            f.write('\n')

    def encrypt(self, data_t, key_t):
        """
        Encrypt data using the key.

        Parameters
        ----------
        data_t : list or string (octals)
            list or string of octals to encrypt
        key_t : list or string (octals)
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
        data = copy.deepcopy(data_t)
        key = copy.deepcopy(key_t)

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

    def decrypt(self, data_t, key_t):
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
        data = copy.deepcopy(data_t)
        key = copy.deepcopy(key_t)

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
