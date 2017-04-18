#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
import scipy.sparse as scsparse
from matplotlib import pyplot as plt
from numpy import poly1d
from scipy.sparse.linalg import spsolve
import iopro

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

# Node Coordinates
adapter = iopro.text_adapter('NodeTable.csv', parser='csv')
node = adapter[["x", "z"]][:]
node = node.view('i8').reshape(node.shape + (-1,))

# Element Connectivity
adapter = iopro.text_adapter('ElementTable.csv', parser='csv')
element = adapter[["i", "j"]][:]
element = element.view('i8').reshape(element.shape + (-1,))

# Constraint Settings
adapter = iopro.text_adapter('ConstraintTable.csv', parser='csv')
constraint = adapter[:]
constraint = constraint.view('i8').reshape(constraint.shape + (-1,))

# Nodal Forces
adapter = iopro.text_adapter('LoadTable.csv', parser='csv')
nLoad = adapter[:]
nLoad = nLoad.view('i8').reshape(nLoad.shape + (-1,))


# beam = elemLib.ShearLagElem(q, me, b, A, E, G, I, Ss, Is, cons)

# Kg, Ig, Jg = beam.stiffness()
# KK = model.assembling(Ig, Jg, Kg)

# NLoad = beam.nodeLoad(nLoad)
# # DLoad, ii, jj = beam.distrLoad1(dLoad)
# DLoad, ii, jj = beam.distrLoad(q0=0, qu=0, qv=450)
# DLoad = model.assembling(ii, jj, DLoad)
# Load = DLoad + NLoad

# # plt.spy(KK)
# # plt.show()

# pltDOF = beam.DOF[:, 1]
# pltX = q[pltDOF != 0, 0]
# pltDOF = pltDOF[pltDOF != 0] - 1

# print(beam.DOF)
# print(beam.LOC)

# disp = spsolve(KK, Load)
# # print(pltX)
# # print(disp[pltDOF])
# # plt.plot(pltX, disp[pltDOF], "o")
# # plt.show()

# De = np.array(beam.LOC, dtype=np.float64)
# De = De.reshape((40, 8, 1))
# DeView = De.ravel()
# valu, indices = np.unique(DeView, return_inverse=True)
# valu[1:] = disp
# DeView[:] = valu[indices]

# zzz = beam.Ke @ De - beam.Ke @ beam.bDe + beam.bFe
# # print(zzz[:, 2, 0])
# # print(zzz[:, 6, 0])


# # if __name__ == "__main__":
# #     import cProfile
# #     cProfile.run("foo()")
