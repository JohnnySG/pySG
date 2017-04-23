#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 18:04:11
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-22 23:35:26
# ----------------------------------------

import numpy as np
import pandas as pd


class DegreeFreedom(object):
    """Summary

    Attributes:
        SID (TYPE): Description
    """

    def __init__(self, nod_tab, num_dof):
        """Summary

        Args:
            nod_tab (TYPE): Description
            num_dof (TYPE): Description
        """
        super().__init__()
        nq = nod_tab.shape[0]
        row = nod_tab.index
        col = ['U{}'.format(i) for i in range(1, num_dof + 1)]

        self.num_dof = num_dof
        self.SID = pd.DataFrame([
            [x + num_dof * y for x in range(1, num_dof + 1)]
            for y in range(nq)
        ], index=row, columns=col)

    def nodDOF(self, nod):
        """Summary

        Args:
            nod (TYPE): Description

        Returns:
            Ouput (TYPE): Description
        """
        nod_dof = self.SID.loc[nod.ID]

        return nod_dof

    def eleDOF(self, ele):
        """Summary

        Args:
            ele (TYPE): Description

        Returns:
            Ouput (TYPE): Description
        """
        DOFi = self.SID.loc[ele[[0]]]
        DOFj = self.SID.loc[ele[[1]]]
        val = np.concatenate((DOFi, DOFj), axis=1)
        coli = ['U{}i'.format(i) for i in range(1, self.num_dof + 1)]
        colj = ['U{}j'.format(i) for i in range(1, self.num_dof + 1)]
        col = coli + colj
        ele_dof = pd.DataFrame(val, index=ele.index, columns=col)

        return ele_dof


if __name__ == '__main__':

    xlsx = pd.ExcelFile('Data.xlsx')
    nod_tab = xlsx.parse('Node', index_col=0)
    DOF = DegreeFreedom(nod_tab, 5)
    print(DOF.SID)
    print(DOF.SID[[1]])
