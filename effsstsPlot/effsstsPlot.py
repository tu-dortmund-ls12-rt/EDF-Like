from __future__ import division
import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import math


def pickColor(ischeme):  # TODO adjust
    color = ''
    if ischeme == 'RI DM':  # --- 1 DM Evaluation.
        color = '#000000'
    elif ischeme == 'UniFramework':
        color = '#0000ff'
    elif ischeme == 'SuspJit':
        color = '#ff9900'
    elif ischeme == 'SuspBlock':
        color = '#33cc33'
    elif ischeme == 'SuspObl':
        color = '#ff0066'
    elif ischeme == 'RI EDF':  # --- 2 EDF Evaluation.
        color = '#000000'
    elif ischeme == 'Our EMSoft':
        color = '#0000ff'
    elif ischeme == 'Dong and Liu':
        color = '#ff9900'
    elif ischeme == 'Liu and Anderson':
        color = '#33cc33'
    elif ischeme == 'Susp as Comp':
        color = '#ff0066'
    elif ischeme == 'RI EQDF lam=0':  # --- 3 EQDF Evaluation.
        color = '#6666ff'
    elif ischeme == 'RI EQDF lam=-1':
        color = '#b3b3ff'
    elif ischeme == 'RI EQDF lam=+1':
        color = '#0000cc'
    elif ischeme == 'RI EQDF any lam in [-10,10]':
        color = '#000000'
    elif ischeme == 'RI SAEDF lam=0':  # --- 4 SAEDF Evaluation.
        color = '#6666ff'
    elif ischeme == 'RI SAEDF lam=-1':
        color = '#b3b3ff'
    elif ischeme == 'RI SAEDF lam=+1':
        color = '#0000cc'
    elif ischeme == 'RI SAEDF any lam in [-10,10]':
        color = '#000000'
    elif ischeme in [  # --- 5 Evaluation.
            'RI-fix DM D1.0', 'RI-var DM D1.0',
            ]:
        color = '#99ff99'
    elif ischeme in [
            'RI-fix DM D1.1', 'RI-var DM D1.1',
            ]:
        color = '#00e600'
    elif ischeme in [
            'RI-fix DM D1.2', 'RI-var DM D1.2',
            ]:
        color = '#008000'
    elif ischeme in [
            'RI-fix DM D1.5', 'RI-var DM D1.5',
            ]:
        color = '#000000'
    elif ischeme in [  # --- 6 Evaluation.
            'RI-fix EDF D1.0', 'RI-var EDF D1.0'
            ]:
        color = '#ff9980'
    elif ischeme in [
            'RI-fix EDF D1.1', 'RI-var EDF D1.1'
            ]:
        color = '#ff3300'
    elif ischeme in [
            'RI-fix EDF D1.2', 'RI-var EDF D1.2'
            ]:
        color = '#b32400'
    elif ischeme in [
            'RI-fix EDF D1.5', 'RI-var EDF D1.5'
            ]:
        color = '#000000'
    else:  # --- Other: Randomly.
        color = "#%06x" % random.randint(0, 0xFFFFFF)
    return color


def pickMarker(ischeme):  # TODO adjust
    marker = ''
    if ischeme in [
            'RI DM',
            'RI EDF',
            'RI EQDF any lam in [-10,10]',
            'RI SAEDF any lam in [-10,10]',
            'RI-fix DM D1.5', 'RI-var DM D1.5',
            'RI-fix EDF D1.5', 'RI-var EDF D1.5'
            ]:
        marker = 'o'
    elif ischeme in [
            'UniFramework',
            'Our EMSoft',
            'RI EQDF lam=0',
            'RI SAEDF lam=0',
            'RI-fix DM D1.1', 'RI-var DM D1.1',
            'RI-fix EDF D1.1', 'RI-var EDF D1.1'
            ]:
        marker = 'x'
    elif ischeme in [
            'SuspJit',
            'Dong and Liu',
            'RI EQDF lam=+1',
            'RI SAEDF lam=+1',
            'RI-fix DM D1.2', 'RI-var DM D1.2',
            'RI-fix EDF D1.2', 'RI-var EDF D1.2'
            ]:
        marker = '>'
    elif ischeme in [
            'SuspBlock',
            'Liu and Anderson',
            'RI EQDF lam=-1',
            'RI SAEDF lam=-1',
            'RI-fix DM D1.0', 'RI-var DM D1.0',
            'RI-fix EDF D1.0', 'RI-var EDF D1.0'
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
        # marker = '<'
        marker = random.choice(randommarker)
    return marker


def pickName(ischeme):  # TODO adjust
    name = ''
    if ischeme == 'UniFramework':  # --- 1 DM Evaluation.
        name = 'CNH16'
    elif ischeme == 'RI EDF':  # --- 2 EDF Evaluation.
        name = 'RI EDF'
    elif ischeme == 'Our EMSoft':
        name = 'GBC20'
    elif ischeme == 'Dong and Liu':
        name = 'DL16'
    elif ischeme == 'Liu and Anderson':
        name = 'LA13'
    elif ischeme == 'Susp as Comp':
        name = 'SuspObl'
    elif ischeme == 'RI EQDF lam=0':  # --- 3 EQDF Evaluation.
        name = 'RI EQDF $\lambda=0$'
    elif ischeme == 'RI EQDF lam=-1':
        name = 'RI EQDF $\lambda=-1$'
    elif ischeme == 'RI EQDF lam=+1':
        name = 'RI EQDF $\lambda=+1$'
    elif ischeme == 'RI EQDF any lam in [-10,10]':
        name = 'RI EQDF $\lambda \in [-10,10]$'
    elif ischeme == 'RI SAEDF lam=0':  # --- 4 SAEDF Evaluation.
        name = 'RI SAEDF $\lambda=0$'
    elif ischeme == 'RI SAEDF lam=-1':
        name = 'RI SAEDF $\lambda=-1$'
    elif ischeme == 'RI SAEDF lam=+1':
        name = 'RI SAEDF $\lambda=1$'
    elif ischeme == 'RI SAEDF any lam in [-10,10]':
        name = 'RI SAEDF $\lambda \in [-10,10]$'
    else:
        name = ischeme
    return name


def pickLineStyle(ischeme):
    if ischeme in [
            'SuspJit',
            'SuspBlock',
            'Dong and Liu',
            'Liu and Anderson',
            'RI EQDF lam=-1',
            'RI EQDF lam=+1',
            'RI SAEDF lam=-1',
            'RI SAEDF lam=+1',
            'RI-fix DM D1.0', 'RI-var DM D1.0',
            'RI-fix EDF D1.0', 'RI-var EDF D1.0',
            'RI-fix DM D1.2', 'RI-var DM D1.2',
            'RI-fix EDF D1.2', 'RI-var EDF D1.2'
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


def effsstsPlot(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks,Ncol=3, plotallname=''):
    """
    prints all plots
    """
    # sstype= ['S','M','L','0.15']
    # ssofftypes = [2, 3, 5]
    ssoprops = ['2', '5', '8']

    figlabel = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # prefix="effsstsPlot/data/"

    # for three sub-plot, fixed
    # fig = plt.figure(figsize=(13, 4))
    fig = plt.figure()
    # create a virtual outer subsplot for putting big x-ylabel
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.9, left=0.1, right=0.95, hspace=0.3)

    ax.set_xlabel('Utilization (%)', size=15, fontsize=20)
    ax.set_ylabel('Acceptance Ratio', size=15, fontsize=20)
    ax.spines['top'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.tick_params(labelcolor='black', top=False,
                   bottom=False, left=False, right=False, labelsize=16)

    i = 1
    for ischeme in schemes:
        ifile = prefix+"/"+str(minsstype)+"-"+str(maxsstype)+"/"+str(ssofftypes)+"/"+ischeme+ str(numberoftasks) +".npy"
        data = np.load(ifile)
        x = data[0][0::1]
        y = data[1][0::1]
        us = int(math.ceil(ustart/ustep))
        ue = int(math.floor(uend/ustep))
        print(x)
        print(y)
        x=x[us:ue+1]
        y=y[us:ue+1]
        ax.plot(x, y,
                pickLineStyle(ischeme),
                color=pickColor(ischeme),
                marker=pickMarker(ischeme),
                markersize=5,
                markevery=1,
                fillstyle='none',
                label=pickName(ischeme),
                linewidth=1.0,
                clip_on=False)
        if i == 1:
            ax.legend(bbox_to_anchor=(0.5, 1.2),
                        loc=10,
                        markerscale=1.5,
                        ncol=Ncol,
                        borderaxespad=0.,
                        prop={'size': 16})

    ax.set_title('No. of tasks: '+str(numberoftasks)+', Self-suspension length: ' +
                    str(minsstype)+"-"+str(maxsstype), size=10, y=0.99, fontsize=20)
    ax.grid()
    i += 1
    #fig.savefig(prefix+"/"+isstype+"/"+issofftypes +
        #           "/"+ischeme+".pdf", bbox_inches='tight')

    #plt.show()
    if plotall:
        if plotallname != '':
            fig.savefig(prefix + '/' + plotallname + '.pdf', bbox_inches='tight')
            print('[DONE]', '/' + prefix + '/' + plotallname + '.pdf')
        else:
            fig.savefig(prefix + '/EFFSSTS[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf', bbox_inches='tight')
            print('[DONE]', '/' + prefix + '/EFFSSTS[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf')
    else:
        fig.savefig(prefix + '/' + schemes[0] + '[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf', bbox_inches='tight')
        print('[DONE]', '/' + prefix + '/' + schemes[0] + '[' +  str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf')
    #sys.exit()


def effsstsPlotmulti(prefix, plotall, id_par, par_values, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks):
    """
    prints all plots
    """
    # sstype= ['S','M','L','0.15']
    # ssofftypes = [2, 3, 5]
    ssoprops = ['2', '5', '8']

    figlabel = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    # prefix="effsstsPlot/data/"

    # for three sub-plot, fixed
    # fig = plt.figure(figsize=(13, 4))
    #fig = plt.figure()
    # create a virtual outer subsplot for putting big x-ylabel
    # ax = fig.add_subplot(111)
    # fig.subplots_adjust(top=0.9, left=0.1, right=0.95, hspace=0.3)
    if id_par == 'Tasks per set':
        numberoftasks = par_values

    elif id_par == 'Number of Segments':
        ssofftypes = par_values
        print
        'ns1: ', ssofftypes[0]
    elif id_par == 'Suspension Length':
        minsstype = par_values[0:3]
        maxsstype = par_values[3:6]

    fig = plt.figure(figsize=(18, 12))
    for c in range(3):
        ax = fig.add_subplot(2, 3, (c + 1))

        ax.set_xlabel('Utilization (%)', size=10)
        ax.set_ylabel('Acceptance Ratio', size=10)
        ax.spines['top'].set_color('black')
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.spines['right'].set_color('black')
        ax.tick_params(labelcolor='black', top=False,
                       bottom=False, left=False, right=False)
        i = 1
        for ischeme in schemes:
            if id_par == 'Tasks per set':
                ifile = prefix + "/" + str(minsstype) + "-" + str(maxsstype) + "/" + str(
                    ssofftypes) + "/" + ischeme + str(numberoftasks[c]) + ".npy"
            elif id_par == 'Number of Segments':
                ifile = prefix + "/" + str(minsstype) + "-" + str(maxsstype) + "/" + str(
                    ssofftypes[c]) + "/" + ischeme + str(numberoftasks) + ".npy"
            elif id_par == 'Suspension Length':
                ifile = prefix + "/" + str(minsstype[c]) + "-" + str(maxsstype[c]) + "/" + str(
                    ssofftypes) + "/" + ischeme + str(numberoftasks) + ".npy"
            data = np.load(ifile)
            x = data[0][0::1]
            y = data[1][0::1]
            us = int(math.ceil(ustart/ustep))
            ue = int(math.floor(uend/ustep))
            print(x)
            print(y)
            x=x[us:ue+1]
            y=y[us:ue+1]
            ax.plot(x, y,
                    '-',
                    color=pickColor(ischeme),
                    marker=pickMarker(ischeme),
                    markersize=4,
                    markevery=1,
                    fillstyle='none',
                    label=pickName(ischeme),
                    linewidth=1.0,
                    clip_on=False)
            if c==1:
                ax.legend(bbox_to_anchor=(0.5, 1.11),
                          loc=10,
                          markerscale=1.5,
                          ncol=3,
                          borderaxespad=0.,
                          prop={'size': 10})
            if i == 1:
                ax.grid()
            i += 1

    fig.suptitle('No. of tasks: '+str(numberoftasks)+', Self-suspension length: ' +
                    str(minsstype)+"-"+str(maxsstype), size=16, y=0.99)
    # ax.grid()

    #fig.savefig(prefix+"/"+isstype+"/"+issofftypes +
        #           "/"+ischeme+".pdf", bbox_inches='tight')

    #plt.show()
    if plotall:
        fig.savefig(prefix + '/EFFSSTS[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf', bbox_inches='tight')
        print('[DONE]', '/' + prefix + '/EFFSSTS[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf')
    else:
        fig.savefig(prefix + '/' + schemes[0] + '[' + str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf', bbox_inches='tight')
        print('[DONE]', '/' + prefix + '/' + schemes[0] + '[' +  str(ssofftypes) + '][' + str(minsstype)+"-"+str(maxsstype) + '][' + str(numberoftasks) + '].pdf')


def effsstsPlotAll(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, Ncol=3, plotsingle=True, plotallname=''):
    print('-------------------------------------------------------')
    print(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep,numberoftasks)
    print('-------------------------------------------------------')
    if plotsingle:
        for scheme in schemes:
            effsstsPlot(prefix, False, [scheme], minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, Ncol=Ncol)
    if (plotall):
        effsstsPlot(prefix, True, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks, Ncol=Ncol, plotallname=plotallname)


def effsstsPlotAllmulti(prefix, plotall, id_par, par_values, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks):
    print('-------------------------------------------------------')
    print(prefix, plotall, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep,numberoftasks)
    print('-------------------------------------------------------')
    for scheme in schemes:
        effsstsPlotmulti(prefix, False, id_par, par_values, scheme.split(), minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks)
    if (plotall):
        effsstsPlotmulti(prefix, True, id_par, par_values, schemes, minsstype, maxsstype, ssofftypes, ustart, uend, ustep, numberoftasks)

if __name__ == '__main__':
    args = sys.argv
    print(args)
    testSchemes = ['EDA', 'NC', 'SCEDF', 'PASS-OPA']
    testSelfSuspendingType= ['S','M','L']
    testNumberofSegments = [2]
    effsstsPlotAll(args[1], True, testSchemes, testSelfSuspendingType, testNumberofSegments, 1, 99, 5, 10)
