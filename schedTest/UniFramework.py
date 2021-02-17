# Schedulability test from "A Unifying Response Time Analysis Framework for
# Dynamic Self-Suspending Tasks" from Chen, Nelissen, Huang in 2016
# https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/2016-chen-report-850.pdf
import math


def compute_sum_entry_Eq4(t, Q, x, R, C, T):
    # Compute one entry of the sum on the left hand side from Equation 4.
    return C*math.ceil((t+Q+(1-x)*(R-C))/T)


def compute_lhs_Eq4(task, HPTasks, vec_x, t, Q):
    # Compute the left hand side from Equation 4.
    total = task['execution'] + task['sslength']
    # for itask, ix in zip(HPTasks, vec_x):
    for idx in range(len(HPTasks)):
        itask = HPTasks[idx]
        ix = vec_x[idx]
        total += compute_sum_entry_Eq4(
            t, Q[idx], ix, itask['wcrt_uniframework'],
            itask['execution'], itask['period'])
    return total


def compute_WCRT_bound(task, HPTasks, vec_x):
    # Compute the response time bound using Theorem 1.
    # Given: vector x

    # Compute Q.
    Q = []
    Qvar = 0.0
    for idx in range(len(HPTasks)-1, 0-1, -1):
        Qvar += HPTasks[idx]['sslength']*vec_x[idx]
        Q.insert(0, Qvar)
    # for itask, ix in zip(HPTasks, vec_x):
    #     Q += itask['sslength']*ix

    # TDA.
    t = task['execution'] + task['sslength']
    while True:
        wcrt = compute_lhs_Eq4(task, HPTasks, vec_x, t, Q)
        if (wcrt > task['deadline']  # deadline miss
                or wcrt <= t):  # Eq 4 holds
            break
        t = wcrt  # increase t for next iteration

    return wcrt


def compute_vec_lin_approx(tasks, index):
    # Compute vector for linear approximation, using Equation 27
    vec_x = []
    sumU = 0
    for idx in range(index):
        itask = tasks[idx]  # task under consideration
        iutil = itask['execution']/itask['period']  # util
        sumU += iutil  # sum of utilizations

        # Compute lhs and rhs of Eq 27.
        lhs = iutil * (itask['wcrt_uniframework'] - itask['execution'])
        rhs = itask['sslength'] * sumU

        # Cases.
        if lhs > rhs:
            vec_x.append(1)
        else:
            vec_x.append(0)
    return vec_x


def vec_dominate_eq2(tasks, index):
    # Compute vector to dominate Equation 2 (suspension as release jitter)
    # Specified in Lemma 16.
    vec_x = []
    for idx in range(index):
        vec_x.append(0)
    return vec_x


def vec_dominate_eq3(tasks, index):
    # Compute vector to dominate Equation 3 (suspension as blocking)
    # Specified in Lemma 17, technical report proof.
    vec_x = []
    for idx in range(index):
        if tasks[idx]['sslength'] <= tasks[idx]['execution']:
            vec_x.append(1)
        else:
            vec_x.append(0)
    return vec_x


def UniFramework(tasks):
    # Schedulability test form the paper using the vector from eq 27 (linear
    # approximation) and the vectors to dominate Eq 2 and Eq 3.
    # Input: Tasks ordered by priority.
    for idx in range(len(tasks)):
        vec_lin = compute_vec_lin_approx(tasks, idx)
        vec2 = vec_dominate_eq2(tasks, idx)
        vec3 = vec_dominate_eq3(tasks, idx)

        wcrt_lin = compute_WCRT_bound(tasks[idx], tasks[:idx], vec_lin)
        wcrt2 = compute_WCRT_bound(tasks[idx], tasks[:idx], vec2)
        wcrt3 = compute_WCRT_bound(tasks[idx], tasks[:idx], vec3)

        wcrt = min(wcrt_lin, wcrt2, wcrt3)

        if wcrt > task['deadline']:  # deadline miss
            return False
        else:
            task['wcrt_uniframework'] = wcrt  # set wcrt
            continue
    return True
