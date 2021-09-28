#!/usr/bin/env python3

import random


class Key:
    def key(self):
        K = {}
        K_I = {}
        random_values = [i for i in range(8)]
        random.shuffle(random_values)
        for i in range(8):
            K[i] = random_values[i]
            K_I[random_values[i]] = i
        return K, K_I
