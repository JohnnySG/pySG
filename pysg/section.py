#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Johnny
# @Date:   2016-07-12 11:40:10
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-18 20:31:56
# ----------------------------------------


class Section(object):
    def __init__(self, A, I, Aw, Sw, Iw, Iww):
        """Define the cross-section properties

        Args:
            A (TYPE): Area
            I (TYPE): Description
            Aw (TYPE): Description
            Sw (TYPE): Description
            Iw (TYPE): Description
            Iww (TYPE): Description
        """
        self.A = A
        self.I = I
        self.Aw = Aw
        self.Sw = Sw
        self.Iw = Iw
        self.Iww = Iww

if __name__ == '__main__':
    A = 10.3
    I = 6.0285
    Aw = 0.247913
    Sw = -1.28276
    Iw = 1.00748
    Iww = 0.796819
    sec = Section(A, I, Aw, Sw, Iw, Iww)
    print(sec.Iww)
