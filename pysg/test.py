#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
import scipy.sparse as scsparse
from matplotlib import pyplot as plt
from numpy import poly1d
from scipy.sparse.linalg import spsolve

import model
import elemLib
import core


# def foo():
# 定义材料特性和截面参数
b = 3
A = 10.3
E = 3.55 * 10**7
G = 0.417 * E
I = 6.0285
Is = 1.5654
Ss = -2.8 * 0.7299

# b = 77
# A = 2568
# E = 2800
# G = E / (2 * (1 + 0.37))
# I = 1551449.6199
# Is = 139930.7773 * 2 + 279861.5546 + 743246.3226
# Ss = -21.2835 * 616 - 21.2835 * 308 * 2 + 616 * 34.7165

# 定义节点
q = np.array([
    [0, 0],
    [1, 0],
    [2, 0],
    [3, 0],
    [4, 0],
    [5, 0],
    [6, 0],
    [7, 0],
    [8, 0],
    [9, 0],
    [10, 0],
    [11, 0],
    [12, 0],
    [13, 0],
    [14, 0],
    [15, 0],
    [16, 0],
    [17, 0],
    [18, 0],
    [19, 0],
    [20, 0],
    [21, 0],
    [22, 0],
    [23, 0],
    [24, 0],
    [25, 0],
    [26, 0],
    [27, 0],
    [28, 0],
    [29, 0],
    [30, 0],
    [31, 0],
    [32, 0],
    [33, 0],
    [34, 0],
    [35, 0],
    [36, 0],
    [37, 0],
    [38, 0],
    [39, 0],
    [40, 0],
])

# 定义单元
me = np.array([
    [1, 2],
    [2, 3],
    [3, 4],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 8],
    [8, 9],
    [9, 10],
    [10, 11],
    [11, 12],
    [12, 13],
    [13, 14],
    [14, 15],
    [15, 16],
    [16, 17],
    [17, 18],
    [18, 19],
    [19, 20],
    [20, 21],
    [21, 22],
    [22, 23],
    [23, 24],
    [24, 25],
    [25, 26],
    [26, 27],
    [27, 28],
    [28, 29],
    [29, 30],
    [30, 31],
    [31, 32],
    [32, 33],
    [33, 34],
    [34, 35],
    [35, 36],
    [36, 37],
    [37, 38],
    [38, 39],
    [39, 40],
    [40, 41],
])

# 施加约束条件
cons = np.array([
    [1, 0, 0, 1, 1],
    [21, 1, 0, 1, 1],
    [41, 1, 0, 1, 1],

])

# 定义荷载
nLoad = np.array([
    [41, 0, 0, 0, 0],
])

beam = elemLib.ShearLagElem(q, me, b, A, E, G, I, Ss, Is, cons)

Kg, Ig, Jg = beam.stiffness()
KK = model.assembling(Ig, Jg, Kg)

NLoad = beam.nodeLoad(nLoad)
# DLoad, ii, jj = beam.distrLoad1(dLoad)
DLoad, ii, jj = beam.distrLoad(q0=0, qu=0, qv=450)
DLoad = model.assembling(ii, jj, DLoad)
Load = DLoad + NLoad

# plt.spy(KK)
# plt.show()

pltDOF = beam.DOF[:, 1]
pltX = q[pltDOF != 0, 0]
pltDOF = pltDOF[pltDOF != 0] - 1

print(beam.DOF)
print(beam.LOC)

disp = spsolve(KK, Load)
# print(pltX)
# print(disp[pltDOF])
# plt.plot(pltX, disp[pltDOF], "o")
# plt.show()

De = np.array(beam.LOC, dtype=np.float64)
De = De.reshape((40, 8, 1))
DeView = De.ravel()
valu, indices = np.unique(DeView, return_inverse=True)
valu[1:] = disp
DeView[:] = valu[indices]

zzz = beam.Ke @ De - beam.Ke @ beam.bDe + beam.bFe
# print(zzz[:, 2, 0])
# print(zzz[:, 6, 0])


# if __name__ == "__main__":
#     import cProfile
#     cProfile.run("foo()")
