from __future__ import division
from schedTest import tgPath, RI, RTEDF, UDLEDF, SCEDF, WLAEDF, Audsley, UniFramework, FP_Analyses
from effsstsPlot import effsstsPlot

import numpy as np
import os
import sys

import random


###
# global preferences
###

gTotBucket = 500  # total number of task sets per utilization
gTasksinBkt = 10  # tasks per set

gUStep = 1  # utilization step
gUStart = 0  # utilization start
gUEnd = 100  # utilization end

# share from period - wcet for self-suspension:
gMaxsstype = 0.5  # maximal total self-suspension length
gMinsstype = 0.0  # minimal total self-suspension length

gSSofftypes = 0  # number of segments does not matter

Ncol = 3  # number of columns in Legend

RI_depth = 5  # depth for RI schedulability test
RI_max_a = 10  # maximal a for RI schedulability test

plotallname = ''

# Schedulability tests to be run:
scheme_flag_options = ['1', '2', '3', '4', '5a', '5b', '6a', '6b']

if len(sys.argv) == 1:
    print('Please provide additional argument to choose schedulability tests.')
    print('Please choose from:', scheme_flag_options)
    quit()

scheme_flag = sys.argv[1]
if scheme_flag == '1':
    # 1 DM Evaluation.
    gSchemes = ['RI DM', 'UniFramework', 'SuspJit', 'SuspBlock', 'SuspObl']
    plotallname = '1_dm'
elif scheme_flag == '2':
    # 2 EDF Evaluation.
    gSchemes = ['RI EDF', 'Our EMSoft', 'Dong and Liu', 'Liu and Anderson',
                'Susp as Comp']
    plotallname = '2_edf'
elif scheme_flag == '3':
    # 3 EQDF Evaluation.
    gSchemes = ['RI EQDF lam=-1', 'RI EQDF lam=0', 'RI EQDF lam=+1',
                'RI EQDF any lam in [-10,10]']
    Ncol = 2
    plotallname = '3_eqdf'
elif scheme_flag == '4':
    # 4 SAEDF Evaluation.
    gSchemes = ['RI SAEDF lam=-1', 'RI SAEDF lam=0', 'RI SAEDF lam=+1',
                'RI SAEDF any lam in [-10,10]']
    Ncol = 2
    plotallname = '4_saedf'
elif scheme_flag == '5a':
    # 5a Arb deadline DM Evaluation.
    gSchemes = ['RI-fix DM D1.0', 'RI-fix DM D1.1', 'RI-fix DM D1.2',
                'RI-fix DM D1.5']
    Ncol = 2
    plotallname = '5a_arb_dl_dm'
elif scheme_flag == '5b':
    # 5b Arb deadline DM Evaluation.
    gSchemes = ['RI-var DM D1.0', 'RI-var DM D1.1', 'RI-var DM D1.2',
                'RI-var DM D1.5']
    Ncol = 2
    plotallname = '5b_arb_dl_dm'
elif scheme_flag == '6a':
    # 6a Arb deadline EDF Evaluation.
    gSchemes = ['RI-fix EDF D1.0', 'RI-fix EDF D1.1', 'RI-fix EDF D1.2',
                'RI-fix EDF D1.5']
    Ncol = 2
    plotallname = '6a_arb_dl_edf'
elif scheme_flag == '6b':
    # 6b Arb deadline EDF Evaluation.
    gSchemes = ['RI-var EDF D1.0', 'RI-var EDF D1.1', 'RI-var EDF D1.2',
                'RI-var EDF D1.5']
    Ncol = 2
    plotallname = '6b_arb_dl_edf'
else:
    print('No valid argument. Please choose from:', scheme_flag_options)
    quit()


gPlotdata = True  # flag to plot data

gPrefixdata = "effsstsPlot/Data"  # path to store data

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

# Iterate though schedulability tests
for ischeme in gSchemes:
    x = np.arange(gUStart, gUEnd+1, gUStep)
    print(x)
    y = np.zeros(int((gUEnd-gUStart) / gUStep) + 1)
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

        numfail = 0  # number of fails
        for tasks in tasksets:  # iterate over each taskset
            # --- 1 DM Evaluation. ---
            if ischeme == 'RI DM':  # RI scheduling
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
            elif ischeme == 'RI EDF':  # RI scheduling
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
            elif ischeme == 'RI EQDF lam=0':
                RI.set_prio(tasks, prio_policy=101, lam=0)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI EQDF lam=-1':
                RI.set_prio(tasks, prio_policy=101, lam=-1)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI EQDF lam=+1':
                RI.set_prio(tasks, prio_policy=101, lam=+1)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI EQDF any lam in [-10,10]':
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
            elif ischeme == 'RI SAEDF lam=0':
                RI.set_prio(tasks, prio_policy=201, lam=0)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI SAEDF lam=-1':
                RI.set_prio(tasks, prio_policy=201, lam=-1)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI SAEDF lam=+1':
                RI.set_prio(tasks, prio_policy=201, lam=+1)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI SAEDF any lam in [-10,10]':
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
            elif ischeme == 'RI-fix DM D1.0':
                # Set Deadlines.
                for itask in tasks:
                    itask['deadline'] = 1.0 * itask['period']
                # Set priorities.
                RI.set_prio(tasks, prio_policy=2)
                # Sched test.
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI-fix DM D1.1':
                for itask in tasks:
                    itask['deadline'] = 1.1 * itask['period']
                RI.set_prio(tasks, prio_policy=2)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI-fix DM D1.2':
                for itask in tasks:
                    itask['deadline'] = 1.2 * itask['period']
                RI.set_prio(tasks, prio_policy=2)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI-fix DM D1.5':
                for itask in tasks:
                    itask['deadline'] = 1.5 * itask['period']
                RI.set_prio(tasks, prio_policy=2)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            # --- 5b Arb deadline DM Evaluation. ---
            elif ischeme == 'RI-var DM D1.0':
                # Set Deadlines.
                for itask in tasks:
                    itask['deadline'] = 1.0 * itask['period']
                # Set priorities.
                RI.set_prio(tasks, prio_policy=2)
                # Sched test.
                if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
                    numfail += 1
            elif ischeme == 'RI-var DM D1.1':
                for itask in tasks:
                    itask['deadline'] = 1.1 * itask['period']
                RI.set_prio(tasks, prio_policy=2)
                if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
                    numfail += 1
            elif ischeme == 'RI-var DM D1.2':
                for itask in tasks:
                    itask['deadline'] = 1.2 * itask['period']
                RI.set_prio(tasks, prio_policy=2)
                if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
                    numfail += 1
            elif ischeme == 'RI-var DM D1.5':
                for itask in tasks:
                    itask['deadline'] = 1.5 * itask['period']
                RI.set_prio(tasks, prio_policy=2)
                if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
                    numfail += 1
            # --- 6a Arb deadline EDF Evaluation. ---
            elif ischeme == 'RI-fix EDF D1.0':
                # Set Deadlines.
                for itask in tasks:
                    itask['deadline'] = 1.0 * itask['period']
                # Set priorities.
                RI.set_prio(tasks, prio_policy=3)
                # Sched test.
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI-fix EDF D1.1':
                for itask in tasks:
                    itask['deadline'] = 1.1 * itask['period']
                RI.set_prio(tasks, prio_policy=3)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI-fix EDF D1.2':
                for itask in tasks:
                    itask['deadline'] = 1.2 * itask['period']
                RI.set_prio(tasks, prio_policy=3)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            elif ischeme == 'RI-fix EDF D1.5':
                for itask in tasks:
                    itask['deadline'] = 1.5 * itask['period']
                RI.set_prio(tasks, prio_policy=3)
                if RI.RI_fixed(tasks, depth=RI_depth) is False:
                    numfail += 1
            # --- 6b Arb deadline EDF Evaluation. ---
            elif ischeme == 'RI-var EDF D1.0':
                # Set Deadlines.
                for itask in tasks:
                    itask['deadline'] = 1.0 * itask['period']
                # Set priorities.
                RI.set_prio(tasks, prio_policy=3)
                # Sched test.
                if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
                    numfail += 1
            elif ischeme == 'RI-var EDF D1.1':
                for itask in tasks:
                    itask['deadline'] = 1.1 * itask['period']
                RI.set_prio(tasks, prio_policy=3)
                if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
                    numfail += 1
            elif ischeme == 'RI-var EDF D1.2':
                for itask in tasks:
                    itask['deadline'] = 1.2 * itask['period']
                RI.set_prio(tasks, prio_policy=3)
                if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
                    numfail += 1
            elif ischeme == 'RI-var EDF D1.5':
                for itask in tasks:
                    itask['deadline'] = 1.5 * itask['period']
                RI.set_prio(tasks, prio_policy=3)
                if RI.RI_var(tasks, depth=RI_depth, max_a=RI_max_a) is False:
                    numfail += 1
            # --- Else. ---
            else:
                assert ischeme, 'not vaild ischeme'

        acceptanceRatio = 1 - (numfail / len(tasksets))
        print("acceptanceRatio:", acceptanceRatio)
        y[u] = acceptanceRatio
        # if acceptanceRatio == 0:
        #     ifskip = True

    plotPath = (gPrefixdata + '/' + str(gMinsstype) + '-' + str(gMaxsstype)
                + '/' + str(gSSofftypes) + '/')
    plotfile = (gPrefixdata + '/' + str(gMinsstype) + '-' + str(gMaxsstype)
                + '/' + str(gSSofftypes) + '/' + ischeme + str(gTasksinBkt))

    # Store results
    if not os.path.exists(plotPath):
        os.makedirs(plotPath)
    np.save(plotfile, np.array([x, y]))


###
# Plot results
###

gPlotall = True
gPlotsingle = False

if gPlotdata:
    if len(gSchemes) != 0:
        try:
            effsstsPlot.effsstsPlotAll(
                gPrefixdata, gPlotall, gSchemes, gMinsstype, gMaxsstype,
                gSSofftypes, gUStart, gUEnd, gUStep, gTasksinBkt, Ncol=Ncol,
                plotsingle=gPlotsingle, plotallname=plotallname)
        except Exception as e:
            MainWindow.statusBar().showMessage(str(e))
    else:
        MainWindow.statusBar().showMessage('There is no plot to draw.')
