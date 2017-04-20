#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 14:55:59
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-19 20:14:15
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
    DOF[cons.index - 1] = cons.values
    for i in range(0, nq):
        for j in range(0, 4):
            if DOF[i, j] != 0:
                count = count + 1
                DOF[i, j] = count
    return DOF


def getLOC(DOF, element):
    """单元定位向量

    Args:
        DOF (TYPE): 节点自由度矩阵
        element (TYPE): 单元连通性矩阵

    Returns:
        Ouput (TYPE): 单元定位向量
    """
    DOFi = DOF[element.iloc[:, 0] - 1]
    DOFj = DOF[element.iloc[:, 1] - 1]
    LOC = np.concatenate((DOFi, DOFj), axis=1)
    return LOC


def LOC_to_DOF(LOC):
    """单元的自由度

    Args:
        DOF (TYPE): 节点自由度矩阵
        element (TYPE): 单元连通性矩阵

    Returns:
        Ouput (TYPE): 单元定位向量
    """
    DOF = np.zeros((LOC.shape[0] + 1, 4), dtype=int)
    DOF[:-2] = LOC[:-1, 0:4]
    DOF[-2:] = LOC[-1].reshape((2, -1))

    return DOF
