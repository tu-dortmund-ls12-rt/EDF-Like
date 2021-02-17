# Typical fixed priority analyses using TDA.
# E.g. specified in "A Unifying Response Time Analysis Framework for
# Dynamic Self-Suspending Tasks" from Chen, Nelissen, Huang in 2016
# https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/2016-chen-report-850.pdf
import math


def SuspObl(tasks):
    # Suspension oblivious test, given by Eq 1.
    # Given: tasks ordered by priority.
    for idx in range(len(tasks)):
        wcrt = SuspObl_WCRT(tasks[idx], tasks[:idx])
        if wcrt > tasks[idx]['deadline']:  # deadline miss
            return False
        else:
            tasks[idx]['wcrt_uniframework'] = wcrt  # set wcrt
            continue
    return True


def SuspObl_WCRT(task, HPTasks):
    # Compute the response time bound using Eq 1.
    t = task['execution'] + task['sslength']
    while True:
        # Compute lhs of Eq 1.
        wcrt = task['execution'] + task['sslength']
        for itask in HPTasks:
            wcrt += math.ceil(t/itask['period'])*(
                itask['execution']+itask['suspension'])
        if (wcrt > task['deadline']  # deadline miss
                or wcrt <= t):  # Eq 1 holds
            break
        t = wcrt  # increase t for next iteration
    return wcrt
