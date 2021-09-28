#!/usr/bin/env python3

from .SBox import SBox
from .PBox import PBox
from .Key import Key


class ToyCipher(SBox, PBox, Key):
    def __init__(self, key_len=6):
        self.key_len = key_len
        self.P, self.P_I = self.permutation_box(key_len)
        self.S, self.S_I = self.substitution_box(key_len)
        self.K, self.K_I = self.key()
        super().__init__()

    def encrypt(self, data, key, armor=False):
        # 16
        pass
