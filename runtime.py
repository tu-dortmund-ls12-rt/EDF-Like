#!/usr/bin/env python3
"""This is file is to evaluate the runtime of our approach."""

from schedTest import tgPath  # Task generation from SSSEvaluation
from schedTest import RTEDF, UDLEDF, SCEDF, WLAEDF, UniFramework, FP_Analyses  # Analyses from SSSEvaluation
from schedTest import RI  # Our analysis
from effsstsPlot import effsstsPlot  # Plot function from SSSEvaluation

# other packages
import numpy as np
import os
import random
import time
from itertools import repeat
from multiprocessing import Pool  # multiprocessing
from argparse import ArgumentParser


# def plot_results(
#         gPrefixdata, gSchemes, gMinsstype, gMaxsstype,
#         gSSofftypes, gUStart, gUEnd, gUStep, gTasksinBkt, Ncol, plotallname):
#     """ Plot the results.
#     """
#     if len(gSchemes) != 0:
#         try:
#             effsstsPlot.effsstsPlotRuntime(
#                 gPrefixdata, True, gSchemes, gMinsstype, gMaxsstype,
#                 gSSofftypes, gUStart, gUEnd, gUStep, gTasksinBkt, Ncol=Ncol,
#                 plotsingle=False, plotallname=plotallname)
#         except Exception as e:
#             return False
#     else:
#         MainWindow.statusBar().showMessage('There is no plot to draw.')
#     return True


def create_tasksets(number_tasks):
    ###
    # Create Task sets
    ###
    random.seed(331)  # same task sets for each plot

    tasksets_difutil = []  # task set differentiated by utilization

    for u in range(gUStart, gUEnd, gUStep):
        tasksets = []
        for i in range(0, gTotBucket, 1):
            percentageU = u / 100
            # Create task set with predefined parameters.
            tasks = tgPath.taskGeneration_p(
                number_tasks, percentageU, gMinsstype,
                gMaxsstype, vRatio=1, numLog=int(2))
            # Sort tasks by period.
            sortedTasks = sorted(tasks, key=lambda item: item['period'])
            tasksets.append(sortedTasks)  # add
            for itask in tasks:
                if itask['period'] != itask['deadline']:
                    print('period and deadline are different')
                    breakpoint()
        tasksets_difutil.append(tasksets)  # add

    return tasksets_difutil


def runtime_eval(ischeme, tasksets_difutil, num_processors, RI_depth=None, RI_max_a=None):
    x = np.arange(gUStart, gUEnd + 1, gUStep)
    print(x)
    y = np.zeros(int((gUEnd - gUStart) / gUStep) + 1)
    print(y)

    runtimes = []  # runtimes

    ifskip = False  # skip flag when 0 is reached

    # Iterate through taskset.
    for u, tasksets in enumerate(tasksets_difutil, start=0):
        print("Scheme:", ischeme, "Task-sets:", gTotBucket, "Tasks per set:",
              len(tasksets[0]), "U:", gUStart + u * gUStep, "SSLength:",
              str(gMinsstype), " - ", str(gMaxsstype))

        with Pool(num_processors) as p:
            runtimes_difutil = p.starmap(timing, zip(repeat(ischeme), tasksets, repeat(RI_depth), repeat(RI_max_a)))
        runtimes.extend(list(runtimes_difutil))  # add runtime values

    return runtimes


def timing(ischeme, tasks, RI_depth=None, RI_max_a=None):
    """Return the time it takes to run the schedulability test ischeme once for tasks."""
    start = time.time()  # start timer

    # --- 1 DM Evaluation. ---
    if ischeme == 'EL DM':  # RI scheduling
        RI.set_prio(tasks, prio_policy=2)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'UniFramework':
        UniFramework.UniFramework(tasks)
    elif ischeme == 'SuspObl':
        FP_Analyses.SuspObl(tasks)
    elif ischeme == 'SuspJit':
        FP_Analyses.SuspJit(tasks)
    elif ischeme == 'SuspBlock':
        FP_Analyses.SuspBlock(tasks)
    # --- 2 EDF Evaluation. ---
    elif ischeme == 'EL EDF':  # RI scheduling
        RI.set_prio(tasks, prio_policy=3)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'Our EMSoft':  # Our EMSoft
        RTEDF.RTEDF(tasks)
    elif ischeme == 'Dong and Liu':
        UDLEDF.UDLEDF(tasks)
    elif ischeme == 'Liu and Anderson':
        WLAEDF.WLAEDF(tasks)
    elif ischeme == 'Susp as Comp':
        SCEDF.SC_EDF(tasks)
    # --- 3 EQDF Evaluation. ---
    elif ischeme == 'EL EQDF lam=0':
        RI.set_prio(tasks, prio_policy=101, lam=0)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL EQDF lam=-1':
        RI.set_prio(tasks, prio_policy=101, lam=-1)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL EQDF lam=+1':
        RI.set_prio(tasks, prio_policy=101, lam=+1)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL EQDF any lam in [-10,10]':
        for lam in [0] + list(range(-10, 11, 1)):  # lam range
            # (Testing 0 first gives results faster.)
            RI.set_prio(tasks, prio_policy=101, lam=lam)
            if RI.RI_fixed(tasks, depth=RI_depth) is True:
                break
    # --- 4 SAEDF Evaluation. ---
    elif ischeme == 'EL SAEDF lam=0':
        RI.set_prio(tasks, prio_policy=201, lam=0)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL SAEDF lam=-1':
        RI.set_prio(tasks, prio_policy=201, lam=-1)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL SAEDF lam=+1':
        RI.set_prio(tasks, prio_policy=201, lam=+1)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL SAEDF any lam in [-10,10]':
        for lam in [0] + list(range(-10, 11, 1)):  # lam range
            # (Testing 0 first gives results faster.)
            RI.set_prio(tasks, prio_policy=201, lam=lam)
            if RI.RI_fixed(tasks, depth=RI_depth) is True:
                break
    # --- 5a Arb deadline DM Evaluation. ---
    elif ischeme == 'EL-fix DM D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        RI.set_prio(tasks, prio_policy=2)
        # Sched test.
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL-fix DM D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL-fix DM D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL-fix DM D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        RI.RI_fixed(tasks, depth=RI_depth)
    # --- 5b Arb deadline DM Evaluation. ---
    elif ischeme == 'EL-var DM D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        RI.set_prio(tasks, prio_policy=2)
        # Sched test.
        RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a)
    elif ischeme == 'EL-var DM D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a)
    elif ischeme == 'EL-var DM D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a)
    elif ischeme == 'EL-var DM D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a)
    # --- 6a Arb deadline EDF Evaluation. ---
    elif ischeme == 'EL-fix EDF D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        RI.set_prio(tasks, prio_policy=3)
        # Sched test.
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL-fix EDF D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL-fix EDF D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        RI.RI_fixed(tasks, depth=RI_depth)
    elif ischeme == 'EL-fix EDF D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        RI.RI_fixed(tasks, depth=RI_depth)
    # --- 6b Arb deadline EDF Evaluation. ---
    elif ischeme == 'EL-var EDF D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        RI.set_prio(tasks, prio_policy=3)
        # Sched test.
        RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a)
    elif ischeme == 'EL-var EDF D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a)
    elif ischeme == 'EL-var EDF D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a)
    elif ischeme == 'EL-var EDF D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a)
    # --- Else. ---
    else:
        raise ValueError(f"{ischeme=} is not valid.")

    return time.time() - start


def store_results(ischeme, number_tasks, runtimes):
    # breakpoint()
    plotPath = (gPrefixdata)
    plotfile = (gPrefixdata + '/Runtime/' + ischeme + str(number_tasks) + '_runtime')

    # Store results
    if not os.path.exists(plotPath):
        os.makedirs(plotPath)
    np.save(plotfile, runtimes)


if __name__ == '__main__':
    ###
    # Options
    ###
    parser = ArgumentParser()
    parser.add_argument("-q", "--quick", dest="quick", action="store_true", default=False,
                        help="Run only a small configuration to test that the program runs. Otherwise, the full evaluation is performed.")
    parser.add_argument("-p", "--processes", dest="proc", type=int,
                        help="Specify the number of concurrent processes.")
    parser.add_argument("scheme", help="Choose a scheme flag option from: [1]")
    args = vars(parser.parse_args())

    ###
    # Global preferences.
    ###
    if args["quick"]:  # Quick setting to check if the program runs completely without Error.
        gTotBucket = 10  # total number of task sets per utilization

        # number of tasks
        num_tasks_start = 10
        num_tasks_end = 210
        num_tasks_step = 95

        gUStep = 50  # utilization step
        gUStart = 0  # utilization start
        gUEnd = 100  # utilization end

        # Share from period - wcet for self-suspension:
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length

        gSSofftypes = 0  # number of segments does not matter

        Ncol = 3  # number of columns in Legend

        RI_depth = 2  # depth for EL schedulability test
        RI_max_a = 2  # maximal a for EL schedulability test

        num_processors = 6  # number of processors for the evaluation
    else:  # Full evaluation.
        gTotBucket = 100  # total number of task sets per utilization

        # number of tasks
        num_tasks_start = 10
        num_tasks_end = 210
        num_tasks_step = 10

        gUStep = 10  # utilization step
        gUStart = 0  # utilization start
        gUEnd = 100  # utilization end

        # Share from period - wcet for self-suspension:
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length

        gSSofftypes = 0  # number of segments does not matter

        Ncol = 3  # number of columns in Legend

        RI_depth = 5  # depth for EL schedulability test
        RI_max_a = 10  # maximal a for EL schedulability test

        num_processors = 100  # number of processors for the evaluation

    # Further plotting preferences
    gPrefixdata = "effsstsPlot/Data"  # path to store data

    # Modify the number of processes
    if args["proc"] is not None and args["proc"] > 0:
        num_processors = args["proc"]

    # Set the scheme flag.
    scheme_flag = args["scheme"]

    ###
    # Choose schedulability tests to be run + assign corresponding gSchemes and plotallname:
    ###
    plotallname = ''
    if scheme_flag == '1':
        # 1 EDF
        gSchemes = ['EL EDF', 'Our EMSoft', 'Liu and Anderson']
        plotallname = '1_runtime_edf'
    else:
        raise ValueError(f'{scheme_flag=} is no valid argument.')

    ###
    # Runtime tests.
    ###
    for number_tasks in range(num_tasks_start, num_tasks_end, num_tasks_step):
        # Create tasksets.
        tasksets_difutil = create_tasksets(number_tasks)
        # Do the tests + measure the runtime.
        for ischeme in gSchemes:
            runtimes = runtime_eval(ischeme, tasksets_difutil, num_processors, RI_depth=RI_depth, RI_max_a=RI_max_a)
            store_results(ischeme, number_tasks, runtimes)

    ###
    # Plot.
    ###
    effsstsPlot.effsstsPlotRuntime(
        gPrefixdata, gSchemes, num_tasks_start, num_tasks_end, num_tasks_step,
        Ncol=3, plotallname='runtime_eval_' + str(scheme_flag) + '_avg', method='avg', ylabel='Average Runtime (s)',
        show_legend=False)

    effsstsPlot.effsstsPlotRuntime(
        gPrefixdata, gSchemes, num_tasks_start, num_tasks_end, num_tasks_step,
        Ncol=3, plotallname='runtime_eval_' + str(scheme_flag) + '_max', method='max', ylabel='Maximal Runtime (s)',
        show_legend=False)
