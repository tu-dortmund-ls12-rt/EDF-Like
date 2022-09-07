from schedTest import GUC21
from schedTest import EL
from schedTest import tgPath as create

import numpy as np
import os
import sys
import random
import itertools
from itertools import repeat
from multiprocessing import Pool

from effsstsPlot import effsstsPlot as plot

random.seed(331)  # set seed to have same task sets for each plot


def store_results(results, path, filename):
    file = os.path.join(path, filename)
    if not os.path.exists(path):
        os.makedirs(path)
    np.save(file, results)


def load_results(path, filename):
    file = os.path.join(path, filename)
    results = np.load(file, allow_pickle=True)
    return results


def create_tasksets(
        UStart,  # start of utilization
        UEnd,  # end of utilization
        UStep,  # utilization step
        TasksinBkt,  # tasks per set
        TotBucket,  # number of task sets per utilization
        Minsstype,  # minimal ratio of self-suspension
        Maxsstype,  # maximal ratio of self-suspension
):
    """Create tasksets according to description."""
    tasksets_difutil = []  # task set differentiated by utilization

    for u in range(UStart, UEnd + UStep, UStep):
        tasksets = []
        for i in range(0, TotBucket, 1):
            percentageU = u / 100
            # Create task set with predefined parameters.
            tasks = create.taskGeneration_p(
                TasksinBkt, percentageU, Minsstype, Maxsstype, vRatio=1, numLog=int(2))
            # Sort tasks by period.
            sortedTasks = sorted(tasks, key=lambda item: item['period'])
            tasksets.append(sortedTasks)  # add
            for itask in tasks:
                if itask['period'] != itask['deadline']:
                    print('period and deadline are different')
                    # breakpoint()
        tasksets_difutil.append(tasksets)  # add

    return tasksets_difutil


def test_scheme(gScheme, tasksets_difutil, multiproc=0):
    """Test a scheme for all tasksets in tasksets_difutil"""
    print('Scheme:', gScheme)
    results = []
    for tasksets in tasksets_difutil:  # tasksets are aggregated like this
        acceptance = []
        if multiproc == 0:  # without multiprocessing
            for taskset in tasksets:
                acceptance.append(_test_scheme(gScheme, taskset))
        else:  # with multiprocessing
            with Pool(multiproc) as p:
                acceptance = p.starmap(
                    _test_scheme, zip(repeat(gScheme), tasksets))
        results.append(sum(acceptance) / len(tasksets))

    return results


def _test_scheme(gScheme, taskset):
    # Choose correct scheme
    if gScheme == 'FP':  # this is used
        # set arrival curves
        arr_curves = [GUC21.arr_sporadic(task['period']) for task in taskset]
        # do test
        return GUC21.sched_test(taskset, arr_curves, choose_xvec='comb3')

    elif gScheme == 'EL-fixed':
        EL.set_prio(taskset, prio_policy=2)
        return EL.RI_fixed(taskset)
    elif gScheme == 'EL-var':
        EL.set_prio(taskset, prio_policy=2)
        return EL.RI_var(taskset, max_a=10)

    else:
        return False


def _set_deadlines(taskset, param):
    for tsk in taskset:
        tsk['deadline'] = tsk['period'] * param


def _make_jitter_tasks(taskset, jit):
    tasksetJ = [dict(tsk) for tsk in taskset]
    for tsk in tasksetJ:
        tsk['period'] *= (1 - jit)
    return tasksetJ


def _constrained_tasks(taskset):
    tasksetJ = [dict(tsk) for tsk in taskset]
    for tsk in tasksetJ:
        tsk['deadline'] = min(tsk['deadline'], tsk['period'])
    return tasksetJ


if __name__ == '__main__':

    # Input check
    if len(sys.argv) < 3:
        print('Please provide additional arguments.')
        print('1st:  0:sched test + plot, 1: plot only')
        print('2nd:  argument to choose schedulability test')
        quit()

    # Settings
    gTotBucket = 200  # total number of task sets per utilization
    gTasksinBkt = 50  # tasks per set

    gUStart = 0  # utilization start
    gUEnd = 100  # utilization end
    gUStep = 5  # utilization step

    # Share from period - wcet for self-suspension:
    gMaxsstype = 0.5  # maximal total self-suspension length
    gMinsstype = 0.0  # minimal total self-suspension length

    gSSofftypes = 0  # number of segments does not matter

    deadline_stretch = [0.8, 1.2]

    Ncol = 3  # number of columns in Legend
    datapath = 'data'
    plotpath = 'plot'
    plotname = ' '  # name for plots, to be changed when choosing schedulability tests

    gMultiproc = 100  # number of concurrent threads

    #####
    # === Try-out settings: ===
    gTotBucket = 100
    gTasksinBkt = 20
    gMultiproc = 0
    #####

    # Choose schedulability tests
    scheme_flag = sys.argv[2]

    # ==Show that Heuristic is useful==
    ##### Comparison #####
    if scheme_flag == '401':
        gSchemes = ['FP', 'EL-fixed', 'EL-var']
        plotname = '401'
        gTotBucket = 200  # total number of task sets per utilization
        gMaxsstype = 0.3  # maximal total self-suspension length
        gMinsstype = 0.1  # minimal total self-suspension length
        deadline_stretch = [1.0, 1.2]
    elif scheme_flag == '402':
        gSchemes = ['FP', 'EL-fixed', 'EL-var']
        plotname = '402'
        gTotBucket = 200  # total number of task sets per utilization
        gMaxsstype = 0.3  # maximal total self-suspension length
        gMinsstype = 0.1  # minimal total self-suspension length
        deadline_stretch = [0.8, 1.2]

    # == ELSE ==
    else:
        print('second input argument not valid')
        quit()

    # Create task sets
    tasksets_difutil = create_tasksets(
        gUStart, gUEnd, gUStep, gTasksinBkt, gTotBucket, gMinsstype, gMaxsstype)

    # Deadline stretch
    if deadline_stretch != [1, 1]:
        for tsksets in tasksets_difutil:
            for tskset in tsksets:
                for tsk in tskset:
                    mult = random.uniform(*deadline_stretch)
                    tsk['deadline'] = tsk['period'] * mult

    # Sort by deadline
    for tsksets in tasksets_difutil:
        for tskset in tsksets:
            tskset.sort(key=lambda x: x['deadline'])

    # Schedulability test + store results
    for gScheme in gSchemes:
        # test
        results = list(zip(itertools.count(start=gUStart, step=gUStep),
                           test_scheme(gScheme, tasksets_difutil, multiproc=gMultiproc)))
        print(list(results))
        # store results
        store_results(results, datapath, gScheme + '.npy')

    # plot results
    results_plot = [load_results(datapath, gScheme + '.npy')
                    for gScheme in gSchemes]

    plot.plot_comparison(gSchemes, results_plot, plotpath, plotname, Ncol)
