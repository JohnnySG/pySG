#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 18:04:11
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-15 18:04:38
# ----------------------------------------


class Material:
    def __init__(self, E, mu, gamma, alpha):
        """Summary

        Args:
            E (TYPE): Description
            mu (TYPE): Description
            gamma (TYPE): Description
            alpha (TYPE): Description
        """
        self.E = E
        self.mu = mu
        self.gamma = gamma
        self.alpha = alpha
        self.shearModulus = E / 2 / (1 + mu)

    def G(self):
        """Summary

        Returns:
            Ouput (TYPE): Shear Modulus
        """
        return self.shearModulus
