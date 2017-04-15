#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
import scipy.sparse as scsparse


def assembling(Ig, Jg, Kg):
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


def extractDe(Ig, Jg, Kg):
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
