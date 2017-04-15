#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
import core


class ShearLagElem(object):
    """Shear lag segment element

    Attributes:
        A (float): area of cross section
        bDe (TYPE): Description
        bFe (TYPE): Description
        C (TYPE): Description
        DOF (TYPE): Description
        E (float): elasticity modulus
        G (float): shear elasticity
        I (float): inertia moment of cross section
        Iw (float): inertia moment of top slab
        Ke (TYPE): Description
        L (TYPE): Description
        LOC (TYPE): Description
        me (TYPE): Description
        nme (TYPE): Description
        nq (TYPE): Description
        q (TYPE): Description
        S (TYPE): Description
        Sw (TYPE): Description
        Trans (TYPE): Description
    """

    def __init__(self, q, me, E, G, A, I, Sw, Iw, cons):

        super().__init__()
        self.q = q
        self.me = me
        self.E = E
        self.G = G
        self.A = A
        self.I = I
        self.Sw = Sw
        self.Iw = Iw

        nq = q.shape[0]
        nme = me.shape[0]
        q1 = q[me[:, 0] - 1]
        q2 = q[me[:, 1] - 1]
        L = np.sqrt(np.sum((q2 - q1)**2, axis=1))
        C = (q2 - q1)[:, 0] / L
        S = -(q2 - q1)[:, 1] / L

        self.nq = nq
        self.nme = nme
        self.L = L
        self.C = C
        self.S = S

        DOF = core.getDOF(cons, nq)
        DOFi = DOF[me[:, 0] - 1]
        DOFj = DOF[me[:, 1] - 1]
        LOC = np.concatenate((DOFi, DOFj), axis=1)

        self.DOF = DOF
        self.LOC = LOC

    def stiffness(self):
        """Computes all the element stiffness value

        Returns:
            Ouput (float array): a one dimensional array, (1,36×nme)
        """
        q = self.q
        me = self.me
        A = self.A
        E = self.E
        G = self.G
        I = self.I
        Iw = self.Iw
        Sw = self.Sw
        L = self.L
        C = self.C
        S = self.S
        nq = self.nq
        nme = self.nme
        DOF = self.DOF
        LOC = self.LOC

        z0 = Sw / A
        m = 1 - 5 * Sw * z0 / (6 * Iw)
        beta = Iw / I
        n = 1 / (m - 5 * beta / 6)
        k = np.sqrt(5 * G * n / (2 * E * b**2))

        Trans = np.zeros((nme, 8, 8))

        Trans[:, 0, 0] = Trans[:, 1, 1] = Trans[:, 4, 4] = Trans[:, 5, 5] = C
        Trans[:, 2, 2] = Trans[:, 3, 3] = Trans[:, 6, 6] = Trans[:, 7, 7] = 1
        Trans[:, 1, 0] = Trans[:, 5, 4] = S
        Trans[:, 0, 1] = Trans[:, 4, 5] = -S

        self.Trans = Trans

        Ke = np.zeros((nme, 8, 8))

        e1 = 1 + np.exp(k * L)
        e2 = 1 - np.exp(k * L)
        e3 = 1 + np.exp(2 * k * L)
        e4 = 1 - np.exp(2 * k * L)

        r1 = e2 * G * Aw * L**2
        r2 = e1 * G * Aw * k * L**3
        r3 = beta * E * Iw * (2 * e2 + e1 * k * L)
        r4 = e4 * (Sw * zw + 4 * beta * Iw) - e3 * If * k * L
        r5 = e4 * (Sw * zw - 2 * beta * Iw) - 2 * If * k * L * np.exp(k * L)

        a1 = r2 / (12 * r3 + r2)
        a2 = (r2 + 3 * r3) / (12 * r3 + r2)
        a3 = (r2 - 6 * r3) / (12 * r3 + r2)
        a4 = r3 / (12 * r3 + r2)
        a5 = (3 * r1 + 2 * r2 + 6 * r3) / (12 * r3 + r2)
        a6 = (3 * r1 + r2 - 6 * r3) / (12 * r3 + r2)
        a7 = 6 * r3 * (2 * e2 * (Sw * zw + beta * Iw) - e1 * If *
                       k * L) / (Iw * (12 * e2 * r3 + e4 * G * Aw * k * L**6))
        a8 = E * L**2 * (r4 * k * L + 6 * e2**2 * beta * Iw) / \
            (12 * e2 * r3 + e4 * G * Aw * k * L**6)
        a9 = E * L**2 * (r5 * k * L - 6 * e2**2 * beta * Iw) / \
            (12 * e2 * r3 + e4 * G * Aw * k * L**6)

        Ke[:, 0, 0] = Ke[:, 4, 4] = E * A / L
        Ke[:, 0, 4] = Ke[:, 4, 0] = -E * A / L
        Ke[:, 3, 0] = Ke[:, 0, 3] = Ke[:, 4, 7] = Ke[:, 7, 4] = E * Sw / L
        Ke[:, 7, 0] = Ke[:, 0, 7] = Ke[:, 4, 3] = Ke[:, 3, 4] = -E * Sw / L
        Ke[:, 1, 1] = Ke[:, 5, 5] = 12 * E * I * a1 / L**3
        Ke[:, 5, 1] = Ke[:, 1, 5] = -12 * E * I * a1 / L**3
        Ke[:, 2, 1] = Ke[:, 1, 2] = Ke[:, 6, 1] = Ke[:, 1, 6] = \
            -6 * E * I * a1 / L**2
        Ke[:, 5, 2] = Ke[:, 2, 5] = Ke[:, 6, 5] = Ke[:, 5, 6] = \
            6 * E * I * a1 / L**2
        Ke[:, 2, 2] = Ke[:, 6, 6] = 4 * E * I * a2 / L
        Ke[:, 6, 2] = Ke[:, 2, 6] = 2 * E * I * a3 / L
        Ke[:, 7, 1] = Ke[:, 1, 7] = Ke[:, 3, 1] = Ke[:, 1, 3] = \
            -6 * G * Aw * a4 / beta
        Ke[:, 7, 5] = Ke[:, 5, 7] = Ke[:, 5, 3] = Ke[:, 3, 5] = \
            6 * G * Aw * a4 / beta
        Ke[:, 3, 2] = Ke[:, 2, 3] = Ke[:, 7, 6] = Ke[:, 6, 7] = \
            2 * E * Iw * a5 / L
        Ke[:, 7, 2] = Ke[:, 2, 7] = Ke[:, 6, 3] = Ke[:, 3, 6] = \
            2 * E * Iw * a6 / L
        Ke[:, 3, 3] = Ke[:, 7, 7] = E * Iw * a7 / L + G * Aw * a8 / L
        Ke[:, 3, 7] = Ke[:, 7, 3] = -E * Iw * a7 / L - G * Aw * a9 / L

        self.Ke = Ke

        epd = np.array(range(nme), ndmin=2)
        epd = epd[[0, 0, 0, 0, 0, 0, 0, 0], :].T

        Kg = np.transpose(Trans, axes=(0, 2, 1)) @ Ke @ Trans
        Ig = LOC[epd]
        Jg = np.transpose(Ig, axes=(0, 2, 1))

        Kg = Kg.reshape((64 * nme))
        Ig = Ig.reshape((64 * nme))
        Jg = Jg.reshape((64 * nme))

        Ig, Jg, Kg = Ig[Ig != 0], Jg[Ig != 0], Kg[Ig != 0]
        Ig, Jg, Kg = Ig[Jg != 0] - 1, Jg[Jg != 0] - 1, Kg[Jg != 0]

        return Kg, Ig, Jg

    def nodeLoad(self, nLoad):
        """Summary

        Args:
            nLoad (TYPE): Description

        Returns:
            Ouput (TYPE): Description
        """
        DOF = self.DOF

        load1 = np.zeros_like(DOF)
        load1[nLoad[:, 0] - 1] = nLoad[:, 1:]
        load1 = load1[DOF != 0].reshape((-1, 1))

        return load1

    def distrLoad1(self, dLoad):
        """Summary

        Args:
            dLoad (TYPE): Description

        Returns:
            Ouput (TYPE): Description
        """
        LOC = self.LOC
        L = self.L

        load2 = np.zeros_like(LOC)
        L = L.reshape((-1, 1))
        # 等效剪力
        load2[dLoad[:, 0] - 1, 0:2] = 0.5 * dLoad[:, 1:] * L[dLoad[:, 0] - 1]
        load2[dLoad[:, 0] - 1, 4:6] = 0.5 * dLoad[:, 1:] * L[dLoad[:, 0] - 1]
        # 等效弯矩
        load2[dLoad[:, 0] - 1, 2:3] = \
            -1 / 12 * dLoad[:, 2:3] * L[dLoad[:, 0] - 1]**2
        load2[dLoad[:, 0] - 1, 6:7] = \
            1 / 12 * dLoad[:, 2:3] * L[dLoad[:, 0] - 1]**2
        jj = LOC[LOC != 0] - 1
        ii = np.zeros_like(jj)
        load2 = load2[LOC != 0]

        return load2, jj, ii

    def distrLoad(self, q0, qu, qv):
        """Summary

        Args:
            q0 (TYPE): Description
            qu (TYPE): Description
            qv (TYPE): Description

        Returns:
            Ouput (TYPE): Description
        """
        A = self.A
        E = self.E
        G = self.G
        I = self.I
        Iw = self.Iw
        Sw = self.Sw
        L = self.L
        nme = self.nme
        DOF = self.DOF
        LOC = self.LOC
        Trans = self.Trans
        Ke = self.Ke

        z0 = Sw / A
        beta = Iw / I

        bDe = np.zeros((nme, 8, 1))
        bDe[:, 0, 0] = bDe[:, 1, 0] = bDe[:, 2, 0] = 0
        bDe[:, 3, 0] = -q0 * z0 * b**2 / (2 * G * Iw)
        bDe[:, 4, 0] = -L**2 * (3 * q0 + qu * L) / (6 * E * A)
        bDe[:, 5, 0] = qv * L**4 / (24 * E * I)
        bDe[:, 6, 0] = -qv * L**3 / (6 * E * I)
        bDe[:, 7, 0] = -qv * L * b**2 / (2 * G * I) - \
            (q0 + qu * L) * z0 * b**2 / (2 * G * Iw)
        self.bDe = bDe

        bD = np.transpose(Trans, axes=(0, 2, 1)) @ Ke @ bDe

        bFe = np.zeros((nme, 8, 1))
        bFe[:, 0, 0] = Sw * E * b**2 * (qu * z0 + qv * beta) / (3 * G * Iw)
        bFe[:, 1, 0] = 0
        bFe[:, 2, 0] = E * b**2 * (qu * z0 + qv * beta) / (3 * G)
        bFe[:, 3, 0] = 4 * E * b**2 * (qu * z0 + qv * beta) / (15 * G)
        bFe[:, 4, 0] = -Sw * E * b**2 * \
            (qu * z0 + qv * beta) / (3 * G * Iw) - L * (q0 + qu * L / 2)
        bFe[:, 5, 0] = -qv * L
        bFe[:, 6, 0] = -E * b**2 * \
            (qu * z0 + qv * beta) / (3 * G) - qv * L**2 / 2
        bFe[:, 7, 0] = -4 * E * b**2 * (qu * z0 + qv * beta) / (15 * G) - \
            2 * Sw * L * (q0 + qu * L / 2) / (3 * A) - qv * L**2 * beta / 3
        self.bFe = bFe

        bF = np.transpose(Trans, axes=(0, 2, 1)) @ bFe

        Load2 = bD[:, :, 0] - bF[:, :, 0]

        Ig = LOC[LOC != 0] - 1
        Jg = np.zeros_like(Ig)
        Load2 = Load2[LOC != 0]

        return Load2, Ig, Jg
