#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 14:55:59
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-18 20:39:39
# ----------------------------------------

import numpy as np


def getDOF(cons, nq):
    """Convert constraint to degree of freedom

    Args:
        cons (int list): constraint, (nq,qDOF)
        nq (TYPE): Description

    Returns:
        Ouput (int array): degree of freedom, (nq,qDOF)
    """
    count = 0
    DOF = np.ones((nq, 4), dtype=int)
    DOF[cons[:, 0] - 1] = cons[:, 1:]
    for i in range(0, nq):
        for j in range(0, 4):
            if DOF[i, j] != 0:
                count = count + 1
                DOF[i, j] = count
    return DOF
