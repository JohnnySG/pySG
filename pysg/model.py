#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 14:55:45
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-19 22:15:38
# ----------------------------------------

import numpy as np
import scipy.sparse as scsparse
import core


class Model(object):
    """Summary

    Attributes:
        database (TYPE): Description
    """

    def __init__(self, mesh, LOC):
        """Summary

        Args:
            db (TYPE): Description
        """
        super().__init__()
        self.mesh = mesh
        self.LOC = LOC
        self.node = mesh.node
        self.element = mesh.element

    def assemble(self):
        """Assembly of the Stiffness Matrix

        Args:
            Ig (TYPE): Description
            Jg (TYPE): Description
            Kg (TYPE): Description

        Returns:
            Ouput (TYPE): Description
        """
        trans = self.mesh.ele_trans_matrix()
        Ke = self.mesh.stiffness()
        epd = np.array(range(self.element.shape[0]), ndmin=2)
        epd = epd[[0, 0, 0, 0, 0, 0, 0, 0], :].T

        Kg = np.transpose(trans, axes=(0, 2, 1)) @ Ke @ trans
        Ig = self.LOC[epd]
        Jg = np.transpose(Ig, axes=(0, 2, 1))

        Kg = Kg.reshape((64 * self.element.shape[0]))
        Ig = Ig.reshape((64 * self.element.shape[0]))
        Jg = Jg.reshape((64 * self.element.shape[0]))
        Ig, Jg, Kg = Ig[Ig != 0], Jg[Ig != 0], Kg[Ig != 0]
        Ig, Jg, Kg = Ig[Jg != 0] - 1, Jg[Jg != 0] - 1, Kg[Jg != 0]

        self.Kmat = scsparse.csr_matrix((
            Kg, (Ig, Jg)
        ))

        return self.Kmat

    def is_assembled(self):
        if self.Kmat is None:
            return False
        return True

    def load(self, nLoad, eLoad):
        """Summary

        Args:
            nLoad (TYPE): direct nodal load
            eLoad (TYPE): element distributed load

        Returns:
            Ouput (TYPE): Description
        """
        L = self.mesh.L
        LOC = self.LOC
        DOF = core.LOC_to_DOF(self.LOC)
        trans = self.mesh.ele_trans_matrix()

        load = np.zeros_like(DOF)
        load[nLoad.index - 1] = nLoad.values
        load = load[DOF != 0].reshape((-1, 1))

        qu0 = eLoad.iloc[:, 0]
        qu = (eLoad.iloc[:, 1] - eLoad.iloc[:, 0]) / L
        qv0 = eLoad.iloc[:, 2]
        qv = (eLoad.iloc[:, 3] - eLoad.iloc[:, 2]) / L

        dFe = np.zeros((self.element.shape[0], 8, 1))
        dFe[:, 0, 0] = qu * L**2 / 6 + qu0 * L / 2
        dFe[:, 1, 0] = 3 * qv * L**2 / 20 + qv0 * L / 2
        dFe[:, 2, 0] = -qv * L**3 / 30 - qv0 * L**2 / 12
        dFe[:, 4, 0] = qu * L**2 / 3 + qu0 * L / 2
        dFe[:, 5, 0] = 7 * qv * L**2 / 20 + qv0 * L / 2
        dFe[:, 6, 0] = qv * L**3 / 20 + qv0 * L**2 / 12
        self.dFe = dFe

        DF = np.transpose(trans, axes=(0, 2, 1)) @ dFe
        DF = DF[:, :, 0]
        Ig = LOC[LOC != 0] - 1
        Jg = np.zeros_like(Ig)
        DF = DF[LOC != 0]
        DF = scsparse.csr_matrix((
            DF, (Ig, Jg)
        ))

        load += DF

        return load


if __name__ == '__main__':
    pass
