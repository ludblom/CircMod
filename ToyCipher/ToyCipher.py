#!/usr/bin/env python3

"""Create a ToyCipher."""

from Attack.Matrix import Matrix
from .SBox import SBox
from .PBox import PBox
from .Key import Key

from pathlib import Path
import copy
import os


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
    __load_p_box(orig_indent, content, box):
        Load the P box from file
    __load_s_box(orig_indent, content, box):
        Load the S and Key box from file
    save_currect_cipher(file_name):
        Save the current cipher to a file in position file_name
    load_cipher(file_name):
        Load a cipher in the path file_name
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

    def __load_p_box(self, orig_indent, content, box):
        """
        Load the P-box.

        Parameters
        ----------
        orig_indent : int
            how far have we already gone
        content : list of str
            the file with the data
        box : str
            P or P_I that is copied over

        Returns
        -------
        int
            the length of P or P_I

        Raises
        ------
        None
        """
        i = 1

        if(box == 'P'):
            self.P = []
        else:
            self.P_I = []

        while(content[i+orig_indent] != ''):
            tmp = []
            for b in content[i+orig_indent].split(' '):
                tmp.append(int(b))
            if(box == 'P'):
                self.P.append(tmp)
            else:
                self.P_I.append(tmp)
            i += 1
        return i

    def __load_s_box(self, orig_indent, content, box):
        """
        Load the S-box or Key box.

        Parameters
        ----------
        orig_indent : int
            how far have we already gone
        content : list of str
            the file with the data
        box : str
            S, S_I, K or K_I that is copied over

        Returns
        -------
        int
            the length of S, S_I, K or K_I

        Raises
        ------
        None
        """
        i = 1

        if(box == "S"):
            self.S = {}
        elif(box == "S_I"):
            self.S_I = {}
        elif(box == "K"):
            self.K = {}
        else:
            self.K_I = {}

        while(content[i+orig_indent] != ''):
            a, b = content[i+orig_indent].split(' ')
            if(box == "S"):
                self.S[int(a)] = int(b)
            elif(box == "S_I"):
                self.S_I[int(a)] = int(b)
            elif(box == "K"):
                self.K[int(a)] = int(b)
            else:
                self.K_I[int(a)] = int(b)
            i += 1
        return i

    def save_currect_cipher(self, file_name, hard=False):
        """
        Save the current cipher to a text file.

        Parameters
        ----------
        file_name : string
            path to where the cipher is to be saved
        hard : bool
            overwrite a file with the same name

        Returns
        -------
        None

        Raises
        ------
        OSError
            when the file exist and hard flag is not set to True
        """
        create = Path.cwd().joinpath(file_name)

        if(create.is_file() and hard):
            os.remove(create)
        elif(create.is_file()):
            raise OSError("File exist: {}".format(create))

        with open(create, 'a') as f:
            f.write('## P BOX\n')
            for row in self.P:
                f.write(' '.join([str(i) for i in row]))
                f.write('\n')
            f.write('\n')

            f.write('## P_I BOX\n')
            for row in self.P_I:
                f.write(' '.join([str(i) for i in row]))
                f.write('\n')
            f.write('\n')

            f.write('## S BOX\n')
            for key in self.S:
                f.write('{} {}\n'.format(key, self.S[key]))
            f.write('\n')

            f.write('## S_I BOX\n')
            for key in self.S_I:
                f.write('{} {}\n'.format(key, self.S_I[key]))
            f.write('\n')

            f.write('## K BOX\n')
            for key in self.K:
                f.write('{} {}\n'.format(key, self.K[key]))
            f.write('\n')

            f.write('## K_I BOX\n')
            for key in self.K_I:
                f.write('{} {}\n'.format(key, self.K_I[key]))
            f.write('\n')

    def load_cipher(self, file_name):
        """
        Load a cipher in the path file_name.

        Parameters
        ----------
        file_name : string
            full path to the file

        Returns
        -------
        None

        Raises
        ------
        FileNotFoundError
            the file file_name do not exist
        """
        file_name = Path(file_name)

        if not file_name.is_file():
            raise FileNotFoundError('File {} do not exist.'.format(file_name))

        with open(file_name, 'r') as f:
            content = f.read().splitlines()

        # Exchange data in the boxes
        i = 0
        while(i < len(content)):
            if(content[i] == "## P BOX"):
                i += self.__load_p_box(i, content, 'P')
            elif(content[i] == "## P_I BOX"):
                i += self.__load_p_box(i, content, 'P_I')
            elif(content[i] == "## S BOX"):
                i += self.__load_s_box(i, content, 'S')
            elif(content[i] == "## S_I BOX"):
                i += self.__load_s_box(i, content, 'S_I')
            elif(content[i] == "## K BOX"):
                i += self.__load_s_box(i, content, 'K')
            elif(content[i] == "## K_I BOX"):
                i += self.__load_s_box(i, content, 'K_I')
            else:
                i += 1

        # Convert the column len to octal representation
        self.block_len = len(self.P)/3

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
