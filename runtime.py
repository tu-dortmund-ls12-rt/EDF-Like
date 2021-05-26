from __future__ import division
from schedTest import tgPath, RI, RTEDF, UDLEDF, SCEDF, WLAEDF, Audsley, UniFramework, FP_Analyses
from effsstsPlot import effsstsPlot

import numpy as np
import os
import sys

import random

import time

from multiprocessing import Pool
from itertools import repeat


###
# Global preferences.
###

gTotBucket = 100  # total number of task sets per utilization
gTasksinBkt = 10  # tasks per set

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

plotallname = ''


# Plotting preferences.
gPlotdata = True  # flag to plot data
gPlotall = True
gPlotsingle = False
gPrefixdata = "effsstsPlot/Data/Runtime"  # path to store data


# Help function to plot results.
def plot_results(
        gPrefixdata, gPlotall, gSchemes, gMinsstype, gMaxsstype,
        gSSofftypes, gUStart, gUEnd, gUStep, gTasksinBkt, Ncol,
        gPlotsingle, plotallname):
    """ Plot the results.
    """
    if len(gSchemes) != 0:
        try:
            effsstsPlot.effsstsPlotRuntime(
                gPrefixdata, gPlotall, gSchemes, gMinsstype, gMaxsstype,
                gSSofftypes, gUStart, gUEnd, gUStep, gTasksinBkt, Ncol=Ncol,
                plotsingle=gPlotsingle, plotallname=plotallname)
        except Exception as e:
            return False
    else:
        MainWindow.statusBar().showMessage('There is no plot to draw.')
    return True


# if gPlotdata:
#     # If data can be used, plot directly.
#     if plot_results(
#             gPrefixdata, gPlotall, gSchemes, gMinsstype, gMaxsstype,
#             gSSofftypes, gUStart, gUEnd, gUStep, gTasksinBkt, Ncol,
#             gPlotsingle, plotallname) is True:
#         quit()


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

# breakpoint()

###
# Schedulability tests
###

# # --- bug testing
# for tasksets in tasksets_difutil:
#     for tasks in tasksets:
#         RI.set_prio(tasks, prio_policy=2)
#         if RI.RI_fixed(tasks, depth=RI_depth) != RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a):
#             breakpoint()
#     print('done')
# quit()
# # ---

def runtime_eval(ischeme, tasksets_difutil, num_processors):
    x = np.arange(gUStart, gUEnd+1, gUStep)
    print(x)
    y = np.zeros(int((gUEnd-gUStart) / gUStep) + 1)
    print(y)

    runtimes = []  # runtimes

    ifskip = False  # skip flag when 0 is reached

    # Iterate through taskset.
    for u, tasksets in enumerate(tasksets_difutil, start=0):
        print("Scheme:", ischeme, "Task-sets:", gTotBucket, "Tasks per set:",
              len(tasksets[0]), "U:", gUStart + u * gUStep, "SSLength:",
              str(gMinsstype), " - ", str(gMaxsstype))

        # if u == 0:  # utilization of 0 percent
        #     y[u] = 1
        #     continue
        # if u * gUStep == 100:  # utilization 100 percent
        #     y[u] = 0
        #     continue
        # if ifskip:  # skip iteration when flag is done
        #     print("acceptanceRatio:", 0)
        #     y[u] = 0
        #     continue

        # numfail = 0  # number of fails

        with Pool(num_processors) as p:
            runtimes_difutil = p.starmap(timing, zip(repeat(ischeme), tasksets))
        runtimes.extend(list(runtimes_difutil))  # add runtime values

        # acceptanceRatio = 1 - (numfail / len(tasksets))
        # print("acceptanceRatio:", acceptanceRatio)
        # y[u] = acceptanceRatio

    return runtimes


def timing(ischeme, tasks):
    start = time.time()  # start timer

    numfail = 0  # PEUDO - INITIALIZATION (we did not deal with removing it at all places)

    # --- 1 DM Evaluation. ---
    if ischeme == 'EL DM':  # RI scheduling
        RI.set_prio(tasks, prio_policy=2)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
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
    elif ischeme == 'EL EDF':  # RI scheduling
        RI.set_prio(tasks, prio_policy=3)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
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
        RI.set_prio(tasks, prio_policy=101, lam=0)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL EQDF lam=-1':
        RI.set_prio(tasks, prio_policy=101, lam=-1)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL EQDF lam=+1':
        RI.set_prio(tasks, prio_policy=101, lam=+1)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL EQDF any lam in [-10,10]':
        fail_flag = True
        for lam in [0] + list(range(-10, 11, 1)):  # lam range
            # (Testing 0 first gives results faster.)
            RI.set_prio(tasks, prio_policy=101, lam=lam)
            if RI.RI_fixed(tasks, depth=RI_depth) is True:
                fail_flag = False
                break
        if fail_flag:
            numfail += 1
    # --- 4 SAEDF Evaluation. ---
    elif ischeme == 'EL SAEDF lam=0':
        RI.set_prio(tasks, prio_policy=201, lam=0)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL SAEDF lam=-1':
        RI.set_prio(tasks, prio_policy=201, lam=-1)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL SAEDF lam=+1':
        RI.set_prio(tasks, prio_policy=201, lam=+1)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL SAEDF any lam in [-10,10]':
        fail_flag = True
        for lam in [0] + list(range(-10, 11, 1)):  # lam range
            # (Testing 0 first gives results faster.)
            RI.set_prio(tasks, prio_policy=201, lam=lam)
            if RI.RI_fixed(tasks, depth=RI_depth) is True:
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
        RI.set_prio(tasks, prio_policy=2)
        # Sched test.
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix DM D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix DM D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix DM D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    # --- 5b Arb deadline DM Evaluation. ---
    elif ischeme == 'EL-var DM D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        RI.set_prio(tasks, prio_policy=2)
        # Sched test.
        if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var DM D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var DM D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var DM D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        RI.set_prio(tasks, prio_policy=2)
        if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
            numfail += 1
    # --- 6a Arb deadline EDF Evaluation. ---
    elif ischeme == 'EL-fix EDF D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        RI.set_prio(tasks, prio_policy=3)
        # Sched test.
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix EDF D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix EDF D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    elif ischeme == 'EL-fix EDF D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        if RI.RI_fixed(tasks, depth=RI_depth) is False:
            numfail += 1
    # --- 6b Arb deadline EDF Evaluation. ---
    elif ischeme == 'EL-var EDF D1.0':
        # Set Deadlines.
        for itask in tasks:
            itask['deadline'] = 1.0 * itask['period']
        # Set priorities.
        RI.set_prio(tasks, prio_policy=3)
        # Sched test.
        if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var EDF D1.1':
        for itask in tasks:
            itask['deadline'] = 1.1 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var EDF D1.2':
        for itask in tasks:
            itask['deadline'] = 1.2 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
            numfail += 1
    elif ischeme == 'EL-var EDF D1.5':
        for itask in tasks:
            itask['deadline'] = 1.5 * itask['period']
        RI.set_prio(tasks, prio_policy=3)
        if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
            numfail += 1
    # --- Else. ---
    else:
        assert ischeme, 'not vaild ischeme'

    return time.time() - start



def store_results(ischeme, number_tasks, runtimes):
    # breakpoint()
    plotPath = (gPrefixdata)
    plotfile = (gPrefixdata + '/' + ischeme + str(number_tasks) + '_runtime')

    # Store results
    if not os.path.exists(plotPath):
        os.makedirs(plotPath)
    np.save(plotfile, runtimes)

# if gPlotdata:
#     # Plot data after Evaluation results.
#     if plot_results(
#             gPrefixdata, gPlotall, gSchemes, gMinsstype, gMaxsstype,
#             gSSofftypes, gUStart, gUEnd, gUStep, gTasksinBkt, Ncol,
#             gPlotsingle, plotallname) is True:
#         quit()

if __name__ == '__main__':

    # Schedulability tests to be run:
    scheme_flag_options = ['1']

    if len(sys.argv) == 1:
        print('Please provide additional argument to choose schedulability tests.')
        print('Please choose from:', scheme_flag_options)
        quit()

    scheme_flag = sys.argv[1]
    if scheme_flag == '1':
        # 1 EDF
        gSchemes = ['EL EDF', 'Our EMSoft', 'Liu and Anderson']
        plotallname = '1_runtime_edf'
    elif scheme_flag == '2':
        # 1 EDF
        gSchemes = ['EL EDF']
        plotallname = '2_runtime_edf'
    else:
        print('No valid argument. Please choose from:', scheme_flag_options)
        quit()

    # settings
    num_tasks_start = 10
    num_tasks_end = 210
    num_tasks_step = 10

    # # runtime tests
    # for number_tasks in range(num_tasks_start, num_tasks_end, num_tasks_step):
    #     tasksets_difutil = create_tasksets(number_tasks)
    #     for ischeme in gSchemes:
    #         runtimes = runtime_eval(ischeme, tasksets_difutil, 100)
    #         store_results(ischeme, number_tasks, runtimes)


    # plot
    effsstsPlot.effsstsPlotRuntime(
            gPrefixdata, gSchemes, num_tasks_start, num_tasks_end, num_tasks_step,
            Ncol=3, plotallname='runtime_eval_' + str(scheme_flag) + '_avg', method='avg', ylabel='Average Runtime (s)', show_legend=False)

    effsstsPlot.effsstsPlotRuntime(
            gPrefixdata, gSchemes, num_tasks_start, num_tasks_end, num_tasks_step,
            Ncol=3, plotallname='runtime_eval_' + str(scheme_flag) + '_max', method='max', ylabel='Maximal Runtime (s)', show_legend=False)
