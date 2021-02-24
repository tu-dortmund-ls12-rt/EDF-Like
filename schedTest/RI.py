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
        # EQDF Eval
        elif prio_policy == 201:
            task['prio_shift'] = task['deadline'] + (-1)*task['execution']
        elif prio_policy == 202:
            task['prio_shift'] = task['deadline'] + (0)*task['execution']
        elif prio_policy == 203:
            task['prio_shift'] = task['deadline'] + (1)*task['execution']
        elif prio_policy == 204:
            task['prio_shift'] = task['deadline'] + (10)*task['execution']
        elif prio_policy == 205:
            task['prio_shift'] = task['deadline'] + (100)*task['execution']
        elif prio_policy == 206:
            task['prio_shift'] = task['deadline'] + (1000)*task['execution']
        # EQDF Eval
        elif prio_policy == 301:
            task['prio_shift'] = task['deadline'] + (-1)*task['sslength']
        elif prio_policy == 302:
            task['prio_shift'] = task['deadline'] + (0)*task['sslength']
        elif prio_policy == 303:
            task['prio_shift'] = task['deadline'] + (1)*task['sslength']
        elif prio_policy == 304:
            task['prio_shift'] = task['deadline'] + (10)*task['sslength']
        elif prio_policy == 305:
            task['prio_shift'] = task['deadline'] + (100)*task['sslength']
        elif prio_policy == 306:
            task['prio_shift'] = task['deadline'] + (1000)*task['sslength']
        # Other Eval
        elif prio_policy == 401:
            task['prio_shift'] = 0
        elif prio_policy == 402:
            task['prio_shift'] = task['execution']
        elif prio_policy == 403:
            task['prio_shift'] = task['sslength']
        elif prio_policy == 404:
            task['prio_shift'] = task['deadline'] * task['execution']
        elif prio_policy == 405:
            task['prio_shift'] = task['deadline'] * task['sslength']
        elif prio_policy == 406:
            task['prio_shift'] = task['execution'] * task['sslength']


def RI_fixed(tasks, eta=0.01, depth=3, setprio=0):
    """Main function to run the schedulability test with fixed analysis window.
    - tasks = the task set under analysis
        - priority shift is an additional parameter in task
    - eta = determine the step size for the search algorithm
    - depth = number of improving runs in the search algorithm
    - setprio = set the priorities (if != 0) using the function set_prio
    """

    # Set priorities
    if setprio != 0:
        set_prio(tasks, setprio)

    # Order task set by deadline from big to small
    ord_tasks = sorted(tasks, key=lambda item: -item['deadline'])

    # Initial response time bounds.
    resp = []
    for task in ord_tasks:
        resp.append(task['deadline'])

    solved = False
    indrun = 0

    # Iterate over number of improving runs, until depth is reached or the test
    # returns True.
    while indrun < depth and not solved:
        indrun += 1
        solved = True  # will be changed to false, if the iteration fails

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
            step = eta * ord_tasks[indk]['deadline']  # step size
            if step <= 0:  # check if step is big enough
                print('step is too small')
                return False
            while valb < ord_tasks[indk]['deadline']:
                # Compute one candidate.
                val = 0
                val += ceil(
                    (ord_tasks[indk]['deadline']-valb)/ord_tasks[indk]['period']
                    )*(ord_tasks[indk]['execution']+ord_tasks[indk]['sslength'])
                for indi in range(len(ord_tasks)):
                    if indi == indk:  # only consider i != k
                        continue
                    val += max(ceil(
                            (G[indi] + resp[indi] - valb)/ord_tasks[indi]['period']
                            ), 0) * ord_tasks[indi]['execution']
                val += valb

                # Add candidate to list.
                cand.append(val)

                # Prepare next iteration.
                idx += 1
                valb = idx * step

            # Compare candidates.
            resp[indk] = min(cand)

            # Check schedulability condition.
            if resp[indk] > ord_tasks[indk]['deadline']:
                solved = False
                resp[indk] = ord_tasks[indk]['deadline']

    return solved


def RI_var(tasks, eta=0.01, max_a=1, depth=3, setprio=0):
    """Main function to run the schedulability test with variable analysis
    window.
    - tasks = the task set under analysis
        - priority shift is an additional parameter in task
    - eta = determine the step size for the search algorithm
    - max_a = maximum length of analysis window
    - depth = number of improving runs in the search algorithm
    - setprio = set the priorities (if != 0) using the function set_prio
    """

    # Set priorities
    if setprio != 0:
        set_prio(tasks, setprio)

    # Order task set by deadline from big to small.
    ord_tasks = sorted(tasks, key=lambda item: -item['deadline'])

    # Initial response time bounds.
    resp = []
    for task in ord_tasks:
        resp.append(task['deadline'])

    solved = False
    indrun = 0

    # Iterate over number of improving runs, until depth is reached or the test
    # returns True.
    while indrun < depth and not solved:
        indrun += 1
        solved = True  # will be changed to false, if the iteration fails

        # Iterate over task indices.
        for indk in range(len(ord_tasks)):
            # Compute G.
            G = []
            for indi in range(len(ord_tasks)):
                G.append(min(
                    ord_tasks[indk]['period'] - ord_tasks[indi]['execution'],
                    ord_tasks[indk]['prio_shift'] - ord_tasks[indi]['prio_shift']))

            # Iterate over analysis window length.
            resp_a = []  # response times for different a
            for inda in range(max_a + 1):

                # Compute candidates.
                cand = []
                idx = 0  # running index
                valb = 0  # value of b
                step = eta * ord_tasks[indk]['deadline']  # step size
                if step <= 0:  # check if step is big enough
                    print('step is too small')
                    return False
                while valb < inda*ord_tasks[indk]['period'] + ord_tasks[indk]['deadline']:
                    # Compute one candidate.
                    val = 0
                    val += min([inda+1, ceil(
                        (ord_tasks[indk]['deadline']-valb + inda * ord_tasks[indk]['period'])/ord_tasks[indk]['period']
                        )])*(ord_tasks[indk]['execution']+ord_tasks[indk]['sslength'])
                    for indi in range(len(ord_tasks)):
                        if indi == indk:  # only consider i != k
                            continue
                        val += max(ceil(
                                (G[indi] + resp[indi] - valb + inda*ord_tasks[indk]['period'])/ord_tasks[indi]['period']
                                ), 0) * ord_tasks[indi]['execution']
                    val += valb - inda * ord_tasks[indk]['period']

                    # Add candidate to list.
                    cand.append(val)

                    # Prepare next iteration.
                    idx += 1
                    valb = idx * step

                # Compare candidates.
                resp_cand = min(cand)  # candidate for a certain a
                resp_a.append(resp_cand)  # all candidates for different a

                # Check schedulability condition.
                if resp_cand <= ord_tasks[indk]['period']:
                    resp[indk] = min(resp_a)
                    break
                if resp_cand > ord_tasks[indk]['deadline'] or inda == max_a:
                    solved = False
                    resp[indk] = ord_tasks[indk]['deadline']
                    break
    return solved
