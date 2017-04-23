#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 14:55:45
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-21 22:29:51
# ----------------------------------------

import numpy as np
import scipy.sparse as scsparse
from . import core


class Model(object):
    """Summary

    Attributes:
        database (TYPE): Description
    """

    def __init__(self, mesh):
        """Summary

        Args:
            db (TYPE): Description
        """
        super().__init__()
        self.mesh = mesh
        self.assemble()

    def assemble(self):
        """Assembly of the Stiffness Matrix

        Args:
            Ig (TYPE): Description
            Jg (TYPE): Description
            Kg (TYPE): Description

        Returns:
            Ouput (TYPE): Description
        """
        trans = self.mesh.trans
        Ke = self.mesh.stiffness()
        Kg = np.transpose(trans, axes=(0, 2, 1)) @ Ke @ trans

        LOC = self.mesh.LOC.values - 1
        Ig, Jg = core.meshgrid(LOC, LOC)

        Kg = Kg.reshape(-1)
        Ig = Ig.reshape(-1)
        Jg = Jg.reshape(-1)

        self.Kmat = scsparse.csr_matrix((
            Kg, (Ig, Jg)
        ))

        return self.Kmat

    def is_assembled(self):
        if self.Kmat is None:
            return False
        return True

    def formLoadVec(self):
        """Summary

        Returns:
            Ouput (TYPE): Description
        """
        LOC = self.mesh.LOC.values
        equLoad = self.mesh.equLoad
        DOF = core.LOC_to_DOF(LOC)
        trans = self.mesh.trans

        NF = self.mesh.node.load
        load = np.zeros_like(DOF)
        load[NF.index - 1] = NF.values
        load = load.reshape(-1, 1)

        DF = np.transpose(trans, axes=(0, 2, 1)) @ equLoad
        DF = DF.reshape(-1)
        Ig = (LOC - 1).reshape(-1)
        Jg = np.zeros_like(Ig)
        DF = scsparse.csr_matrix((
            DF, (Ig, Jg)
        ))
        self.load = load + DF

    def setBoundary(self):

        inf = np.finfo('f').max
        res = self.mesh.node.restraints
        valRes = (res.values[res.notnull()] * inf).reshape(-1, 1)
        numDOF = self.mesh.node.DOF.loc[res.index].values[res.notnull()]

        self.Kmat[numDOF - 1, numDOF - 1] = inf
        self.load[numDOF - 1] = valRes


if __name__ == '__main__':

    pass
