#!/usr/bin/env python3
"""Taken from SSSEvaluation:
https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/blob/master/schedTest/FixedPriority.py"""

# Typical fixed priority analyses using TDA.
# E.g. specified in "A Unifying Response Time Analysis Framework for
# Dynamic Self-Suspending Tasks" from Chen, Nelissen, Huang in 2016
# https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/2016-chen-report-850.pdf
import math


# Suspension Oblivious.
def SuspObl(tasks):
    # Suspension oblivious test, given by Eq 1.
    # Given: tasks ordered by priority.
    for idx in range(len(tasks)):
        wcrt = SuspObl_WCRT(tasks[idx], tasks[:idx])
        if wcrt > tasks[idx]['deadline']:  # deadline miss
            return False
        else:
            tasks[idx]['wcrt_obl'] = wcrt  # set wcrt
            continue
    return True


def SuspObl_WCRT(task, HPTasks):
    # Compute the response time bound using Eq 1.
    t = task['execution'] + task['sslength']
    while True:
        # Compute lhs of Eq 1.
        wcrt = task['execution'] + task['sslength']
        for itask in HPTasks:
            wcrt += math.ceil(t / itask['period']) * (
                    itask['execution'] + itask['sslength'])
        if (wcrt > task['deadline']  # deadline miss
                or wcrt <= t):  # Eq 1 holds
            break
        t = wcrt  # increase t for next iteration
    return wcrt


# Suspension as Release Jitter.
def SuspJit(tasks):
    # Suspension as release jitter, given by Eq 2.
    # Given: tasks ordered by priority.
    for idx in range(len(tasks)):
        wcrt = SuspJit_WCRT(tasks[idx], tasks[:idx])
        if wcrt > tasks[idx]['deadline']:  # deadline miss
            return False
        else:
            tasks[idx]['wcrt_jit'] = wcrt  # set wcrt
            continue
    return True


def SuspJit_WCRT(task, HPTasks):
    # Compute the response time bound using Eq 2.
    t = task['execution'] + task['sslength']
    while True:
        # Compute lhs of Eq 2.
        wcrt = task['execution'] + task['sslength']
        for itask in HPTasks:
            wcrt += math.ceil(
                (t + itask['wcrt_jit'] - itask['execution']) / itask['period']
            ) * itask['execution']
        if (wcrt > task['deadline']  # deadline miss
                or wcrt <= t):  # Eq 2 holds
            break
        t = wcrt  # increase t for next iteration
    return wcrt


# Suspension as Blocking.
def SuspBlock(tasks):
    # Suspension as blocking, given by Eq 3.
    # Given: tasks ordered by priority.
    for idx in range(len(tasks)):
        wcrt = SuspBlock_WCRT(tasks[idx], tasks[:idx])
        if wcrt > tasks[idx]['deadline']:  # deadline miss
            return False
        else:
            tasks[idx]['wcrt_block'] = wcrt  # set wcrt
            continue
    return True


def SuspBlock_WCRT(task, HPTasks):
    # Compute the response time bound using Eq 3.

    # Compute B.
    B = task['sslength']
    for itask in HPTasks:
        B += min(itask['execution'], itask['sslength'])

    t = task['execution'] + task['sslength']
    while True:
        # Compute lhs of Eq 3.
        wcrt = task['execution'] + B
        for itask in HPTasks:
            wcrt += math.ceil(t / itask['period']) * itask['execution']
        if (wcrt > task['deadline']  # deadline miss
                or wcrt <= t):  # Eq 2 holds
            break
        t = wcrt  # increase t for next iteration
    return wcrt
