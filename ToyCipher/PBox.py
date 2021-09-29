#!/usr/bin/env python3

import copy, random


class PBox:
    def __init__(self):
        self.P, self.P_I = self.permutation_box(self.key_len)
        super().__init__()

    def permutation_box(self, num_of_octals):
        P_I = []
        while P_I == []:
            P_tmp = []
            for _ in range(num_of_octals*3):
                tmp = []
                for _ in range(num_of_octals*3):
                    rand = random.randint(0, 1)
                    tmp.append(rand)
                P_tmp.append(tmp)
            P = copy.deepcopy(P_tmp)
            P_I = self.calculate_inverse(P_tmp)
        return P, P_I

    def convert_oct_to_binary(self, data):
        bin_data = []
        # Convert to string binary of size 3 (octal)
        bin_tmp = [format(i, '03b') for i in data]
        # Convert the strings to int
        for bin_part in bin_tmp:
            for b in bin_part:
                bin_data.append(int(b))
        return bin_data

    def convert_binary_to_oct(self, data):
        oct_data = []
        for i in range(0, len(data), 3):
            tmp = [str(j) for j in data[i:i+3]]
            oct_data.append(int('0b{}'.format(''.join(tmp)), 2))
        return oct_data

    def p_box_multiplication(self, data, encrypt):
        bin_data = self.convert_oct_to_binary(data)
        if encrypt:
            res_data = self.mul_row_column(bin_data, self.P)
        else:
            res_data = self.mul_row_column(bin_data, self.P_I)
        return self.convert_binary_to_oct(res_data)
