#!/usr/bin/env python3

"""Preform hidden sum attack."""

from .Matrix import Matrix

import copy


class HiddenSum:
    """
    A class to preform hidden sum attack.

    ...

    Attributes
    ----------
    None

    Methods
    -------
    lambda_six(x):
        lambda for 6-bits
    lambdaInv_six(l):
        inverse lambda for 6-bits
    vprime_six(v):
        vprime for 6-bits
    vprimeInv_six(v):
        inverse vprime for 6-bits
    attack(t, c):
        attack cipher c using the toy cipher t
    """

    def lambda_six(self, x):
        """
        Calculate the lambda for 6-bits.

        Parameters
        ----------
        x : list of int
            binary list

        Returns
        -------
        list of int
        """
        l = []
        l.append(x[0])
        l.append((x[0]&x[2])^x[1])
        l.append(x[2])
        return l

    def lambdaInv_six(self, l):
        """
        Calculate the inverse lambda for 6-bits.

        Parameters
        ----------
        x : list of int
            binary list

        Returns
        -------
        list of int
        """
        x = []
        x.append(l[0])
        x.append(l[1]^(l[0]&l[2]))
        x.append(l[2])
        return x

    def vprime_six(self, v):
        """
        Calculate the VPrime for 6-bits.

        Parameters
        ----------
        x : list of int
            binary list

        Returns
        -------
        list of int
        """
        a = self.lambda_six(v[:3])
        b = self.lambda_six(v[3:])
        return a+b

    def vprimeInv_six(self, v):
        """
        Calculate the inverse VPrime for 6-bits.

        Parameters
        ----------
        x : list of int
            binary list

        Returns
        -------
        list of int
        """
        a = self.lambdaInv_six(v[:3])
        b = self.lambdaInv_six(v[3:])
        return a+b

    def attack(self, t, c):
        """
        Attack the cipher c using the ToyCipher t.

        Parameters
        ----------
        t : class ToyCipher
            the class ToyCipher used to encrypt c
        c : list of int
            list of binary ints

        Returns
        -------
        list of int
            c decrypted
        """
        zero = [0 for i in range(6)]
        zeroc = t.encrypt(zero, "000000")

        mat = Matrix()
        I = mat.get_identity(6)

        Caz = [t.encrypt(i, "000000") for i in I]

        lCaz = [self.vprime_six(i) for i in Caz]
        lzeroc = self.vprime_six(zeroc)

        lCaz2 = [ [ (lCaz[i][j]^lzeroc[j]) for j in range(6) ] for i in range(6) ]
        lCaz2Inv = mat.calculate_inverse(lCaz2)

        if(lCaz2Inv == []):
            return []

        cc = self.vprime_six(c)

        mm = mat.matrix_mul_row_column([cc[i]^lzeroc[i] for i in range(6)], lCaz2Inv)

        return self.vprimeInv_six(mm)
