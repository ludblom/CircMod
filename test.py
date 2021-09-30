#!/usr/bin/env python3

"""Tests for the Ring product, ToyCipher."""

import unittest
from Attack.RingOperator import Ring
from ToyCipher.ToyCipher import ToyCipher


class TestRingRules(unittest.TestCase):
    """Testing the ring product."""

    def test_symmetry(self):
        """Test symmetry."""
        test_sizes = [
            (3, 1),
            (5, 2)
        ]

        for N, k in test_sizes:
            c = Ring(N=N, k=k)
            for a in range(2**N):
                for b in range(2**N):
                    self.assertEqual(
                        c.ring(a, b),
                        c.ring(b, a),
                        """
                        ring({},{}) should be equal to ring({},{}), N:{}, k:{}
                        """.format(a, b, b, a, N, k)
                    )

    def test_nondistribution(self):
        """Test non-distribution."""
        test_sizes = [
            (3, 1),
            (5, 2)
        ]

        for N, k in test_sizes:
            hs = Ring(N=N, k=k)
            for a in range(2**N):
                for b in range(2**N):
                    for c in range(2**N):
                        # a o b
                        a_plus_b = hs.binary_to_int(hs.matrix_sum(
                            hs.int_to_binary(a, N), hs.int_to_binary(b, N))
                        )

                        # (a o b) o c
                        a_plus_b_circ_c = hs.ring(a_plus_b, c)

                        # a o c
                        a_ring_c = hs.int_to_binary(hs.ring(a, c), N)

                        # b o c
                        b_ring_c = hs.int_to_binary(hs.ring(b, c), N)

                        # (a o b)+(a o c)
                        a_sum_c = hs.matrix_sum(a_ring_c, b_ring_c)

                        # ((a o b)+(a o c))+c
                        end = hs.binary_to_int(hs.matrix_sum(
                            a_sum_c, hs.int_to_binary(c, N))
                        )

                        # (a o b) o c == ((a o b)+(a o c))+c
                        self.assertEqual(
                            a_plus_b_circ_c,
                            end,
                            """
                            N: {}, k: {}, a: {}, b: {}, c: {}
                            """.format(N, k, a, b, c)
                        )

    def test_matrix_product(self):
        """Test matrix product property."""
        test_sizes = [
            (3, 1),
            (5, 2)
        ]

        for N, k in test_sizes:
            hs = Ring(N=N, k=k)
            for x in range(2**N):
                for a in range(2**N):
                    for b in range(2**N):
                        # a o b
                        a_ring_b = hs.ring(a, b)

                        # x o (a o b)
                        x_ring_ab = hs.ring(x, a_ring_b)

                        # M_{a o b}
                        Mx_a_ring_b = hs.get_Bx(a_ring_b)

                        # x * M_{a o b}
                        xMxM_a_ring_b = hs.matrix_mul(
                                            hs.int_to_binary(x, N),
                                            Mx_a_ring_b
                        )

                        # x * M_{a o b} + a o b
                        end = hs.binary_to_int(
                                hs.matrix_sum(
                                    xMxM_a_ring_b,
                                    hs.int_to_binary(a_ring_b, N)
                                )
                        )

                        # x o (a o b) == x * M_{a o b} + a o b
                        self.assertEqual(
                            x_ring_ab,
                            end,
                            """
                            N: {}, k: {}, x: {}, a: {}, b: {}
                            """.format(N, k, x, a, b)
                        )

    def test_dot_associativity(self):
        """Test associativity."""
        test_sizes = [
            (3, 1),
            (5, 2)
        ]

        for N, k in test_sizes:
            hs = Ring(N=N, k=k)
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
                            """
                            N: {}, k: {}, a: {}, b: {}, c: {}
                            """.format(N, k, a, b, c)
                        )

    def test_dot_distributive(self):
        """Test the distributive law."""
        test_sizes = [
            (3, 1),
            (5, 2)
        ]

        for N, k in test_sizes:
            hs = Ring(N=N, k=k)
            for a in range(2**N):
                for b in range(2**N):
                    for c in range(2**N):
                        # a + b
                        a_sum_b = hs.binary_to_int(
                            hs.matrix_sum(hs.int_to_binary(a, N),
                                          hs.int_to_binary(b, N)
                                          )
                        )

                        # (a+b).c
                        a_sum_b_dot_c = hs.dot(a_sum_b, c)

                        # a.c
                        a_dot_c = hs.dot(a, c)

                        # b.c
                        b_dot_c = hs.dot(b, c)

                        # a.c + b.c
                        a_dot_c_sum_b_dot_c = hs.binary_to_int(
                            hs.matrix_sum(hs.int_to_binary(a_dot_c, N),
                                          hs.int_to_binary(b_dot_c, N)
                                          )
                        )

                        # (a+b).c == a.c + b.c
                        self.assertEqual(
                            a_sum_b_dot_c,
                            a_dot_c_sum_b_dot_c,
                            "N: {}, k: {}, a: {}, b: {}, c: {}".format(N, k,
                                                                       a, b, c)
                        )


# class TestToyCipher(unittest.TestCase):
#     """Testing the ToyCipher."""

#     def test_enc_dec(self):
#         """Test if encrypting and decrypting a string is equal."""
#         c = ToyCipher()
#         for i in range(100):
#             msg = []
#             c.encrypt(msg, msg)


if __name__ == '__main__':
    unittest.main()
