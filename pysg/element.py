#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 14:55:45
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-22 23:43:09
# ----------------------------------------

import numpy as np
import pandas as pd


class ShearLag(object):
    """1-D Shear Lag Beam Element.

    This Class is used to caculate the element stiffness
    of 1-D beam element considering shear lag effect. The
    element stiffness is derived from finite segment method
    proposed.
    """

    def __init__(self, mat, sec, nod_tab, ele_tab):
        """Inits ShearLagElement with database.

        Args:
            db (float): data info for ShearLagElement
        """
        super().__init__()
        self.mat = mat
        self.sec = sec
        self.nod_tab = nod_tab
        self.ele_tab = ele_tab

        q1 = nod_tab[ele_tab[[0]]]
        q2 = nod_tab[ele_tab[[1]]]
        self.L = np.sqrt(np.sum((q2.values - q1.values)**2, axis=1))
        delta = q2.values - q1.values
        self.C = delta[:, 0] / self.L
        self.S = -delta[:, 2] / self.L

    @property
    def trans(self):

        trans = np.zeros((self.ele_tab.shape[0], 8, 8))
        trans[:, 0, 0] = trans[:, 1, 1] = trans[:, 4, 4] = trans[:, 5, 5] = (
            self.C
        )
        trans[:, 2, 2] = trans[:, 3, 3] = trans[:, 6, 6] = trans[:, 7, 7] = 1
        trans[:, 1, 0] = trans[:, 5, 4] = self.S
        trans[:, 0, 1] = trans[:, 4, 5] = -self.S

        return trans

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

        Ke = np.zeros((self.ele_tab.shape[0], 8, 8))
        Ke[:, 0, 0] = Ke[:, 4, 4] = E * A / L
        Ke[:, 0, 4] = Ke[:, 4, 0] = -E * A / L
        Ke[:, 3, 0] = Ke[:, 0, 3] = Ke[:, 4, 7] = Ke[:, 7, 4] = E * Sw / L
        Ke[:, 7, 0] = Ke[:, 0, 7] = Ke[:, 4, 3] = Ke[:, 3, 4] = -E * Sw / L
        Ke[:, 1, 1] = Ke[:, 5, 5] = 12 * E * I / L**3
        Ke[:, 5, 1] = Ke[:, 1, 5] = -12 * E * I / L**3
        Ke[:, 2, 1] = Ke[:, 1, 2] = Ke[:, 6, 1] = Ke[:, 1, 6] = (
            -6 * E * I / L**2
        )
        Ke[:, 5, 2] = Ke[:, 2, 5] = Ke[:, 6, 5] = Ke[:, 5, 6] = (
            6 * E * I / L**2
        )
        Ke[:, 2, 2] = Ke[:, 6, 6] = 4 * E * I / L
        Ke[:, 6, 2] = Ke[:, 2, 6] = 2 * E * I / L
        Ke[:, 3, 2] = Ke[:, 2, 3] = Ke[:, 7, 6] = Ke[:, 6, 7] = (
            E * Iw / L
        )
        Ke[:, 7, 2] = Ke[:, 2, 7] = Ke[:, 6, 3] = Ke[:, 3, 6] = (
            -E * Iw / L
        )
        Ke[:, 3, 3] = Ke[:, 7, 7] = E * Iww / L + G * Aw * L / 3
        Ke[:, 3, 7] = Ke[:, 7, 3] = -E * Iww / L + G * Aw * L / 6
        self.Ke = Ke

        return self.Ke

    def setLoad(self, load):
        """load: a number vector indicates a nodal load.

        Args:
            load (TYPE): Description
        """
        self.load = load.loc[self.ele_tab.index]

    @property
    def equLoad(self):

        L = self.L
        load = self.load
        qu0 = load.iloc[:, 0]
        qu = (load.iloc[:, 1] - load.iloc[:, 0]) / L
        qv0 = load.iloc[:, 2]
        qv = (load.iloc[:, 3] - load.iloc[:, 2]) / L

        equLoad = np.zeros((self.ele_tab.shape[0], 8, 1))
        equLoad[:, 0, 0] = qu * L**2 / 6 + qu0 * L / 2
        equLoad[:, 1, 0] = 3 * qv * L**2 / 20 + qv0 * L / 2
        equLoad[:, 2, 0] = -qv * L**3 / 30 - qv0 * L**2 / 12
        equLoad[:, 4, 0] = qu * L**2 / 3 + qu0 * L / 2
        equLoad[:, 5, 0] = 7 * qv * L**2 / 20 + qv0 * L / 2
        equLoad[:, 6, 0] = qv * L**3 / 20 + qv0 * L**2 / 12

        return equLoad
