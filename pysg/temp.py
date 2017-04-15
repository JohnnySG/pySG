#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
import scipy.sparse as scsparse
from matplotlib import pyplot as plt
from numpy import poly1d
from scipy.sparse.linalg import spsolve
import scipy as sc

# a = np.array([[2, -1], [-1, 2]])
# b = np.array([[1, -1], [-1, 4]])

# print(a)
# print(b)
# print(a @ b)
# print(b @ a)


c = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# invs = np.linalg.inv(c)
# sqr = sc.linalg.sqrtm(invs)
diag, eigV = sc.linalg.eig(c)

print(c)
print(diag)
print(eigV)

print(512888. - 213784 * np.exp(0.875092))
# print(sc.linalg.sqrtm(c))

# print(sc.linalg.sqrtm(invs))
# print(sc.linalg.expm(sqr))
# print(np.array([[100, 1, 2], [1, 100, 90], [1, 102, 100]]))
# print(sc.linalg.sqrtm(np.array([[100, 1, 2], [1, 100, 97], [1, 103, 100]])))


