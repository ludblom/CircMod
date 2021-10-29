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
    tilde(x):
        tile convert
    tildeInv(l):
        inverse tile convert
    create_M(t):
        create the M matrix from ToyCipher class t
    """

    def tilde(self, x):
        """
        Calculate the tilde of x.

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

    def tildeInv(self, l):
        """
        Calculate the inverse tilde of l.

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

    def create_M(self, t):
        """
        Create the M used to traverse inbetween ciphertext and message.

        Parameters
        ----------
        t : Class ToyCipher
            the already created ToyCipher class

        Returns
        -------
        tuple
            M : the M matrix
            zero : the zero matrix used to mul with the cipher
        """
        zero = [0 for i in range(3)]
        zero = t.encrypt(zero, "000")
        zero = self.lambd(zero)

        I = t.get_identity(3)
        M = []
        for e in I:
            v = t.encrypt(e, "000")
            v_tile = self.lambd(v)
            M.append(t.xor(v_tile, zero))

        return M, zero
