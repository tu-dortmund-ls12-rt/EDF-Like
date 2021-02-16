from __future__ import division
from schedTest import tgPath, RI
from effsstsPlot import effsstsPlot

import numpy as np
import os

import random


###
# global preferences
###

gTotBucket = 100  # total number of task sets
gTasksinBkt = 10  # tasks per set

gUStep = 10  # utilization step [in percent]
gUStart = 0  # utilization start
gUEnd = 100  # utilization end

# share from period - wcet for self-suspension:
gMaxsstype = 0.3  # maximal total self-suspension length
gMinsstype = 0.1  # minimal total self-suspension length

gSSofftypes = 2  # number of self-suspension segments

gSchemes = ['RI-fix']  # schedulability tests to be run

gPlotdata = True  # flag to plot data

gPrefixdata = "effsstsPlot/Data"  # path to store data

###
# Create Task sets
###

tasksets_difutil = []  # task set differentiated by utilization

for u in range(gUStart, gUEnd, gUStep):
    tasksets = []
    for i in range(0, gTotBucket, 1):
        percentageU = u / 100
        # Create task set with predefined parameters.
        tasks = tgPath.taskGeneration_p(gTasksinBkt, percentageU, gMinsstype,
                                        gMaxsstype, vRatio=1,
                                        numLog=int(2), numsegs=gSSofftypes)
        # Sort tasks by period.
        sortedTasks = sorted(tasks, key=lambda item: item['period'])
        tasksets.append(sortedTasks)  # add
    tasksets_difutil.append(tasksets)  # add

# breakpoint()
###
# Add priority shifts
###
import math
for tasksets in tasksets_difutil:
    for taskset in tasksets:
        # p = 0  # DM
        for task in taskset:
            # task['prio_shift'] = task['deadline']
            # task['prio_shift'] = task['deadline']-0.5*task['sslength']
            # task['prio_shift'] = task['deadline']+0.5*task['sslength']
            # task['prio_shift'] = task['deadline']*task['execution']
            # task['prio_shift'] = (task['deadline']+0.5*task['sslength'])*task['execution']
            # task['prio_shift'] = task['deadline'] * (task['execution'] + 0.5 * task['sslength'])

            # # DM:
            # p += task['deadline']
            # task['prio_shift'] = p

            # FIFO:
            task['prio_shift'] = 0



###
# Schedulability tests
###

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
              str(gMinsstype), " - ", str(gMaxsstype),
              "Num. of segments:", gSSofftypes)
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
        for tasks in tasksets:  # iterate for each taskset
            if ischeme == 'SCEDF':
                if SCEDF.SC_EDF(tasks) is False:
                    numfail += 1
            elif ischeme == 'SCRM':
                if SEIFDA.SC_RM(tasks) is False:
                    numfail += 1
            elif ischeme == 'PASS-OPA':
                if Audsley.Audsley(tasks) is False:
                    numfail += 1
            elif ischeme == 'SEIFDA-MILP':
                if mipx.mip(tasks) is False:
                    numfail += 1
            elif ischeme.split('-')[0] == 'SEIFDA':
                if SEIFDA.greedy(tasks, ischeme) is False:
                    numfail += 1
            elif ischeme.split('-')[0] == 'PATH':
                if PATH.PATH(tasks, ischeme) is False:
                    numfail += 1
            elif ischeme == 'EDA':
                if EDA.EDA(tasks, gSSofftypes) is False:
                    numfail += 1
            elif ischeme == 'PROPORTIONAL':
                if PROPORTIONAL.PROPORTIONAL(tasks, gSSofftypes) is False:
                    numfail += 1
            elif ischeme == 'NC':
                if NC.NC(tasks) is False:
                    numfail += 1
            elif ischeme == 'SCAIR-RM':
                if rad.scair_dm(tasks) is False:
                    numfail += 1
            elif ischeme == 'SCAIR-OPA':
                if rad.Audsley(tasks, ischeme) is False:  # sorted tasks
                    numfail += 1
            elif ischeme == 'Biondi':
                if rt.Biondi(tasks) is False:
                    numfail += 1
            # khchen
            elif ischeme == 'Combo-SJSB':
                if combo.sjsb(tasks) is False:  # sorted tasks
                    numfail += 1
            # hteper
            elif ischeme == 'RSS':
                if RSS.SC2EDF(tasks) is False:  # sorted tasks
                    numfail += 1
            # mguenzel
            elif ischeme == 'RI-fix':  # RI scheduling
                if RI.RI_fixed_better(tasks, abort=3) is False:
                    numfail += 1
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

if gPlotdata:
    if len(gSchemes) != 0:
        try:
            effsstsPlot.effsstsPlotAll(gPrefixdata, gPlotall, gSchemes, gMinsstype, gMaxsstype, gSSofftypes,
                                       gUStart, gUEnd, gUStep, gTasksinBkt)
        except Exception as e:
            MainWindow.statusBar().showMessage(str(e))
    else:
        MainWindow.statusBar().showMessage('There is no plot to draw.')
