from __future__ import division
from schedTest import tgPath, RI, RTEDF, UDLEDF, SCEDF, WLAEDF, Audsley, UniFramework, FP_Analyses
from effsstsPlot import effsstsPlot

import numpy as np
import os

import random


###
# global preferences
###

gTotBucket = 100  # total number of task sets
gTasksinBkt = 10  # tasks per set

gUStep = 5  # utilization step [in percent]
gUStart = 0  # utilization start
gUEnd = 100  # utilization end

# share from period - wcet for self-suspension:
gMaxsstype = 0.5  # maximal total self-suspension length
gMinsstype = 0.0  # minimal total self-suspension length

gSSofftypes = 2  # number of self-suspension segments

# Schedulability tests to be run:
# # EDF Evaluation.
# gSchemes = ['RI EDF', 'Our EMSoft', 'Dong and Liu', 'Liu and Anderson', 'Susp as Comp']
# # DM Evaluation.
# gSchemes = ['RI DM', 'UniFramework', 'SuspObl', 'SuspJit', 'SuspBlock']
# # RI EQDF
# gSchemes = ['RI EQDF lam=-1', 'RI EQDF lam=0', 'RI EQDF lam=1', 'RI EQDF lam=10', 'RI EQDF lam=100', 'RI EQDF lam=1000']
# # RI SAEDF
# gSchemes = ['RI SAEDF lam=-1', 'RI SAEDF lam=0', 'RI SAEDF lam=1', 'RI SAEDF lam=10', 'RI SAEDF lam=100', 'RI SAEDF lam=1000']
# # Other
# gSchemes = ['RI FIFO', 'RI Pi=C', 'RI Pi=S', 'RI Pi=D*C', 'RI Pi=D*S', 'RI Pi=C*S']
# # RI fix any
# gSchemes = ['RI-fix-any']

# RI arb deadline DM
gSchemes = ['RI-var DM D1.0', 'RI-var DM D1.1', 'RI-var DM D1.2', 'RI-var DM D1.5']

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
            elif ischeme == 'RI-fix-1':  # RI scheduling
                if RI.RI_fixed(tasks, depth=3, setprio=1) is False:
                    numfail += 1
            elif ischeme == 'RI-fix-2':  # RI scheduling
                if RI.RI_fixed(tasks, depth=3, setprio=2) is False:
                    numfail += 1
            elif ischeme == 'RI-fix-3':  # RI scheduling
                if RI.RI_fixed(tasks, depth=3, setprio=3) is False:
                    numfail += 1
            elif ischeme == 'RI-fix-4':  # RI scheduling
                if RI.RI_fixed(tasks, depth=3, setprio=4) is False:
                    numfail += 1
            elif ischeme == 'RI-fix-5':  # RI scheduling
                if RI.RI_fixed(tasks, depth=3, setprio=5) is False:
                    numfail += 1
            elif ischeme == 'RI-fix-6':  # RI scheduling
                if RI.RI_fixed(tasks, depth=3, setprio=6) is False:
                    numfail += 1
            elif ischeme == 'RI-fix-7':  # RI scheduling
                if RI.RI_fixed(tasks, depth=3, setprio=7) is False:
                    numfail += 1
            elif ischeme == 'RI-fix-8':  # RI scheduling
                if RI.RI_fixed(tasks, depth=3, setprio=8) is False:
                    numfail += 1
            elif ischeme == 'RI-fix-9':  # RI scheduling
                if RI.RI_fixed(tasks, depth=3, setprio=9) is False:
                    numfail += 1
            elif ischeme == 'RI-fix-any':  # RI scheduling
                fail_flag = True
                for ind in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    if RI.RI_fixed(tasks, depth=3, setprio=ind) is True:
                        fail_flag = False
                if fail_flag:
                    numfail += 1
            elif ischeme == 'RI EDF':  # RI scheduling
                RI.set_prio(tasks, prio_policy=101)
                if RI.RI_fixed(tasks, depth=3) is False:
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
            elif ischeme == 'RI DM':  # RI scheduling
                RI.set_prio(tasks, prio_policy=2)
                if RI.RI_fixed(tasks, depth=3) is False:
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
            # RI EQDF
            elif ischeme == 'RI EQDF lam=-1':
                RI.set_prio(tasks, prio_policy=201)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI EQDF lam=0':
                RI.set_prio(tasks, prio_policy=202)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI EQDF lam=1':
                RI.set_prio(tasks, prio_policy=203)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI EQDF lam=10':
                RI.set_prio(tasks, prio_policy=204)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI EQDF lam=100':
                RI.set_prio(tasks, prio_policy=205)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI EQDF lam=1000':
                RI.set_prio(tasks, prio_policy=206)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            # RI SAEDF
            elif ischeme == 'RI SAEDF lam=-1':
                RI.set_prio(tasks, prio_policy=301)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI SAEDF lam=0':
                RI.set_prio(tasks, prio_policy=302)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI SAEDF lam=1':
                RI.set_prio(tasks, prio_policy=303)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI SAEDF lam=10':
                RI.set_prio(tasks, prio_policy=304)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI SAEDF lam=100':
                RI.set_prio(tasks, prio_policy=305)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI SAEDF lam=1000':
                RI.set_prio(tasks, prio_policy=306)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            # Other
            elif ischeme == 'RI FIFO':
                RI.set_prio(tasks, prio_policy=401)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI Pi=C':
                RI.set_prio(tasks, prio_policy=402)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI Pi=S':
                RI.set_prio(tasks, prio_policy=403)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI Pi=D*C':
                RI.set_prio(tasks, prio_policy=404)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI Pi=D*S':
                RI.set_prio(tasks, prio_policy=405)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI Pi=C*S':
                RI.set_prio(tasks, prio_policy=406)
                if RI.RI_fixed(tasks, depth=3) is False:
                    numfail += 1
            elif ischeme == 'RI-fix-any':  # RI scheduling
                fail_flag = True
                for ind in [101,  # RI EDF
                            2,  # RI DM
                            201, 202, 203, 204, 205, 206,  # RI EQEDF
                            301, 302, 303, 304, 305, 306,  # RI SAEDF
                            401, 402, 403, 404, 405, 406]:  # RI Other
                    RI.set_prio(tasks, prio_policy=ind)
                    if RI.RI_fixed(tasks, depth=3) is True:
                        fail_flag = False
                        break
                if fail_flag:
                    numfail += 1
            # RI-var DM
            elif ischeme == 'RI-var DM D1.0':
                # Set Deadlines.
                for itask in tasks:
                    itask['deadline'] = 1.0 * itask['period']
                # Set priorities.
                RI.set_prio(tasks, prio_policy=2)
                # Sched test.
                if RI.RI_var(tasks, depth=3, max_a=5) is False:
                    numfail += 1
            elif ischeme == 'RI-var DM D1.1':
                # Set Deadlines.
                for itask in tasks:
                    itask['deadline'] = 1.1 * itask['period']
                # Set priorities.
                RI.set_prio(tasks, prio_policy=2)
                # Sched test.
                if RI.RI_var(tasks, depth=3, max_a=5) is False:
                    numfail += 1
            elif ischeme == 'RI-var DM D1.2':
                # Set Deadlines.
                for itask in tasks:
                    itask['deadline'] = 1.2 * itask['period']
                # Set priorities.
                RI.set_prio(tasks, prio_policy=2)
                # Sched test.
                if RI.RI_var(tasks, depth=3, max_a=5) is False:
                    numfail += 1
            elif ischeme == 'RI-var DM D1.5':
                # Set Deadlines.
                for itask in tasks:
                    itask['deadline'] = 1.5 * itask['period']
                # Set priorities.
                RI.set_prio(tasks, prio_policy=2)
                # Sched test.
                if RI.RI_var(tasks, depth=3, max_a=5) is False:
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
