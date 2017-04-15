#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Johnny
# @Date:   2016-07-12 11:40:10
# @Email:  sg19910914@gmail.com
# @Last Modified by:   Johnny
# @Last Modified time: 2016-07-26 10:21:30
# ----------------------------------------


class Section:
    def __init__(self, mat, A, J, I33, I22):
        """Summary

        Args:
            mat (TYPE): Description
            A (TYPE): Area
            J (TYPE): Description
            I33 (TYPE): Description
            I22 (TYPE): Description
        """
        self.material = mat
        self.A = A
        self.J = J
        self.I33 = I33
        self.I22 = I22
