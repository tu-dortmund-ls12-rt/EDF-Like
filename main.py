#!/usr/bin/env python3
"""This is the main file of our evaluation."""

from schedTest import tgPath  # Task generation from SSSEvaluation
from schedTest import RTEDF, UDLEDF, SCEDF, WLAEDF, UniFramework, FP_Analyses  # Analyses from SSSEvaluation
from schedTest import EL  # Our analysis
from effsstsPlot import effsstsPlot  # Plot function from SSSEvaluation

import numpy as np
import os
import random
from multiprocessing import Pool
from itertools import repeat
from argparse import ArgumentParser


# Help function to plot results.
def plot_results(
        gPrefixdata, gSchemes, gMinsstype, gMaxsstype,
        gSSofftypes, gUStart, gUEnd, gUStep, gTasksinBkt, Ncol, plotallname):
    """ Plot the results.
    """
    effsstsPlot.effsstsPlotAll(
        gPrefixdata, True, gSchemes, gMinsstype, gMaxsstype,
        gSSofftypes, gUStart, gUEnd, gUStep, gTasksinBkt, Ncol=Ncol,
        plotsingle=False, plotallname=plotallname)


def check(ischeme, tasks, EL_depth=None, EL_max_a=None):
    """Check function to apply multiprocessing."""
    numfail = 0
    # --- 1 DM Evaluation. ---
    if ischeme == 'EL DM':  # EL scheduling
        EL.set_prio(tasks, prio_policy=2)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'UniFramework':
        if UniFramework.UniFramework(tasks) is False:
            numfail += 1
    elif ischeme == 'SuspObl':
        if FP_Analyses.SuspObl(tasks) is False:
            numfail += 1
    elif ischeme == 'SuspJit':
        if FP_Analyses.SuspJit(tasks) is False:
            numfail += 1
    elif ischeme == 'SuspBlock':
        if FP_Analyses.SuspBlock(tasks) is False:
            numfail += 1
    # --- 2 EDF Evaluation. ---
    elif ischeme == 'EL EDF':  # EL scheduling
        EL.set_prio(tasks, prio_policy=3)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'Our EMSoft':  # Our EMSoft
        if RTEDF.RTEDF(tasks) is False:
            numfail += 1
    elif ischeme == 'Dong and Liu':
        if UDLEDF.UDLEDF(tasks) is False:
            numfail += 1
    elif ischeme == 'Liu and Anderson':
        if WLAEDF.WLAEDF(tasks) is False:
            numfail += 1
    elif ischeme == 'Susp as Comp':
        if SCEDF.SC_EDF(tasks) is False:
            numfail += 1
    # --- 3 EQDF Evaluation. ---
    elif ischeme == 'EL EQDF lam=0':
        EL.set_prio(tasks, prio_policy=101, lam=0)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL EQDF lam=-1':
        EL.set_prio(tasks, prio_policy=101, lam=-1)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL EQDF lam=+1':
        EL.set_prio(tasks, prio_policy=101, lam=+1)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL EQDF any lam in [-10,10]':
        fail_flag = True
        for lam in [0] + list(range(-10, 11, 1)):  # lam range
            # (Testing 0 first gives results faster.)
            EL.set_prio(tasks, prio_policy=101, lam=lam)
            if EL.EL_fixed(tasks, depth=EL_depth) is True:
                fail_flag = False
                break
        if fail_flag:
            numfail += 1
    # --- 4 SAEDF Evaluation. ---
    elif ischeme == 'EL SAEDF lam=0':
        EL.set_prio(tasks, prio_policy=201, lam=0)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL SAEDF lam=-1':
        EL.set_prio(tasks, prio_policy=201, lam=-1)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL SAEDF lam=+1':
        EL.set_prio(tasks, prio_policy=201, lam=+1)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL SAEDF any lam in [-10,10]':
        fail_flag = True
        for lam in [0] + list(range(-10, 11, 1)):  # lam range
            # (Testing 0 first gives results faster.)
            EL.set_prio(tasks, prio_policy=201, lam=lam)
            if EL.EL_fixed(tasks, depth=EL_depth) is True:
                fail_flag = False
                break
        if fail_flag:
            numfail += 1
    # --- 5a Arb deadline DM Evaluation. ---
    elif ischeme == 'EL-fix DM D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        EL.set_prio(tasks, prio_policy=2)
        # Sched test.
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix DM D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        EL.set_prio(tasks, prio_policy=2)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix DM D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        EL.set_prio(tasks, prio_policy=2)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix DM D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        EL.set_prio(tasks, prio_policy=2)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    # --- 5b Arb deadline DM Evaluation. ---
    elif ischeme == 'EL-var DM D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        EL.set_prio(tasks, prio_policy=2)
        # Sched test.
        if EL.EL_var(tasks, depth=EL_depth, max_a=EL_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var DM D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        EL.set_prio(tasks, prio_policy=2)
        if EL.EL_var(tasks, depth=EL_depth, max_a=EL_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var DM D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        EL.set_prio(tasks, prio_policy=2)
        if EL.EL_var(tasks, depth=EL_depth, max_a=EL_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var DM D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        EL.set_prio(tasks, prio_policy=2)
        if EL.EL_var(tasks, depth=EL_depth, max_a=EL_max_a) is False:
            numfail += 1
    # --- 6a Arb deadline EDF Evaluation. ---
    elif ischeme == 'EL-fix EDF D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        EL.set_prio(tasks, prio_policy=3)
        # Sched test.
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix EDF D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        EL.set_prio(tasks, prio_policy=3)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix EDF D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        EL.set_prio(tasks, prio_policy=3)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix EDF D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        EL.set_prio(tasks, prio_policy=3)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    # --- 6b Arb deadline EDF Evaluation. ---
    elif ischeme == 'EL-var EDF D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        EL.set_prio(tasks, prio_policy=3)
        # Sched test.
        if EL.EL_var(tasks, depth=EL_depth, max_a=EL_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var EDF D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        EL.set_prio(tasks, prio_policy=3)
        if EL.EL_var(tasks, depth=EL_depth, max_a=EL_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var EDF D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        EL.set_prio(tasks, prio_policy=3)
        if EL.EL_var(tasks, depth=EL_depth, max_a=EL_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var EDF D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        EL.set_prio(tasks, prio_policy=3)
        if EL.EL_var(tasks, depth=EL_depth, max_a=EL_max_a) is False:
            numfail += 1
    # --- Else. ---
    else:
        raise ValueError(f"{ischeme=} is not valid.")

    return numfail


if __name__ == '__main__':
    ###
    # Options
    ###
    parser = ArgumentParser()
    parser.add_argument("-q", "--quick", dest="quick", action="store_true", default=False,
                        help="Run only a small configuration to test that the program runs. Otherwise, the full evaluation is performed.")
    parser.add_argument("-p", "--processes", dest="proc", type=int,
                        help="Specify the number of concurrent processes.")
    parser.add_argument("scheme", help="Choose a scheme flag option from: [1, 2, 3, 4, 5a, 5b, 6a, 6b]")
    args = vars(parser.parse_args())

    ###
    # Global variables
    ###
    if args["quick"]:  # Quick setting to check if the program runs completely without Error.
        gTotBucket = 10  # total number of task sets per utilization
        gTasksinBkt = 3  # tasks per set

        gUStep = 50  # utilization step
        gUStart = 0  # utilization start
        gUEnd = 100  # utilization end

        # Share from period - wcet for self-suspension:
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length

        gSSofftypes = 0  # number of segments does not matter

        Ncol = 3  # number of columns in Legend

        EL_depth = 2  # depth for EL schedulability test
        EL_max_a = 2  # maximal a for EL schedulability test

        num_processors = 6  # number of processors for the evaluation

    else:  # Full evaluation.
        gTotBucket = 500  # total number of task sets per utilization
        gTasksinBkt = 50  # tasks per set

        gUStep = 5  # utilization step
        gUStart = 0  # utilization start
        gUEnd = 100  # utilization end

        # Share from period - wcet for self-suspension:
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length

        gSSofftypes = 0  # number of segments does not matter

        Ncol = 3  # number of columns in Legend

        EL_depth = 5  # depth for EL schedulability test
        EL_max_a = 10  # maximal a for EL schedulability test

        num_processors = 100  # number of processors for the evaluation

    # Further plotting preferences.
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
        # 1 DM Evaluation.
        gSchemes = ['EL DM', 'UniFramework', 'SuspJit', 'SuspBlock', 'SuspObl']
        plotallname = '1_dm'
    elif scheme_flag == '2':
        # 2 EDF Evaluation.
        gSchemes = ['EL EDF', 'Our EMSoft', 'Liu and Anderson',
                    'Susp as Comp']
        plotallname = '2_edf'
    elif scheme_flag == '3':
        # 3 EQDF Evaluation.
        gSchemes = ['EL EQDF lam=-1', 'EL EQDF lam=0', 'EL EQDF lam=+1',
                    'EL EQDF any lam in [-10,10]']
        Ncol = 2
        plotallname = '3_eqdf'
    elif scheme_flag == '4':
        # 4 SAEDF Evaluation.
        gSchemes = ['EL SAEDF lam=-1', 'EL SAEDF lam=0', 'EL SAEDF lam=+1',
                    'EL SAEDF any lam in [-10,10]']
        Ncol = 2
        plotallname = '4_saedf'
    elif scheme_flag == '5a':
        # 5a Arb deadline DM Evaluation.
        gSchemes = ['EL-fix DM D1.0', 'EL-fix DM D1.1', 'EL-fix DM D1.2',
                    'EL-fix DM D1.5']
        Ncol = 2
        plotallname = '5a_arb_dl_dm'
    elif scheme_flag == '5b':
        # 5b Arb deadline DM Evaluation.
        gSchemes = ['EL-var DM D1.0', 'EL-var DM D1.1', 'EL-var DM D1.2',
                    'EL-var DM D1.5']
        Ncol = 2
        plotallname = '5b_arb_dl_dm'
    elif scheme_flag == '6a':
        # 6a Arb deadline EDF Evaluation.
        gSchemes = ['EL-fix EDF D1.0', 'EL-fix EDF D1.1', 'EL-fix EDF D1.2',
                    'EL-fix EDF D1.5']
        Ncol = 2
        plotallname = '6a_arb_dl_edf'
    elif scheme_flag == '6b':
        # 6b Arb deadline EDF Evaluation.
        gSchemes = ['EL-var EDF D1.0', 'EL-var EDF D1.1', 'EL-var EDF D1.2',
                    'EL-var EDF D1.5']
        Ncol = 2
        plotallname = '6b_arb_dl_edf'
    else:
        raise ValueError(f'{scheme_flag=} is no valid argument.')

    ###
    # Create Task sets
    ###
    random.seed(331)  # Get same task sets for each plot.

    tasksets_difutil = []  # task set differentiated by utilization

    for u in range(gUStart, gUEnd, gUStep):
        tasksets = []
        for i in range(0, gTotBucket, 1):
            percentageU = u / 100
            # Create task set with predefined parameters.
            tasks = tgPath.taskGeneration_p(gTasksinBkt, percentageU, gMinsstype,
                                            gMaxsstype, vRatio=1,
                                            numLog=int(2))
            # Sort tasks by period.
            sortedTasks = sorted(tasks, key=lambda item: item['period'])
            tasksets.append(sortedTasks)  # add
            for itask in tasks:
                if itask['period'] != itask['deadline']:
                    print('period and deadline are different')
                    breakpoint()
        tasksets_difutil.append(tasksets)  # add

    ###
    # Schedulability tests
    ###
    for ischeme in gSchemes:
        x = np.arange(gUStart, gUEnd + 1, gUStep)
        print(x)
        y = np.zeros(int((gUEnd - gUStart) / gUStep) + 1)
        print(y)

        ifskip = False  # skip flag when 0 is reached

        # Iterate through taskset.
        for u, tasksets in enumerate(tasksets_difutil, start=0):
            print("Scheme:", ischeme, "Task-sets:", gTotBucket, "Tasks per set:",
                  gTasksinBkt, "U:", gUStart + u * gUStep, "SSLength:",
                  str(gMinsstype), " - ", str(gMaxsstype))
            if u == 0:  # utilization of 0 percent
                y[u] = 1
                continue
            if u * gUStep == 100:  # utilization 100 percent
                y[u] = 0
                continue
            if ifskip:  # skip iteration when flag is done
                print("acceptanceRatio:", 0)
                y[u] = 0
                continue

            with Pool(num_processors) as p:  # Use several processes and apply the check function.
                fails = p.starmap(check, zip(repeat(ischeme), tasksets, repeat(EL_depth), repeat(EL_max_a)))
            numfail = sum(fails)  # total number of fails

            acceptanceRatio = 1 - (numfail / len(tasksets))
            print("acceptanceRatio:", acceptanceRatio)
            y[u] = acceptanceRatio
            # if acceptanceRatio == 0:
            #     ifskip = True

        # Store results
        plotPath = (gPrefixdata + '/' + str(gMinsstype) + '-' + str(gMaxsstype)
                    + '/' + str(gSSofftypes) + '/')
        plotfile = (gPrefixdata + '/' + str(gMinsstype) + '-' + str(gMaxsstype)
                    + '/' + str(gSSofftypes) + '/' + ischeme + str(gTasksinBkt))

        if not os.path.exists(plotPath):
            os.makedirs(plotPath)
        np.save(plotfile, np.array([x, y]))

    ###
    # Plot.
    ###
    plot_results(gPrefixdata, gSchemes, gMinsstype, gMaxsstype, gSSofftypes, gUStart, gUEnd, gUStep, gTasksinBkt, Ncol,
                 plotallname)
