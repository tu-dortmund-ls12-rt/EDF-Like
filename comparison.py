import schedTest.UNIFRAMEWORK as uni
import schedTest.OurAnalysis as our
import schedTest.RI as el  # EDF like

import taskCreation.tgPath as create

import numpy as np
import os
import sys
import random
import itertools
from itertools import repeat
from multiprocessing import Pool

import plot  # plot results

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
    '''Create tasksets according to description.'''
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
    '''Test a scheme for all tasksets in tasksets_difutil'''
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
    # Find correct scheme
    if gScheme == 'Our - all 0':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=1)
    elif gScheme == 'Our - 3 vec':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=5)
    elif gScheme == 'Uniframework - all 0':
        return uni.UniFramework_all0(taskset)
    elif gScheme == 'Uniframework - 3 vec':
        return uni.UniFramework(taskset)

    # == Benefit with deadline increase ==
    elif gScheme == 'Our D1.0':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='comb3')
    elif gScheme == 'Our D1.1':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.1)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='comb3')
    elif gScheme == 'Our D1.2':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.2)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='comb3')
    elif gScheme == 'Our D1.3':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.3)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='comb3')
    elif gScheme == 'Our D1.4':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.4)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='comb3')
    elif gScheme == 'Our D1.5':
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # set deadlines
        _set_deadlines(taskset, 1.5)
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='comb3')

    # ==Show that Heuristic is useful==
    elif gScheme in ['All 1 H', 'All 1 L']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=2)
    elif gScheme in ['All 0 H', 'All 0 L']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=1)
    elif gScheme in ['Heuristic Lin H', 'Heuristic Lin L']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=4)
    elif gScheme in ['Exhaust H', 'Exhaust L']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec=0)

    # == Tasks with release jitter ==
    elif gScheme == 'SOTA J Spor':
        tasksetJ = _make_jitter_tasks(taskset, gJitter)
        tasksetJ = _constrained_tasks(tasksetJ)
        return uni.UniFramework(tasksetJ)
    elif gScheme == 'Our J':
        arr_curves = [our.arr_jitter(tsk['period'], gJitter)
                      for tsk in taskset]
        tasksetJ = _make_jitter_tasks(taskset, gJitter)
        return our.sched_test(tasksetJ, arr_curves, choose_xvec='comb3')
    elif gScheme == 'SOTA J CPA':
        arr_curves = [our.arr_jitter(tsk['period'], gJitter)
                      for tsk in taskset]
        tasksetJ = _make_jitter_tasks(taskset, gJitter)
        return our.sota_CPA(tasksetJ, arr_curves)

    # == logarithmic arrival curve ==
    elif gScheme == 'SOTA log':
        return uni.UniFramework(taskset)
    elif gScheme == 'Our log':
        arr_curves = [our.arr_log(tsk['period']) for tsk in taskset]
        return our.sched_test(taskset, arr_curves, choose_xvec=4)

    # == EDF-Like comparison ==
    elif gScheme in ['Our', 'FP']:  # this is used
        # set arrival curves
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do test
        return our.sched_test(taskset, arr_curves, choose_xvec='comb3')

    elif gScheme == 'EL-fixed':
        el.set_prio(taskset, prio_policy=2)
        return el.RI_fixed(taskset)
    elif gScheme == 'EL-var':
        el.set_prio(taskset, prio_policy=2)
        return el.RI_var(taskset, max_a=10)
    elif gScheme == 'Any':
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        el.set_prio(taskset, prio_policy=2)
        return (our.sched_test(taskset, arr_curves, choose_xvec=4) or el.RI_fixed(taskset) or el.RI_var(taskset,
                                                                                                        max_a=5))
    elif gScheme == 'Any EL':
        el.set_prio(taskset, prio_policy=2)
        return (el.RI_fixed(taskset) or el.RI_var(taskset, max_a=10))

    # == Experiments ==
    elif gScheme in ['All 0']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='all0')
    elif gScheme in ['All 1']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='all1')
    elif gScheme in ['Heuristic Lin']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='lin')
    elif gScheme in ['Comb 3']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='comb3')
    elif gScheme in ['Exhaust']:
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='exh')

    # == ELSE ==
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

    # #####
    # # === Try-out settings: ===
    # gTotBucket = 100
    # gTasksinBkt = 20
    # gMultiproc = 0
    # #####

    # Choose schedulability tests
    scheme_flag = sys.argv[2]

    # ==Show that Heuristic is useful==
    # 10 tasks per set
    # Deadline = 1.3 period
    if scheme_flag == '10':
        # high suspension
        gSchemes = ['All 0 H', 'All 1 H', 'Heuristic Lin H', 'Exhaust H']
        plotname = '10_heuristic_useful'
        gTasksinBkt = 10
        deadline_stretch = [1, 1.3]
        gMaxsstype = 0.4  # maximal total self-suspension length
        gMinsstype = 0.1  # minimal total self-suspension length
    elif scheme_flag == '11':
        # low suspension
        gSchemes = ['All 0 L', 'All 1 L', 'Heuristic Lin L', 'Exhaust L']
        plotname = '11_heuristic_useful'
        gTasksinBkt = 10
        deadline_stretch = [1, 1.3]
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length

    # ==Benefit with DL increase==
    elif scheme_flag == '12':
        gSchemes = ['Our D1.0', 'Our D1.1', 'Our D1.2',
                    'Our D1.3', 'Our D1.4', 'Our D1.5']
        plotname = '12_deadline_increase'

    # ==Tasks with release jitter==
    elif scheme_flag == '13':
        gSchemes = ['SOTA J10', 'Our J10', 'SOTA J20', 'Our J20']
        plotname = '13_release_jitter'

    # ==logarithmic arrival curve==
    elif scheme_flag == '14':
        gSchemes = ['SOTA log', 'Our log']
        plotname = '14_log'

    # == EDF-Like comparison 1 ==
    # Deadline = 1.3 period
    elif scheme_flag == '15':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '15_comp_EL_50TH'
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.25  # minimal total self-suspension length
        gTasksinBkt = 50
    elif scheme_flag == '16':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '16_comp_EL_50TL'
        gMaxsstype = 0.25  # maximal total self-suspension length
        gMinsstype = 0.  # minimal total self-suspension length
        gTasksinBkt = 50
    elif scheme_flag == '17':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '17_comp_EL_10TH'
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.25  # minimal total self-suspension length
        gTasksinBkt = 10
    elif scheme_flag == '18':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '18_comp_EL_10TL'
        gMaxsstype = 0.25  # maximal total self-suspension length
        gMinsstype = 0.  # minimal total self-suspension length
        gTasksinBkt = 10
    elif scheme_flag == '19':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '19_comp_EL_100TH'
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.25  # minimal total self-suspension length
        gTasksinBkt = 100
    elif scheme_flag == '20':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '20_comp_EL_100TL'
        gMaxsstype = 0.25  # maximal total self-suspension length
        gMinsstype = 0.  # minimal total self-suspension length
        gTasksinBkt = 100
    # == EDF-Like comparison 2 ==
    # Deadline = 1.3 period
    elif scheme_flag == '21':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '15_comp_EL_50TH'
        deadline_stretch = [1.0, 1.2]
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.25  # minimal total self-suspension length
        gTasksinBkt = 50
    elif scheme_flag == '22':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '16_comp_EL_50TL'
        deadline_stretch = [1.0, 1.2]
        gMaxsstype = 0.25  # maximal total self-suspension length
        gMinsstype = 0.  # minimal total self-suspension length
        gTasksinBkt = 50
    elif scheme_flag == '23':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '17_comp_EL_10TH'
        deadline_stretch = [1.0, 1.2]
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.25  # minimal total self-suspension length
        gTasksinBkt = 10
    elif scheme_flag == '24':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '18_comp_EL_10TL'
        deadline_stretch = [1.0, 1.2]
        gMaxsstype = 0.25  # maximal total self-suspension length
        gMinsstype = 0.  # minimal total self-suspension length
        gTasksinBkt = 10
    elif scheme_flag == '25':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '19_comp_EL_100TH'
        deadline_stretch = [1.0, 1.2]
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.25  # minimal total self-suspension length
        gTasksinBkt = 100
    elif scheme_flag == '26':
        gSchemes = ['Our', 'EL-fixed', 'EL-var', 'Any', 'Any EL']
        plotname = '20_comp_EL_100TL'
        deadline_stretch = [1.0, 1.2]
        gMaxsstype = 0.25  # maximal total self-suspension length
        gMinsstype = 0.  # minimal total self-suspension length
        gTasksinBkt = 100

    # ===== Experiments =====
    # == Exp 1: heuristics
    elif scheme_flag == '101':
        gSchemes = ['All 0', 'All 1', 'Heuristic Lin', 'Comb 3', 'Exhaust']
        plotname = '101_heuristic_usefulM'
        gTasksinBkt = 10
        gMaxsstype = 0.3  # maximal total self-suspension length
        gMinsstype = 0.1  # minimal total self-suspension length
    elif scheme_flag == '102':
        # high suspension
        gSchemes = ['All 0', 'All 1', 'Heuristic Lin', 'Comb 3', 'Exhaust']
        plotname = '102_heuristic_usefulH'
        gTasksinBkt = 10
        gMaxsstype = 0.5  # maximal total self-suspension length
        gMinsstype = 0.3  # minimal total self-suspension length
    elif scheme_flag == '103':
        # low suspension
        gSchemes = ['All 0', 'All 1', 'Heuristic Lin', 'Comb 3', 'Exhaust']
        plotname = '103_heuristic_usefulL'
        gTasksinBkt = 10
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length

    # == Exp 2: exploit deadline
    elif scheme_flag == '201':
        gSchemes = ['Our D1.0', 'Our D1.1', 'Our D1.2',
                    'Our D1.3', 'Our D1.4', 'Our D1.5']
        gTasksinBkt = 30
        plotname = '201_exploit_deadline'
        deadline_stretch = [1.0, 1.0]

    # == Exp 3: release jitter
    elif scheme_flag == '301':
        gSchemes = ['SOTA J Spor', 'SOTA J CPA', 'Our J']
        gJitter = 0.1
        gTasksinBkt = 10
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length
        plotname = '301_release_jitter10'
    elif scheme_flag == '302':
        gSchemes = ['SOTA J Spor', 'SOTA J CPA', 'Our J']
        gJitter = 0.2
        gTasksinBkt = 10
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length
        plotname = '302_release_jitter20'

    ##### Comparison #####
    elif scheme_flag == '401':
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

    ##### Comparison #####
    elif scheme_flag == '501':
        gSchemes = ['FP', 'EL-fixed', 'EL-var']
        plotname = '501'
        gTotBucket = 100  # total number of task sets per utilization
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length
        deadline_stretch = [0.5, 1.2]
    elif scheme_flag == '502':
        gSchemes = ['FP', 'EL-fixed', 'EL-var']
        plotname = '502'
        gTotBucket = 100  # total number of task sets per utilization
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length
        deadline_stretch = [0.5, 1.3]
    elif scheme_flag == '503':
        gSchemes = ['FP', 'EL-fixed', 'EL-var']
        plotname = '503'
        gTotBucket = 100  # total number of task sets per utilization
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length
        deadline_stretch = [0.5, 1.5]

    # == Exp 3: release jitter
    elif scheme_flag == '_301':
        gSchemes = ['SOTA J Spor', 'SOTA J CPA', 'Our J']
        gJitter = 0.1
        gTasksinBkt = 30
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length
        plotname = '_301_release_jitter10'
    elif scheme_flag == '_302':
        gSchemes = ['SOTA J Spor', 'SOTA J CPA', 'Our J']
        gJitter = 0.2
        gTasksinBkt = 30
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length
        plotname = '_302_release_jitter20'
    elif scheme_flag == '_303':
        gSchemes = ['SOTA J Spor', 'SOTA J CPA', 'Our J']
        gJitter = 0.1
        gTasksinBkt = 10
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length
        plotname = '_303_release_jitter10'
    elif scheme_flag == '_304':
        gSchemes = ['SOTA J Spor', 'SOTA J CPA', 'Our J']
        gJitter = 0.2
        gTasksinBkt = 10
        gMaxsstype = 0.1  # maximal total self-suspension length
        gMinsstype = 0.0  # minimal total self-suspension length
        plotname = '_304_release_jitter20'

    # == ELSE ==
    else:
        print('second input argument not valid')
        quit()

    # Create task sets
    if sys.argv[1] == '0':
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
    if sys.argv[1] == '0':
        for gScheme in gSchemes:
            # test
            results = list(zip(itertools.count(start=gUStart, step=gUStep),
                               test_scheme(gScheme, tasksets_difutil, multiproc=gMultiproc)))
            print(list(results))
            # store results
            store_results(results, datapath, gScheme + '.npy')

    # plot results
    if sys.argv[1] in ['0', '1']:
        results_plot = [load_results(datapath, gScheme + '.npy')
                        for gScheme in gSchemes]

        plot.plot(gSchemes, results_plot, plotpath, plotname, Ncol)
