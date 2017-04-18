#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 18:04:11
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-18 20:30:38
# ----------------------------------------


class Material(object):
    def __init__(self, E, mu, gamma, alpha):
        """Summary

        Args:
            E (float): Description
            mu (float): Description
            gamma (float): Description
            alpha (float): Description
        """
        self.E = E
        self.mu = mu
        self.gamma = gamma
        self.alpha = alpha
        self.shearModulus = E / 2 / (1 + mu)

    @property
    def G(self):
        """Summary

        Returns:
            Ouput (float): Shear Modulus
        """
        return self.shearModulus

if __name__ == '__main__':

    E = 3.55 * 10**7
    mu = 0.2
    gamma = 0
    alpha = 0
    mat = Material(E, mu, gamma, alpha)
    print(mat.G)
