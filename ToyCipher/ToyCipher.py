#!/usr/bin/env python3

from Circ.Matrix import Matrix
from .SBox import SBox
from .PBox import PBox
from .Key import Key


class ToyCipher(Matrix, SBox, PBox, Key):
    def __init__(self, block_len=6, rounds=3):
        self.block_len = block_len
        self.rounds = rounds
        super().__init__()

    def encrypt(self, data, key):
        if(
            len(key) != self.block_len or
            len(data) != self.block_len
          ):
            print("Error: Key or data size not correct.")
            return 0

        self.xor_data_key(data, key)

        for _ in range(self.rounds):
            self.preform_data_substitution(data, True)
            data = self.p_box_multiplication(data, True)
            self.new_key_round(key, True)
            self.xor_data_key(data, key)

        return data

    def decrypt(self, data, key):
        if(
            len(key) != self.block_len or
            len(data) != self.block_len
          ):
            print("Error: Key or data size not correct.")
            return 0

        for _ in range(self.rounds):
            self.new_key_round(key, True)

        self.xor_data_key(data, key)

        for _ in range(self.rounds):
            data = self.p_box_multiplication(data, False)
            self.preform_data_substitution(data, False)
            self.new_key_round(key, False)
            self.xor_data_key(data, key)

        return data
