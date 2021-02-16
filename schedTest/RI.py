from math import ceil  # ceiling function


def set_prio(tasks, prio_policy=0, lam=0):
    # if prio_policy not in [1, 2, 3, 4]:
    #     print("Priority policy is not implemented.")
    #     return
    if prio_policy == 2:  # DM
        p = 0
    for task in tasks:
        if prio_policy == 1:  # FIFO:
            task['prio_shift'] = 0
        elif prio_policy == 2:  # DM:
            p += task['deadline']
            task['prio_shift'] = p
        elif prio_policy == 3:  # EDF
            task['prio_shift'] = task['deadline']
        elif prio_policy == 4:
            task['prio_shift'] = task['deadline']-0.5*task['sslength']
        elif prio_policy == 5:
            task['prio_shift'] = task['deadline']+0.5*task['sslength']
        elif prio_policy == 6:
            task['prio_shift'] = task['deadline']*task['execution']
        elif prio_policy == 7:
            task['prio_shift'] = task['deadline'] * (task['execution'] + 0.5 * task['sslength'])
        elif prio_policy == 8:
            task['prio_shift'] = task['deadline'] * (task['execution'] + 0.15 * task['sslength'])
        elif prio_policy == 9:
            task['prio_shift'] = (task['deadline']+0.5*task['sslength'])*task['execution']
        elif prio_policy == 101:  # EDF eval
            task['prio_shift'] = task['deadline']


def RI_fixed(tasks, lam=0.01, abort=3, setprio=0):
    # priority shift is an additional parameter in task

    # Set priorities
    if setprio != 0:
        set_prio(tasks, setprio)

    # # Order task set by Priority
    # ord_tasks = sorted(tasks, key=lambda item: -item['prio_shift'])
    # Order task set inverse by deadline
    ord_tasks = tasks[::-1]

    # Initial response times.
    resp = []
    for task in ord_tasks:
        resp.append(task['deadline'])

    solved = False
    indrun = 0

    while indrun < abort and not solved:
        indrun += 1
        solved = True  # changed to false, if the iteration fails

        # Iterate over task indices.
        for indk in range(len(ord_tasks)):
            # Compute G.
            G = []
            for indi in range(len(ord_tasks)):
                G.append(min(
                    ord_tasks[indk]['period'] - ord_tasks[indi]['execution'],
                    ord_tasks[indk]['prio_shift'] - ord_tasks[indi]['prio_shift']))

            # Compute candidates.
            cand = []
            idx = 0  # running index
            valb = 0  # value of b
            step = lam * ord_tasks[indk]['deadline']
            if step <= 0:  # check if step is big enough
                print('step is too small')
                return False
            while valb < ord_tasks[indk]['deadline']:
                val = 0
                val += ceil(
                    (ord_tasks[indk]['deadline'] - valb)/ord_tasks[indk]['period']
                    ) * (ord_tasks[indk]['execution']+ord_tasks[indk]['sslength'])
                for indi in range(len(ord_tasks)):
                    if indi == indk:  # only consider i != k
                        continue
                    val += max(ceil(
                            (G[indi] + resp[indi] - valb)/ord_tasks[indi]['period']
                            ), 0) * ord_tasks[indi]['execution']
                val += valb

                cand.append(val)  # add canidate to list

                idx += 1
                valb = idx * step

            # Compare candidates.
            resp[indk] = min(cand)

            # Check schedulability condition.
            if resp[indk] > ord_tasks[indk]['deadline']:
                solved = False
                resp[indk] = ord_tasks[indk]['deadline']

    return solved
