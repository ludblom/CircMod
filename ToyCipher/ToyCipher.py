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
    __binary(b):
        Make sure a list or string only contain binary
    __check_input(data, key):
        Check that the inputs are correct (data and key)
    __load_p_box(orig_indent, content):
        Load the P box from file
    __load_s_box(orig_indent, content, box):
        Load the S and Key box from file
    save_cipher(file_name):
        Save the current cipher to a file in position file_name
    load_cipher(file_name):
        Load a cipher in the path file_name
    encrypt(data_t, key_t):
        encrypt the data
    decrypt(data_t, key_t):
        decrypt the data
    """

    # TODO: Initiate a parameter to make the cipher 100% attackable (generating attackable S and P boxes).
    def __init__(self, block_len=3, rounds=1, num_of_gamma=1):
        """
        Init default parameters.

        Parameters
        ----------
        block_len : int
            the length of the block
        rounds : int
            how many rounds the cipher has
        """
        self.num_of_gamma = num_of_gamma
        self.block_len = block_len
        self.rounds = rounds
        super().__init__()

    def __binary(self, b):
        """
        Make sure a list or string only is binary.

        Parameters
        ----------
        b : list of int

        Returns
        -------
        bool
            True if between 0 and 1, otherwise False
        """
        if(type(b) != list and type(b) != str):
            return False

        for o in b:
            if int(o) < 0 or int(o) > 1:
                return False
        return True

    def __check_input(self, data, key):
        """
        Make sure input is correct.

        Parameters
        ----------
        data : list or string (binary)
            list or string of binary to encrypt
        key : list or string (binary)
            list or string of binary for a key

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

        if(not self.__binary(data)):
            raise TypeError("Data is not a list, string or not only 0 or 1's.")

        if(not self.__binary(key)):
            raise TypeError("Data is not a list, string or not only 0 or 1's.")

    def __load_p_box(self, orig_indent, content):
        """
        Load the P-box.

        Parameters
        ----------
        orig_indent : int
            how far have we already gone
        content : list of str
            the file with the data

        Returns
        -------
        int
            the length of P

        Raises
        ------
        None
        """
        i = 1

        self.P = []

        try:
            while(content[i+orig_indent] != ''):
                tmp = []
                for b in content[i+orig_indent].split(' '):
                    tmp.append(int(b))
                self.P.append(tmp)
                i += 1
        except:
            pass
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
            S or K that is copied over

        Returns
        -------
        int
            the length of S or K

        Raises
        ------
        None
        """
        i = 1

        if(box == "S"):
            self.S = {}
        else:
            self.K = {}

        try:
            while(content[i+orig_indent] != ''):
                a, b = content[i+orig_indent].split(' ')
                if(box == "S"):
                    self.S[int(a)] = int(b)
                else:
                    self.K[int(a)] = int(b)
                i += 1
        except:
            pass
        if(box == "S"):
            self.S_I = {v: k for k, v in self.S.items()}
        else:
            self.K_I = {v: k for k, v in self.K.items()}

        return i

    def save_cipher(self, file_name, hard=False, only_P=False):
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

            if not only_P:
                f.write('## S BOX\n')
                for key in self.S:
                    f.write('{} {}\n'.format(key, self.S[key]))
                f.write('\n')

                f.write('## K BOX\n')
                for key in self.K:
                    f.write('{} {}\n'.format(key, self.K[key]))
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
                i += self.__load_p_box(i, content)
            elif(content[i] == "## S BOX"):
                i += self.__load_s_box(i, content, 'S')
            elif(content[i] == "## K BOX"):
                i += self.__load_s_box(i, content, 'K')
            else:
                i += 1

        # Load the inverse boxes
        self.P_I = self.calculate_inverse(self.P)

        # Convert the column len to octal representation
        self.block_len = len(self.P)

    def __preform_splitted_substitution(self, data):
        data_splitted = [data[x:x+int(self.block_len/self.num_of_gamma)] for x in range(0, self.block_len, int(self.block_len/self.num_of_gamma))]
        data_tmp = []
        for i in range(self.num_of_gamma):
            data_tmp.append(self.preform_data_substitution(data_splitted[i], True, i))
        return [d for sd in data_tmp for d in sd]

    def encrypt(self, data_t, key_t):
        """
        Encrypt data using the key.

        Parameters
        ----------
        data_t : list or string (binary)
            list or string of binary to encrypt
        key_t : list or string (binary)
            list or string of binary for a key

        Returns
        -------
        List of int

        Raises
        ------
        ValueError
            when data or key is not binary
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

        data = self.xor_data_key(data, key)

        for _ in range(self.rounds):
            data = self.__preform_splitted_substitution(data)
            data = self.p_box_multiplication(data, True)
            key = self.new_key_round(key, True)
            data = self.xor_data_key(data, key)

        return data

    def decrypt(self, data_t, key_t):
        """
        Decrypt data using the key.

        Parameters
        ----------
        data : list or string (binary)
            list or string of binary to decrypt
        key : list or string (binary)
            list or string of binary for a key

        Returns
        -------
        list of int

        Raises
        ------
        ValueError
            when data or key is not binary
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
            key = self.new_key_round(key, True)

        data = self.xor_data_key(data, key)

        for _ in range(self.rounds):
            data = self.p_box_multiplication(data, False)
            data = self.__preform_splitted_substitution(data)
            key = self.new_key_round(key, False)
            data = self.xor_data_key(data, key)

        return data
