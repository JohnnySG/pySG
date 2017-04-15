#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 18:01:33
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-15 18:03:24
# ----------------------------------------
import numpy as np
import CoordinateSystem


class Node(object):
    def __init__(self, x, y, z):
        """Summary

        Args:
            x (float): x-coordinate of Node
            y (float): y-coordinate of Node
            z (float): z-coordinate of Node
        """
        self.x = x
        self.y = y
        self.z = z
        o = [x, y, z]
        pt1 = [x + 1, y, z]
        pt2 = [x, y + 1, z]
        self.localCsys = CoordinateSystem.CoordinateSystem(o, pt1, pt2)
        self.restraints = [False] * 6
        self.load = [False] * 6
        self.disp = [False] * 6

    def TransformMatrix(self):
        """Summary

        Returns:
            Ouput (TYPE): Description
        """
        V = self.localCsys.TransformMatrix()
        V_ = np.zeros((6, 6))
        V_[:3, :3] = V_[3:, 3:] = V
        return V_

    def InitializeCsys(self):
        """Summary

        Returns:
            Ouput (TYPE): Description
        """
        self.localCsys.AlignWithGlobal()

    def setLoad(self, load):
        """
        load: a number vector indicates a nodal load.

        Args:
            load (TYPE): Description
        """
        self.load = load

    def setDisp(self, disp):
        """
        load: a number vector indicates a nodal displacement.

        Args:
            disp (TYPE): Description
        """
        self.disp = disp

    def setRestraints(self, res):
        """
        res: a boolean vector indicates a nodal displacement.

        Args:
            res (TYPE): Description
        """
        self.restraints = res
