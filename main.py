from __future__ import division
from schedTest import (tgPath, SCEDF, EDA, PROPORTIONAL, NC, SEIFDA, Audsley,
                       rad, PATH, mipx, combo, rt, functions, RSS)
from effsstsPlot import effsstsPlot

###
# Create Task sets
###

gTotBucket = 100  # total number of task sets
gTasksinBkt = 10  # tasks per set

gUStep = 10  # utilization step [in percent]
gUStart = 0  # utilization start
gUEnd = 0  # utilization end

# share from period - wcet for self-suspension:
gMaxsstype = 0.5  # maximal total self-suspension length
gMinsstype = 0.1  # minimal total self-suspension length

gSSofftypes = 2  # number of self-suspension segments

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


###
# Schedulability tests
###
