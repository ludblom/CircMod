#!/usr/bin/env python3

import random


class SBox:
    def __init__(self):
        self.S, self.S_I = self.substitution_box(self.key_len)
        super().__init__()

    def substitution_box(self, key_len):
        S = {}
        S_I = {}
        random_values = [int(oct(i)[2:]) for i in range(2**key_len)]
        sorted_values = [int(oct(i)[2:]) for i in range(2**key_len)]
        random.shuffle(random_values)
        for i in range(len(sorted_values)):
            S[sorted_values[i]] = random_values[i]
            S_I[random_values[i]] = sorted_values[i]
        return S, S_I

    def preform_data_substitution(self, data, encrypt):
        for i in range(0, self.msg_len, 2):
            exchange = data[i]*10 + data[i+1]

            if(encrypt):
                exchange = self.S[exchange]
            else:
                exchange = self.S_I[exchange]

            data[i] = int(exchange/10)
            data[i+1] = exchange%10
        return data
