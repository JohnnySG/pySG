#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Johnny
# @Date:   2016-07-12 11:40:10
# @Email:  sg19910914@gmail.com
# @Last Modified by:   Johnny
# @Last Modified time: 2016-07-26 10:19:35
# ----------------------------------------
import numpy as np


class CoordinateSystem:
    def __init__(self, origin, pt1, pt2):
        """
        Args:
            origin (TYPE): 3x1 vector
            pt1 (TYPE): 3x1 vector
            pt2 (TYPE): 3x1 vector

        Raises:
            Exception: Description
        """
        self.origin = origin
        vec1 = np.array([pt1[0] - origin[0], pt1[1] -
                         origin[1], pt1[2] - origin[2]])
        vec2 = np.array([pt2[0] - origin[0], pt2[1] -
                         origin[1], pt2[2] - origin[2]])
        cos = np.dot(vec1, vec2) / np.linalg.norm(vec1) / np.linalg.norm(vec2)
        if cos == 1 or cos == -1:
            raise Exception("Three points should not in a line!!")
        self.x = vec1 / np.linalg.norm(vec1)
        z = np.cross(vec1, vec2)
        self.z = z / np.linalg.norm(z)
        self.y = np.cross(self.z, self.x)

    def SetBy3Pts(self, origin, pt1, pt2):
        """
        Args:
            origin (TYPE): tuple 3
            pt1 (TYPE): tuple 3
            pt2 (TYPE): tuple 3

        Raises:
            Exception: Description
        """
        self.origin = origin
        vec1 = np.array([pt1[0] - origin[0], pt1[1] -
                         origin[1], pt1[2] - origin[2]])
        vec2 = np.array([pt2[0] - origin[0], pt2[1] -
                         origin[1], pt2[2] - origin[2]])
        cos = np.dot(vec1, vec2) / np.linalg.norm(vec1) / np.linalg.norm(vec2)
        if cos == 1 or cos == -1:
            raise Exception("Three points should not in a line!!")
        self.x = vec1 / np.linalg.norm(vec1)
        z = np.cross(vec1, vec2)
        self.z = z / np.linalg.norm(z)
        self.y = np.cross(self.z, self.x)

    def SetOrigin(self, x, y, z):
        """
        Args:
            x (TYPE): Description
            y (TYPE): Description
            z (TYPE): Description
        """
        self.origin = (x, y, z)

    def AlignWithGlobal(self):
        self.x = np.array([1, 0, 0])
        self.y = np.array([0, 1, 0])
        self.z = np.array([0, 0, 1])

    def TransformMatrix(self):
        x = self.x
        y = self.y
        z = self.z
        V = np.array([[x[0], y[0], z[0]],
                      [x[1], y[1], z[1]],
                      [x[2], y[2], z[2]]])
        return V.transpose()

csys = CoordinateSystem((0, 0, 0), (1, 1, 0), (0, 1, 0))
csys.AlignWithGlobal()
