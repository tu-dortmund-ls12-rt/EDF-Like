from argparse import ArgumentParser

from schedTest import GUC21
from schedTest import EL
from schedTest import tgPath as create

import numpy as np
import os
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
        return EL.EL_fixed(taskset)
    elif gScheme == 'EL-var':
        EL.set_prio(taskset, prio_policy=2)
        return EL.EL_var(taskset, max_a=10)

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
    ###
    # Options
    ###
    parser = ArgumentParser()
    parser.add_argument("-q", "--quick", dest="quick", action="store_true", default=False,
                        help="Run only a small configuration to test that the program runs. Otherwise, the full evaluation is performed.")
    parser.add_argument("-p", "--processes", dest="proc", type=int,
                        help="Specify the number of concurrent processes.")
    parser.add_argument("scheme", help="Choose a scheme flag option from: [1, 2]")
    args = vars(parser.parse_args())

    ###
    # Global variables
    ###
    if args["quick"]:  # Quick setting to check if the program runs completely without Error.
        gTotBucket = 10  # total number of task sets per utilization
        gTasksinBkt = 10  # tasks per set

        gUStart = 0  # utilization start
        gUEnd = 100  # utilization end
        gUStep = 50  # utilization step

        gMultiproc = 6  # number of concurrent threads

    else:  # Full evaluation.
        gTotBucket = 200  # total number of task sets per utilization
        gTasksinBkt = 50  # tasks per set

        gUStart = 0  # utilization start
        gUEnd = 100  # utilization end
        gUStep = 5  # utilization step

        gMultiproc = 100  # number of concurrent threads

    # Share from period - wcet for self-suspension:
    gMaxsstype = 0.5  # maximal total self-suspension length # TODO 0.3?
    gMinsstype = 0.0  # minimal total self-suspension length # TODO 0.1?

    gSSofftypes = 0  # number of segments does not matter

    # Further plotting preferences.
    Ncol = 3  # number of columns in Legend
    datapath = 'effsstsPlot/Data/Comparison'
    plotpath = 'effsstsPlot/Data'
    plotname = ''  # name for plots, to be changed when choosing schedulability tests

    # Choose schedulability tests
    scheme_flag = args["scheme"]

    ###
    # Choose schedulability tests to be run + assign corresponding gSchemes and plotallname:
    ###
    if scheme_flag == '1':
        gSchemes = ['FP', 'EL-fixed', 'EL-var']
        plotname = 'comparison_arb_DL_FP_1.0-1.2'
        deadline_stretch = [1.0, 1.2]
    elif scheme_flag == '2':
        gSchemes = ['FP', 'EL-fixed', 'EL-var']
        plotname = 'comparison_arb_DL_FP_0.8-1.2'
        deadline_stretch = [0.8, 1.2]

    else:
        raise ValueError(f'{scheme_flag=} is no valid argument.')

    ###
    # Create Task sets
    ###
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

    ###
    # Schedulability tests
    ###
    for gScheme in gSchemes:
        # test
        results = list(zip(itertools.count(start=gUStart, step=gUStep),
                           test_scheme(gScheme, tasksets_difutil, multiproc=gMultiproc)))
        print(list(results))
        # store results
        store_results(results, datapath, gScheme + '.npy')

    ###
    # Plot.
    ###
    results_plot = [load_results(datapath, gScheme + '.npy')
                    for gScheme in gSchemes]

    plot.plot_comparison(gSchemes, results_plot, plotpath, plotname, Ncol)
