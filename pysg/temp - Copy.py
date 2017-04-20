#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
import scipy.sparse as scsparse
from matplotlib import pyplot as plt
from numpy import poly1d
from scipy.sparse.linalg import spsolve
import iopro
import pandas as pd

import core
import material
import section
import model
import element

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

# # Node Coordinates
# adapter = iopro.text_adapter('NodeTable.csv', parser='csv')
# adapter.set_field_types({"x": 'f8', "z": 'f8'})
# nod = adapter[["x", "z"]][:]
# nod = nod.view('f8').reshape(nod.shape + (-1,))

# # Element Connectivity
# adapter = iopro.text_adapter('ElementTable.csv', parser='csv')
# ele = adapter[["i", "j"]][:]
# ele = ele.view('i8').reshape(ele.shape + (-1,))

# # Constraint Settings
# adapter = iopro.text_adapter('ConstraintTable.csv', parser='csv')
# cons = adapter[:]
# cons = cons.view('i8').reshape(cons.shape + (-1,))

# # Nodal Forces
# adapter = iopro.text_adapter('LoadTable.csv', parser='csv')
# adapter.set_field_types(
#     {
#         "Node": 'i8', "F1": 'f8', "F2": 'f8', "F3": 'f8', "F4": 'f8',
#         "Element": 'f8', "qui": 'f8', "quj": 'f8', "qvi": 'f8', "qvj": 'f8'
#     }
# )
# adapter.set_fill_values({0: 0})
# nLoad = adapter[["Node", "F1", "F2", "F3", "F4"]][:]
# dLoad = adapter[["qui", "quj", "qvi", "qvj"]][:]
# nLoad = nLoad.view('i8').reshape(nLoad.shape + (-1,))
# nLoad = nLoad[nLoad[:, 0] != 0]
# dLoad = dLoad.view('f8').reshape(dLoad.shape + (-1,))
# # print(nLoad)

# 读取模型文件
xlsx = pd.ExcelFile('Data.xlsx')

nod = xlsx.parse('Node', index_col=0)
ele = xlsx.parse('Element', index_col=0)
cons = xlsx.parse('Constraint', index_col=0)
nLoad = xlsx.parse('nLoad', index_col=0)
eLoad = xlsx.parse('eLoad', index_col=0)

# nod.sort_index(inplace=True)
# print(nod.loc[[1, 2], ["x", "z"]])

# 定义材料特性与截面几何特性
mat = material.Material(E, mu, gamma, alpha)
sec = section.Section(A, I, Aw, Sw, Iw, Iww)

# 计算局部坐标系下的单元刚度矩阵
beam = element.ShearLag(mat, sec, nod, ele)
Ke = beam.stiffness()

# # 计算自由度和单元定位向量
# DOF = core.getDOF(cons, nod.shape[0])
# LOC = core.getLOC(DOF, ele)
print(cons)
# # 计算整体坐标系下的单元刚度矩阵
# stru = model.Model(beam, LOC)
# stru.assemble()

# plt.spy(stru.Kmat)
# plt.show()
# print(DOF)

# load = stru.load(nLoad, dLoad)


# distrLoad(0, 0, 450, 0)
# print(LOC)

# node_load = beam.nodeLoad(nLoad)
# # DLoad, ii, jj = beam.distrLoad1(dLoad)
# DLoad, ii, jj = beam.distrLoad(q0=0, qu=0, qv=450)
# DLoad = model.assembling(ii, jj, DLoad)
# Load = DLoad + NLoad


# pltDOF = beam.DOF[:, 1]
# pltX = q[pltDOF != 0, 0]
# pltDOF = pltDOF[pltDOF != 0] - 1

# print(beam.DOF)
# print(beam.LOC)

# disp = spsolve(Kmat, load)
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

# zzz = beam.Ke @ De - beam.Ke @ beam.bDe + beam.bDF
# # print(zzz[:, 2, 0])
# # print(zzz[:, 6, 0])


# # if __name__ == "__main__":
# #     import cProfile
# #     cProfile.run("foo()")
