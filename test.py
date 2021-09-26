#!/usr/bin/env python3

import unittest
from Circ.Matrix import HiddenSum


class TestRingRules(unittest.TestCase):
    def test_symmetry(self):
        test_sizes = [
            (3, 1),
            (5, 2)
        ]

        for N, k in test_sizes:
            c = HiddenSum(N=N,k=k)
            for a in range(2**N):
                for b in range(2**N):
                    self.assertEqual(
                        c.ring(a,b),
                        c.ring(b,a),
                        "ring({},{}) should be equal to ring({},{}), N: {}, k: {}".format(a,b,b,a,N,k)
                    )

    def test_nondistribution(self):
        test_sizes = [
            (3, 1),
            (5, 2)
        ]

        for N, k in test_sizes:
            hs = HiddenSum(N=N,k=k)
            for a in range(2**N):
                for b in range(2**N):
                    for c in range(2**N):
                        a_plus_b = hs.binary_to_int(hs.matrix_sum(hs.int_to_binary(a, N), hs.int_to_binary(b, N)))
                        a_plus_b_circ_c = hs.ring(a_plus_b, c)

                        a_ring_c = hs.int_to_binary(hs.ring(a, c), N)
                        b_ring_c = hs.int_to_binary(hs.ring(b, c), N)
                        a_sum_c = hs.matrix_sum(a_ring_c, b_ring_c)
                        end = hs.binary_to_int(hs.matrix_sum(a_sum_c, hs.int_to_binary(c, N)))

                        self.assertEqual(
                            a_plus_b_circ_c,
                            end,
                            "N: {}, k: {}, a: {}, b: {}, c: {}".format(N, k, a, b, c)
                        )

    def test_matrix_product(self):
        test_sizes = [
            (3, 1),
            (5, 2)
        ]

        for N, k in test_sizes:
            hs = HiddenSum(N=N,k=k)
            for x in range(2**N):
                for a in range(2**N):
                    for b in range(2**N):
                        a_ring_b = hs.ring(a, b)
                        x_ring_ab = hs.ring(x, a_ring_b)

                        Mx_a_ring_b = hs.get_Bx(a_ring_b)
                        xMxM_a_ring_b = hs.matrix_mul(hs.int_to_binary(x, N), Mx_a_ring_b)
                        end = hs.binary_to_int(hs.matrix_sum(xMxM_a_ring_b, hs.int_to_binary(a_ring_b, N)))

                        self.assertEqual(
                            x_ring_ab,
                            end,
                            "N: {}, k: {}, x: {}, a: {}, b: {}".format(N, k, x, a, b)
                        )

    def test_dot_associativity(self):
        test_sizes = [
            (3, 1),
            (5, 2)
        ]

        for N, k in test_sizes:
            hs = HiddenSum(N=N, k=k)
            for a in range(2**N):
                for b in range(2**N):
                    for c in range(2**N):
                        a_dot_b = hs.dot(a, b)
                        ab_dot_c = hs.dot(a_dot_b, c)

                        b_dot_c = hs.dot(b, c)
                        a_dot_bc = hs.dot(a, b_dot_c)

                        self.assertEqual(
                            ab_dot_c,
                            a_dot_bc,
                            "N: {}, k: {}, a: {}, b: {}, c: {}".format(N, k, a, b, c)
                        )

    def test_dot_distributive(self):
        test_sizes = [
            (3, 1),
            (5, 2)
        ]

        for N, k in test_sizes:
            hs = HiddenSum(N=N, k=k)
            for a in range(2**N):
                for b in range(2**N):
                    for c in range(2**N):
                        a_sum_b = hs.binary_to_int(hs.matrix_sum(hs.int_to_binary(a, N), hs.int_to_binary(b, N)))
                        a_sum_b_dot_c = hs.dot(a_sum_b, c)

                        a_dot_c = hs.dot(a, c)
                        b_dot_c = hs.dot(b, c)
                        a_dot_c_sum_b_dot_c = hs.binary_to_int(hs.matrix_sum(hs.int_to_binary(a_dot_c, N), hs.int_to_binary(b_dot_c, N)))

                        self.assertEqual(
                            a_sum_b_dot_c,
                            a_dot_c_sum_b_dot_c,
                            "N: {}, k: {}, a: {}, b: {}, c: {}".format(N, k, a, b, c)
                        )


if __name__ == '__main__':
    unittest.main()
