#!/usr/bin/env python3
"""Most functions taken from or inspired by SSSEvaluation:
https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/blob/master/effsstsPlot/effsstsPlot.py"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import math


###
# Help functions.
###
def pickColor(ischeme):
    """Pick color for different schemes."""
    color = ''  # color
    if ischeme == 'EL DM':  # --- 1 DM Evaluation.
        color = '#000000'
    elif ischeme == 'UniFramework':
        color = '#0000ff'
    elif ischeme == 'SuspJit':
        color = '#ff9900'
    elif ischeme == 'SuspBlock':
        color = '#33cc33'
    elif ischeme == 'SuspObl':
        color = '#ff0066'
    elif ischeme == 'EL EDF':  # --- 2 EDF Evaluation.
        color = '#000000'
    elif ischeme == 'Our EMSoft':
        color = '#0000ff'
    elif ischeme == 'Dong and Liu':
        color = '#ff9900'
    elif ischeme == 'Liu and Anderson':
        color = '#33cc33'
    elif ischeme == 'Susp as Comp':
        color = '#ff0066'
    elif ischeme == 'EL EQDF lam=0':  # --- 3 EQDF Evaluation.
        color = '#6666ff'
    elif ischeme == 'EL EQDF lam=-1':
        color = '#b3b3ff'
    elif ischeme == 'EL EQDF lam=+1':
        color = '#0000cc'
    elif ischeme == 'EL EQDF any lam in [-10,10]':
        color = '#000000'
    elif ischeme == 'EL SAEDF lam=0':  # --- 4 SAEDF Evaluation.
        color = '#6666ff'
    elif ischeme == 'EL SAEDF lam=-1':
        color = '#b3b3ff'
    elif ischeme == 'EL SAEDF lam=+1':
        color = '#0000cc'
    elif ischeme == 'EL SAEDF any lam in [-10,10]':
        color = '#000000'
    elif ischeme in [  # --- 5 Evaluation.
        'EL-fix DM D1.0', 'EL-var DM D1.0',
    ]:
        color = '#99ff99'
    elif ischeme in [
        'EL-fix DM D1.1', 'EL-var DM D1.1',
    ]:
        color = '#00e600'
    elif ischeme in [
        'EL-fix DM D1.2', 'EL-var DM D1.2',
    ]:
        color = '#008000'
    elif ischeme in [
        'EL-fix DM D1.5', 'EL-var DM D1.5',
    ]:
        color = '#000000'
    elif ischeme in [  # --- 6 Evaluation.
        'EL-fix EDF D1.0', 'EL-var EDF D1.0'
    ]:
        color = '#ff9980'
    elif ischeme in [
        'EL-fix EDF D1.1', 'EL-var EDF D1.1'
    ]:
        color = '#ff3300'
    elif ischeme in [
        'EL-fix EDF D1.2', 'EL-var EDF D1.2'
    ]:
        color = '#b32400'
    elif ischeme in [
        'EL-fix EDF D1.5', 'EL-var EDF D1.5'
    ]:
        color = '#000000'
    else:  # --- Other: Randomly.
        color = "#%06x" % random.randint(0, 0xFFFFFF)
    return color


def pickMarker(ischeme):  # TODO adjust
    """Pick marker for different schemes."""
    marker = ''  # marker
    if ischeme in [
        'EL DM',
        'EL EDF',
        'EL EQDF any lam in [-10,10]',
        'EL SAEDF any lam in [-10,10]',
        'EL-fix DM D1.5', 'EL-var DM D1.5',
        'EL-fix EDF D1.5', 'EL-var EDF D1.5'
    ]:
        marker = 'o'
    elif ischeme in [
        'UniFramework',
        'Our EMSoft',
        'EL EQDF lam=0',
        'EL SAEDF lam=0',
        'EL-fix DM D1.1', 'EL-var DM D1.1',
        'EL-fix EDF D1.1', 'EL-var EDF D1.1'
    ]:
        marker = 'x'
    elif ischeme in [
        'SuspJit',
        'Dong and Liu',
        'EL EQDF lam=+1',
        'EL SAEDF lam=+1',
        'EL-fix DM D1.2', 'EL-var DM D1.2',
        'EL-fix EDF D1.2', 'EL-var EDF D1.2'
    ]:
        marker = '>'
    elif ischeme in [
        'SuspBlock',
        'Liu and Anderson',
        'EL EQDF lam=-1',
        'EL SAEDF lam=-1',
        'EL-fix DM D1.0', 'EL-var DM D1.0',
        'EL-fix EDF D1.0', 'EL-var EDF D1.0'
    ]:
        marker = '<'
    elif ischeme in [
        'SuspObl',
        'Susp as Comp'
    ]:
        marker = '|'
    else:
        randommarker = ['o', 'v', '^', '<', '>', '1', '2', '3', '4', '8', 's',
                        'p', 'P', '*', '+', 'x', 'X', 'D', 'd']
        marker = random.choice(randommarker)
    return marker


def pickName(ischeme):
    """Pick name for different schemes."""
    name = ''
    if ischeme == 'UniFramework':  # --- 1 DM Evaluation.
        name = 'CNH16'
    elif ischeme == 'EL EDF':  # --- 2 EDF Evaluation.
        name = 'EL EDF'
    elif ischeme == 'Our EMSoft':
        name = 'GBC20'
    elif ischeme == 'Dong and Liu':
        name = 'DL16'
    elif ischeme == 'Liu and Anderson':
        name = 'LA13'
    elif ischeme == 'Susp as Comp':
        name = 'SuspObl'
    elif ischeme == 'EL EQDF lam=0':  # --- 3 EQDF Evaluation.
        name = 'EL EQDF $\lambda=0$'
    elif ischeme == 'EL EQDF lam=-1':
        name = 'EL EQDF $\lambda=-1$'
    elif ischeme == 'EL EQDF lam=+1':
        name = 'EL EQDF $\lambda=+1$'
    elif ischeme == 'EL EQDF any lam in [-10,10]':
        name = 'EL EQDF $\lambda \in [-10,10]$'
    elif ischeme == 'EL SAEDF lam=0':  # --- 4 SAEDF Evaluation.
        name = 'EL SAEDF $\lambda=0$'
    elif ischeme == 'EL SAEDF lam=-1':
        name = 'EL SAEDF $\lambda=-1$'
    elif ischeme == 'EL SAEDF lam=+1':
        name = 'EL SAEDF $\lambda=+1$'
    elif ischeme == 'EL SAEDF any lam in [-10,10]':
        name = 'EL SAEDF $\lambda \in [-10,10]$'
    else:
        name = ischeme
    return name


def pickLineStyle(ischeme):
    """Pick line style for different schemes."""
    if ischeme in [
        'SuspJit',
        'SuspBlock',
        'Dong and Liu',
        'Liu and Anderson',
        'EL EQDF lam=-1',
        'EL EQDF lam=+1',
        'EL SAEDF lam=-1',
        'EL SAEDF lam=+1',
        'EL-fix DM D1.0', 'EL-var DM D1.0',
        'EL-fix EDF D1.0', 'EL-var EDF D1.0',
        'EL-fix DM D1.2', 'EL-var DM D1.2',
        'EL-fix EDF D1.2', 'EL-var EDF D1.2'
    ]:
        linestyle = '--'
    elif ischeme in [
        'SuspObl',
        'Susp as Comp',
    ]:
        linestyle = ':'
    else:
        linestyle = '-'
    return linestyle


###
# Main functions.
###
def effsstsPlot(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, Ncol=3,
                plotallname=''):
    """ Make a plot of the results obtained by schemes."""

    fig = plt.figure()
    # Create a virtual outer subsplot for putting big x-ylabel
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.8, left=0.2, right=0.95, bottom=0.25, hspace=0.3)

    ax.set_xlabel('Utilization (%)', size=23)
    ax.set_ylabel('Acceptance Ratio', size=23)
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.tick_params(labelcolor='black', top=False,
                   bottom=False, left=False, right=False, labelsize=22)
    ax.set_yticks([0, 0.25, 0.50, 0.75, 1.0])

    i = 1
    for ischeme in schemes:  # iterate over schemes
        # Load data with evaluation results
        ifile = prefix + "/" + str(minsstype) + "-" + str(maxsstype) + "/" + str(ssofftypes) + "/" + ischeme + str(
            numberoftasks) + ".npy"
        data = np.load(ifile)
        x = data[0][0::1]
        y = data[1][0::1]

        # Print results.
        print(x)
        print(y)

        # Extract the correct values.
        us = int(math.ceil(ustart / ustep))
        ue = int(math.floor(uend / ustep))
        x = x[us:ue + 1]
        y = y[us:ue + 1]

        # Plot.
        ax.plot(x, y,
                pickLineStyle(ischeme),
                color=pickColor(ischeme),
                marker=pickMarker(ischeme),
                markersize=8,
                markevery=1,
                fillstyle='none',
                label=pickName(ischeme),
                linewidth=1.8,
                clip_on=False)
        if i == 1:
            # Add a legend.
            ax.legend(
                bbox_to_anchor=(0.42, 1.15),
                loc=10,
                markerscale=1.3,
                ncol=Ncol,
                borderaxespad=0.,
                labelspacing=0.2,  # space between rows
                handlelength=1.8,  # length of the legend line under marker
                handletextpad=0.5,  # space between handle and text
                columnspacing=1.,  # space between columns
                prop={'size': 18})
        i += 1
    # Add grid.
    ax.grid()

    # Store pdf under the specific name.
    if plotall:
        if plotallname != '':
            fig.savefig(prefix + '/' + plotallname + '.pdf', bbox_inches='tight')
            print('[DONE]', '/' + prefix + '/' + plotallname + '.pdf')
        else:
            fig.savefig(
                prefix + '/EFFSSTS[' + str(ssofftypes) + '][' + str(minsstype) + "-" + str(maxsstype) + '][' + str(
                    numberoftasks) + '].pdf', bbox_inches='tight')
            print('[DONE]', '/' + prefix + '/EFFSSTS[' + str(ssofftypes) + '][' + str(minsstype) + "-" + str(
                maxsstype) + '][' + str(numberoftasks) + '].pdf')
    else:
        fig.savefig(prefix + '/' + schemes[0] + '[' + str(ssofftypes) + '][' + str(minsstype) + "-" + str(
            maxsstype) + '][' + str(numberoftasks) + '].pdf', bbox_inches='tight')
        print('[DONE]', '/' + prefix + '/' + schemes[0] + '[' + str(ssofftypes) + '][' + str(minsstype) + "-" + str(
            maxsstype) + '][' + str(numberoftasks) + '].pdf')


def effsstsPlotAll(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks,
                   Ncol=3, plotsingle=True, plotallname=''):
    """Plot function."""
    # Print the plot variables.
    print('-------------------------------------------------------')
    print(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks)
    print('-------------------------------------------------------')
    # Plot.
    if plotsingle:  # One plot for each scheme.
        for scheme in schemes:
            effsstsPlot(prefix, False, [scheme], minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks,
                        Ncol=Ncol)
    if plotall:  # One combined plot all schemes.
        effsstsPlot(prefix, True, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks,
                    Ncol=Ncol, plotallname=plotallname)


def effsstsPlotRuntime(
        prefix, schemes, num_tasks_start, num_tasks_end, num_tasks_step,
        Ncol=3, plotallname=' ', method='avg', ylabel='Runtime (s)',
        show_legend=True):
    """Make plots for the runtime evalutiation.
    (Plots are not presented in the paper, only the values are reported.)"""

    fig = plt.figure()
    # Create a virtual outer subsplot for putting big x-ylabel
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.9, left=0.1, right=0.95, hspace=0.3)

    ax.set_xlabel('#Tasks', fontsize=23)
    ax.set_ylabel(ylabel, fontsize=23)
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.tick_params(labelcolor='black', top=False,
                   bottom=False, left=False, right=False, labelsize=22)

    i = 1
    for ischeme in schemes:  # iterate over schemes
        # Load data with evaluation results
        x = []
        y = []
        for numberoftasks in range(num_tasks_start, num_tasks_end, num_tasks_step):
            ifile = prefix + "/Runtime/" + ischeme + str(numberoftasks) + '_runtime' + ".npy"
            data = np.load(ifile)
            x.append(numberoftasks)
            if method == 'avg':
                y.append(np.average(data))
            elif method == 'max':
                y.append(np.max(data))

        # Print results.
        print(x)
        print(y)

        # Plot.
        ax.plot(x, y,
                pickLineStyle(ischeme),
                color=pickColor(ischeme),
                marker=pickMarker(ischeme),
                markersize=8,
                markevery=1,
                fillstyle='none',
                label=pickName(ischeme),
                linewidth=1.8,
                clip_on=False)
        if i == 1:
            # Add a legend.
            if show_legend is True:
                ax.legend(
                    bbox_to_anchor=(0.42, 1.15),
                    loc=10,
                    markerscale=1.3,
                    ncol=Ncol,
                    borderaxespad=0.,
                    labelspacing=0.2,  # space between rows
                    handlelength=1.8,  # length of the legend line under marker
                    handletextpad=0.5,  # space between handle and text
                    columnspacing=1.,  # space between columns
                    prop={'size': 20})
        i += 1

    # Add grid.
    ax.grid()

    # Store pdf under the specific name.
    fig.savefig(prefix + '/' + plotallname + '.pdf', bbox_inches='tight')
