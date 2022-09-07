#!/usr/bin/env python3
"""Taken from SSSEvaluation:
https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/blob/master/schedTest/SCEDF.py"""


def EDFB(U):
    if U > 1:
        return False
    else:
        return True


def SC_EDF(tasks):
    U = 0
    for itask in tasks:
        U += (itask['execution'] + itask['sslength']) / itask['period']

    return EDFB(U)
