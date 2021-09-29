#!/usr/bin/env python3

import random


class Key:
    def __init__(self):
        self.K, self.K_I = self.key_box()
        super().__init__()

    def key_box(self):
        K = {}
        K_I = {}
        random_values = [i for i in range(8)]
        random.shuffle(random_values)
        for i in range(8):
            K[i] = random_values[i]
            K_I[random_values[i]] = i
        return K, K_I

    def xor_data_key(self, data, key):
        for i in range(len(key)):
            data[i] ^= key[i]
        return data

    def new_key_round(self, key, encrypt):
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
