#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: JohnnySG
# @Date:   2017-04-15 14:55:45
# @Email:  sg19910914@gmail.com
# @Last Modified by:   JohnnySG
# @Last Modified time: 2017-04-15 21:46:42
# ----------------------------------------

import numpy as np
import scipy.sparse as scsparse


class Model(object):
    """Summary

    Attributes:
        database (TYPE): Description
    """

    def __init__(self, db):
        """Summary

        Args:
            db (TYPE): Description
        """
        super().__init__()
        self.database = db

    def save(self):
        """Summary

        Returns:
            Ouput (TYPE): Description
        """
        return

    def is_assembled(self):
        if self.Kmat is None:
            return False
        return True


def assemble(Ig, Jg, Kg):
    """Assembly of the Stiffness Matrix

    Args:
        Ig (TYPE): Description
        Jg (TYPE): Description
        Kg (TYPE): Description

    Returns:
        Ouput (TYPE): Description
    """

    return scsparse.csr_matrix(
        (
            Kg, (Ig, Jg)
        )
    )


def extract_displpacement(Ig, Jg, Kg):
    """Assembly of the Stiffness Matrix

    Args:
        Ig (TYPE): Description
        Jg (TYPE): Description
        Kg (TYPE): Description

    Returns:
        Ouput (TYPE): Description
    """

    return scsparse.csr_matrix(
        (
            Kg, (Ig, Jg)
        )
    )
