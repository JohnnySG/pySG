#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 14:55:59
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-22 02:58:10
# ----------------------------------------

import numpy as np


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


def element_to_node(ele_tab, nod_tab):
    # ele_tab
    #         \
    #             nod_tab
    #                     \
    #                         DOF_tab

    pass


def node_to_element(nod_tab, ele_tab):
    pass


def node_to_DOF(nod_tab, ele_tab):
    pass


def DOF_to_node(nod_tab, ele_tab):
    pass


def meshgrid(x, y):
    """Return coordinate matrices from two coordinate vectors.

    Args:
        x (TYPE): Description
        y (TYPE): Description
    """
    x = np.asarray(x)
    y = np.asarray(y)
    numRows, numCols, numDepths = y.shape[1], x.shape[1], x.shape[0]

    x = x.reshape(numDepths, 1, numCols)
    X = x.repeat(numRows, axis=1)

    y = y.reshape(numDepths, numRows, 1)
    Y = y.repeat(numCols, axis=2)
    return X, Y


if __name__ == '__main__':

    x = [[1, 2, 3], [3, 4, 5]]
    y = [[1, 2, 3], [3, 4, 5]]
    aa, bb = meshgrid(x, y)
    print(aa)
    print(bb)
