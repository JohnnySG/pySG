#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
import scipy.sparse as scsparse
from matplotlib import pyplot as plt
from numpy import poly1d
from scipy.sparse.linalg import spsolve
import iopro

import model
import elemment
import core
import material
import section

# 材料特性
E = 3.55 * 10**7
mu = 0.2
gamma = 0
alpha = 0

# 截面几何特性
A = 10.3
I = 6.0285
Sw = -1.28276
Iw = 1.00748
Iww = 0.796819
Aw = 0.247913

# Node Coordinates
adapter = iopro.text_adapter('NodeTable.csv', parser='csv')
adapter.set_field_types({"x": 'f8', "z": 'f8'})
node = adapter[["x", "z"]][:]
node = node.view('f8').reshape(node.shape + (-1,))

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
nLoad = adapter[["Force 1"]][:]
# nLoad = nLoad.view('i8').reshape(nLoad.shape + (-1,))
# print(adapter.get_field_names())
# print(element)

# 定义材料特性与截面几何特性
mat = material.Material(E, mu, gamma, alpha)
sec = section.Section(A, I, Aw, Sw, Iw, Iww)
cons = constraint

beam = elemment.ShearLag(mat, sec, node, element)
# Kg, Ig, Jg = beam.stiffness()
Ke = beam.stiffness()

print(beam.Ke[0])
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
