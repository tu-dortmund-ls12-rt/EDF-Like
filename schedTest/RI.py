from math import ceil  # ceiling function


def RI_fixed(tasks, lam=0.01, abort=3):
    # priority shift is an additional parameter in task

    # # Order task set by Priority
    # ord_tasks = sorted(tasks, key=lambda item: -item['prio_shift'])
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
