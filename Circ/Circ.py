#!/usr/bin/env python3

from .Matrix import Matrix

class Circ(Matrix):
    def __init__(self, N, k):
        self.Bo = Matrix(gen_Bo=1, N=N, k=k)
        super().__init__()

    def print_Bo(self):
        print(self.Bo)
