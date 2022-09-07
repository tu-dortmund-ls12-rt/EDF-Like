#!/usr/bin/env python3
"""Taken from SSSEvaluation:
https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/blob/master/schedTest/RTEDF.py"""

import math  # math.ceil(), math.floor()


def sort_by_period(tasks):  # lowest period first -- maybe not necessary?
    newlist = sorted(tasks, key=lambda k: k['period'])
    return newlist


def RTEDF(tasks):
    return RTEDF_with_improv(tasks)


def RTEDF_wo_improv(tasks):
    htasks = sort_by_period(tasks)
    n = len(htasks)
    Rtilde = [0] * n
    for k in range(n - 1, -1, -1):
        Atilde = [0] * n  # Compute Atilde_i^k for all i
        for i in range(n):
            if i != k:
                Tk = htasks[k]['period']
                Ti = htasks[i]['period']
                Ck = htasks[k]['execution']
                Ci = htasks[i]['execution']
                Sk = htasks[k]['sslength']

                if i < k:
                    Atilde[i] = Tk - math.floor(Tk / Ti) * Ti
                if i > k:
                    Atilde[i] = Tk + Rtilde[i] - (math.floor(Tk / Ti) + 1) * Ti

        # print('Atilde')
        # print(Atilde)

        Rtildek = [0] * (n)  # Compute Rtilde_k(j) for all j
        for j in range(n):
            if j == k:  # this is the j==0 case
                R = 0
                R += Ck + Sk
                for ji in range(n):
                    if ji != k:
                        R += math.floor(htasks[k]['period'] / htasks[ji]['period']) * htasks[ji]['execution']
                for ji in range(n):
                    if ji != k:
                        R += htasks[ji]['execution']
                Rtildek[j] = R
            else:
                R = 0
                R += Ck + Sk
                for ji in range(n):
                    if ji != k:
                        R += math.floor(htasks[k]['period'] / htasks[ji]['period']) * htasks[ji]['execution']
                for ji in range(n):
                    if ji != k and Atilde[ji] > Atilde[j]:
                        R += htasks[ji]['execution']
                R += max(Atilde[j], 0)
                Rtildek[j] = R
        Rtilde[k] = min(Rtildek)
        # print('Rtilde')
        # print(Rtilde)
        if Rtilde[k] > htasks[k]['period']:
            return False
    return True


def RTEDF_with_improv(tasks):
    htasks = sort_by_period(tasks)
    n = len(htasks)
    Rtilde = [0] * n
    for k in range(n - 1, -1, -1):
        Atilde = [0] * n  # Compute Atilde_i^k for all i
        for i in range(n):
            if i != k:
                Tk = htasks[k]['period']
                Ti = htasks[i]['period']
                Ck = htasks[k]['execution']
                Ci = htasks[i]['execution']
                Sk = htasks[k]['sslength']

                if i < k:
                    Atilde[i] = Tk - math.floor(Tk / Ti) * Ti
                if i > k:
                    Atilde[i] = Tk + Rtilde[i] - (math.floor(Tk / Ti) + 1.0) * Ti

        # print('Atilde')
        # print(Atilde)

        Rtildek = [0] * (n)  # Compute Rtilde_k(j) for all j
        for j in range(n):
            mjk = max(Atilde[j], 0.0)
            if j == k:  # this is the j==0 case
                R = 0.0
                R += Ck + Sk
                for ji in range(n):
                    if ji != k:
                        R += math.floor(htasks[k]['period'] / htasks[ji]['period']) * htasks[ji]['execution']
                for ji in range(n):
                    if ji != k:
                        R += htasks[ji]['execution']
                Rtildek[j] = R
            else:
                R = 0.0
                R += Ck + Sk
                for ji in range(n):
                    if ji != k and Atilde[ji] <= Atilde[j]:
                        R += min(math.floor(htasks[k]['period'] / htasks[ji]['period']),
                                 math.ceil((htasks[k]['period'] - mjk) / htasks[ji]['period'])) * htasks[ji][
                                 'execution']
                for ji in range(n):
                    if ji != k and Atilde[ji] > Atilde[j]:
                        R += min(math.floor(htasks[k]['period'] / htasks[ji]['period']) + 1.0,
                                 math.ceil((htasks[k]['period'] - mjk) / htasks[ji]['period'])) * htasks[ji][
                                 'execution']
                R += mjk
                Rtildek[j] = R
        Rtilde[k] = min(Rtildek)
        # print('Rtilde')
        # print(Rtilde)
        if Rtilde[k] > htasks[k]['period']:
            return False
    return True

# # Testing
# task1 = {'execution':1.9, 'sslength':1.1, 'period':6}
# task2 = {'execution':8.9, 'sslength':1.1, 'period':20}
# T = [task1, task2]
#
# print(RTEDF(T))
