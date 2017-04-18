#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 14:55:45
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-18 20:45:07
# ----------------------------------------

import numpy as np
import core


class ShearLagElement(object):
    """1-D Shear Lag Beam Element.

    This Class is used to caculate the element stiffness
    of 1-D beam element considering shear lag effect. The
    element stiffness is derived from finite segment method
    proposed by 张元海, 李乔. 考虑剪滞变形时箱形梁广义力矩
    的数值分析[J]. 工程力学, 2010, 27(04): 30-36.
    """

    def __init__(self, node, element, mat, sec, cons):
        """Inits ShearLagElement with database.

        Args:
            db (float): data info for ShearLagElement
        """
        super().__init__()
        self.node = node
        self.element = element
        self.mat = mat
        self.sec = sec

        self.nq = node.shape[0]
        self.nme = element.shape[0]
        q1 = node[element[:, 0] - 1]
        q2 = node[element[:, 1] - 1]
        self.L = np.sqrt(np.sum((q2 - q1)**2, axis=1))

        # self.DOF = core.getDOF(cons, self.nq)
        # DOFi = self.DOF[element[:, 0] - 1]
        # DOFj = self.DOF[element[:, 1] - 1]
        # self.LOC = np.concatenate((DOFi, DOFj), axis=1)

    def stiffness(self):
        """Computes all the element stiffness value

        Returns:
            Ouput (float array): a one dimensional array, (1,36×nme)
        """
        E = self.mat.E
        G = self.mat.G

        A = self.sec.A
        I = self.sec.I
        Aw = self.sec.Aw
        Sw = self.sec.Sw
        Iw = self.sec.Iw
        Iww = self.sec.Iww

        L = self.L

        Ke = np.zeros((self.nme, 8, 8))

        Ke[:, 0, 0] = Ke[:, 4, 4] = E * A / L
        Ke[:, 0, 4] = Ke[:, 4, 0] = -E * A / L
        Ke[:, 3, 0] = Ke[:, 0, 3] = Ke[:, 4, 7] = Ke[:, 7, 4] = E * Sw / L
        Ke[:, 7, 0] = Ke[:, 0, 7] = Ke[:, 4, 3] = Ke[:, 3, 4] = -E * Sw / L
        Ke[:, 1, 1] = Ke[:, 5, 5] = 12 * E * I / L**3
        Ke[:, 5, 1] = Ke[:, 1, 5] = -12 * E * I / L**3
        Ke[:, 2, 1] = Ke[:, 1, 2] = Ke[:, 6, 1] = Ke[:, 1, 6] = \
            -6 * E * I / L**2
        Ke[:, 5, 2] = Ke[:, 2, 5] = Ke[:, 6, 5] = Ke[:, 5, 6] = \
            6 * E * I / L**2
        Ke[:, 2, 2] = Ke[:, 6, 6] = 4 * E * I / L
        Ke[:, 6, 2] = Ke[:, 2, 6] = 2 * E * I / L
        Ke[:, 3, 2] = Ke[:, 2, 3] = Ke[:, 7, 6] = Ke[:, 6, 7] = \
            E * Iw / L
        Ke[:, 7, 2] = Ke[:, 2, 7] = Ke[:, 6, 3] = Ke[:, 3, 6] = \
            -E * Iw / L
        Ke[:, 3, 3] = Ke[:, 7, 7] = E * Iww / L + G * Aw * L / 3
        Ke[:, 3, 7] = Ke[:, 7, 3] = -E * Iww / L + G * Aw * L / 6

        self.Ke = Ke

        # epd = np.array(range(self.nme), ndmin=2)
        # epd = epd[[0, 0, 0, 0, 0, 0, 0, 0], :].T

        # Kg = np.transpose(Trans, axes=(0, 2, 1)) @ Ke @ Trans
        # Ig = self.LOC[epd]
        # Jg = np.transpose(Ig, axes=(0, 2, 1))

        # Kg = Kg.reshape((64 * self.nme))
        # Ig = Ig.reshape((64 * self.nme))
        # Jg = Jg.reshape((64 * self.nme))

        # Ig, Jg, Kg = Ig[Ig != 0], Jg[Ig != 0], Kg[Ig != 0]
        # Ig, Jg, Kg = Ig[Jg != 0] - 1, Jg[Jg != 0] - 1, Kg[Jg != 0]

        return Ke  # Kg, Ig, Jg
