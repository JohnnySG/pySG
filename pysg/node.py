#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 18:01:33
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-22 23:01:21
# ----------------------------------------
import numpy as np
import pandas as pd


class Node(object):
    def __init__(self, node_tab):
        """Summary

        Args:
            x (float): x-coordinate of Node
            y (float): y-coordinate of Node
            z (float): z-coordinate of Node
        """
        self.coord = node_tab
        self.x = node_tab[[0]]
        self.y = node_tab[[1]]
        self.z = node_tab[[2]]

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


if __name__ == '__main__':

    pass
