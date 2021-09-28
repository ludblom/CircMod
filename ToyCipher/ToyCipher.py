#!/usr/bin/env python3

from .SBox import SBox
from .PBox import PBox


class ToyCipher(SBox, PBox):
    def __init__(self, N=3, key_size=32):
        self.N = N
        self.P, self.P_I = self.permutation_box(N)
        self.S, self.S_I = self.substitution_box(N)
        super().__init__()

    def string_to_binary(self, string):
        return str(''.join(format(i, '07b') for i in bytearray(string, encoding = 'utf-8')))

    def binary_to_string(self, binary):
        string = ' '
        for i in range(0, len(binary), 7):
            tmp = binary[i:i + 7]
            string += chr(int(tmp, 2))
        return string[1:]

    def encrypt(self, data, key, armor=False):
        # 16
        pass
