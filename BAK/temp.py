#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
from numpy import poly1d
from scipy.sparse.linalg import spsolve
from scipy.interpolate import spline
import scipy.sparse as scsparse
from matplotlib import pyplot as plt
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

# 读取模型文件
xlsx = pd.ExcelFile('Data.xlsx')
nod = xlsx.parse('Node', index_col=0)
ele = xlsx.parse('Element', index_col=0)
cons = xlsx.parse('Constraint', index_col=0)
nLoad = xlsx.parse('nLoad', index_col=0)
eLoad = xlsx.parse('eLoad', index_col=0)

# 定义材料特性与截面几何特性
mat = material.Material(E, mu, gamma, alpha)
sec = section.Section(A, I, Aw, Sw, Iw, Iww)

# 计算局部坐标系下的单元刚度矩阵
beam = element.ShearLag(mat, sec, nod, ele)
Ke = beam.stiffness()

# # 计算自由度和单元定位向量
DOF = core.getDOF(cons, nod.shape[0])
LOC = core.getLOC(DOF, ele)

# 计算整体坐标系下的单元刚度矩阵
stru = model.Model(beam, LOC)
Kmat = stru.assemble()

# 计算综合节点荷载列阵
load = stru.load(nLoad, eLoad)

# 求解平衡方程, 获得位移解
nD = spsolve(Kmat, load)
nD_Mat = np.zeros_like(DOF, dtype="f8")
nD_Mat[DOF != 0] = nD
displacement = nD_Mat[:, 0]
# print(displacement)


# 计算单元杆端力
eD = core.getLOC(nD_Mat, ele).reshape((ele.shape[0], 8, 1))
Fe = beam.Ke @ eD - stru.dFe
nn = 2
force = (np.r_[Fe[:, nn, 0], 0] - np.r_[0, Fe[:, nn + 4, 0]]) / 2
force[0] = Fe[0, nn, 0]
force[-1] = -Fe[-1, nn + 4, 0]
# print(force)
n2 = 3
force2 = (np.r_[Fe[:, n2, 0], 0] - np.r_[0, Fe[:, n2 + 4, 0]]) / 2
force2[0] = Fe[0, n2, 0]
force2[-1] = -Fe[-1, n2 + 4, 0]

# 绘制位移图、内力图
pltX = nod.iloc[:, 0].values
x_smooth = np.linspace(0, pltX[-1], 200)
y_smooth = spline(pltX, displacement, x_smooth)
y_smooth2 = spline(pltX, force2, x_smooth)

plt.plot(x_smooth, y_smooth, '-.')
# plt.plot(x_smooth, y_smooth2, '-')
plt.show()


if __name__ == "__main__":

    pass
