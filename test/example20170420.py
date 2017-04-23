#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
from numpy import poly1d
from scipy.sparse.linalg import spsolve
from scipy.interpolate import spline
import scipy.sparse as scsparse
from matplotlib import pyplot as plt
import pandas as pd
import pysg


# 材料特性
# =================================================================
E = 3.55 * 10**7
mu = 0.2
gamma = 0
alpha = 0
mat = pysg.Material(E, mu, gamma, alpha)


# 截面几何特性
# =================================================================
A = 10.3
I = 6.0285
Sw = -1.28276
Iw = 1.107_580
Iww = 0.796819
Aw = 0.247913
sec = pysg.Section(A, I, Aw, Sw, Iw, Iww)


# 读取模型文件
# =================================================================
xlsx = pd.ExcelFile('Data.xlsx')
nod_tab = xlsx.parse('Node', index_col=0)
ele_tab = xlsx.parse('Element', index_col=0)
res = xlsx.parse('Restraint', index_col=0)
nLoad = xlsx.parse('nLoad', index_col=0)
eLoad = xlsx.parse('eLoad', index_col=0)


# 定义节点自由度
# =================================================================
num_dof = 4
DOF = pysg.DegreeFreedom(nod_tab, num_dof)


# 定义节点、施加节点荷载、设置节点约束
# =================================================================
node = pysg.Node(nod_tab)
node.setLoad(nLoad)
node.setRestraints(res)


# 定义梁单元、施加单元荷载
# =================================================================
# beam = pysg.ShearLag(mat, sec, nod_tab, ele_tab)
# beam.setLoad(eLoad)
# nod_tab.loc[ele_tab[[0]]]
print(ele_tab)
print("['i']", type(ele_tab['i']))
print("[[0]]", type(ele_tab[[0]]))
print(".loc[3]", type(ele_tab.loc[3]))
print(".loc[[3]]", type(ele_tab.loc[[3]]))
print(".iloc[3]", type(ele_tab.iloc[3]))


# # 形成结构总刚、施加荷载作用、设置边界条件
# # =================================================================
# stru = pysg.Model(beam)
# stru.formLoadVec()
# stru.setBoundary()


# # 求解平衡方程, 获得位移解
# # =================================================================
# nD = spsolve(stru.Kmat, stru.load)
# nD = nD.reshape(node.DOF.shape)
# displacement = nD[:, 1]


# # 计算单元杆端力
# # =================================================================
# # eD = pysg.core.getLOC(nD_Mat, ele_tab).reshape((ele_tab.shape[0], 8, 1))
# # Fe = beam.Ke @ beam.trans @ eD - beam.equLoad
# #
# # nn = 2
# # force = (np.r_[Fe[:, nn, 0], 0] - np.r_[0, Fe[:, nn + 4, 0]]) / 2
# # force[0] = Fe[0, nn, 0]
# # force[-1] = -Fe[-1, nn + 4, 0]
# # # print(force)
# #
# # n2 = 3
# # force2 = (np.r_[Fe[:, n2, 0], 0] - np.r_[0, Fe[:, n2 + 4, 0]]) / 2
# # force2[0] = Fe[0, n2, 0]
# # force2[-1] = -Fe[-1, n2 + 4, 0]
# #
# print(nD)


# # 绘制位移图、内力图
# # =================================================================
# pltX = nod_tab.iloc[:, 0].values
# x_smooth = np.linspace(0, pltX[-1], 200)
# y_smooth = spline(pltX, displacement, x_smooth)
# # y_smooth2 = spline(pltX, force2, x_smooth)
# # print(x_smooth[::1])
# # print(y_smooth[::1])


# plt.plot(x_smooth, y_smooth, '-.')
# # plt.plot(x_smooth, y_smooth2, '-')
# plt.show()


if __name__ == "__main__":

    import cProfile

    def foo():
        pass

    # cProfile.run("foo()")
