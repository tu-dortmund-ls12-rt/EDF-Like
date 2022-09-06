# EDF-Like Scheduling Schedulability Evaluation

This repository is used to reproduce the evaluation from the paper

_EDF-Like Scheduling for Self-Suspending Real-Time Tasks_

for RTSS 2022.

This document is explaining how to use the artifact to repeat the experiments presented in the paper, i.e., Section 5.
Please cite the above paper when reporting, reproducing or extending the results.

Most parts of the program are based on
the [Evaluation Framework for Self-Suspending Task Systems](https://github.com/tu-dortmund-ls12-rt/SSSEvaluation).

The rest of the document is organized as follows:

1. [Environment Setup](#environment-setup)
2. [How to run the experiments](#how-to-run-the-experiments)
3. [Overview of the corresponding functions](#overview-of-the-corresponding-functions)
4. [Miscellaneous](#miscellaneous)

## Environment Setup

### Requirements

To run the evaluation [Python3.10](https://www.python.org/downloads/release/python-3100/) has to be installed on the
machine.
(Older versions of Python3 might work as well.)
Moreover, the following Python packages are required: TODO: Update

```
getopt
math
matplotlib
multiprocessing
numpy
os
pickle
random
statistics
sys
```

Assuming that Python 3.10 is installed in the targeted machine, to install the required packages: TODO: Update

```
python3.10 -m pip install matplotlib numpy
```

In case any dependent packages are missing, please install them accordingly.

TODO: CONTINUE HERE =====

TODO:

- troubleshooting: maximum number of processes may be limited by the operating system.

## File Structure

    .
    ├── res                     # Resource packages
    │   ├── benchmark.py        # Server and task creation
    │   ├── our_analysis.py     # Our analysis
    │   ├── plot.py             # Plotting functionality
    │   └── rtc_cb.py           # RTC-based analysis	
    ├── data                    # Evaluation data
    │   ├── 1setup              # Server and task specification
    │   ├── 2results            # Evaluation results
    │   └── 3plots              # Plots to present the results
    ├── main.py                 # Main function of the evaluation
    ├── auto.sh                 # bash-script to automize the evaluation
    └── README.md

Note that the source code of the case study part (Section 6.2) is contributed by a close-source project, so it is
excluded from this repository. Please contact the company, i.e., [EMVICORE GmbH](https://emvicore.com/de/) for further
information.

### Deployment

The following steps explain how to deploy this framework on a common PC:

First, clone the git repository or download
the [zip file](https://github.com/tu-dortmund-ls12-rt/unikernel-based_deferrable_server_analysis/archive/refs/heads/main.zip):

```
git clone https://github.com/tu-dortmund-ls12-rt/unikernel-based_deferrable_server_analysis.git
```

Move into the extracted/cloned folder, change the permissions of the script to be executable, and execute auto.sh
natively:

```
cd unikernel-based_deferrable_server_analysis
chmod 777 auto.sh
./auto.sh
```

## How to run the experiments

- To reproduce Figure 6 and 7 in the paper, ```auto.sh``` should be executed.
- The plotted figures can be found in the folder data/3plots:

Paper figure | Plot in data/3plots
---|---
Fig. 6 | 'plot2_num_servers_combined_util_servers=[0.1, 0.4].pdf'
Fig. 7 | 'plot3_num_servers=[10, 100]_util_servers_combined.pdf'

As a reference, we utilize a machine running Archlinux 5.17.3-arch1-1 x86_64 GNU/Linux,with i7-10610U CPU and 16 GB main
memory. It takes about 170 seconds with this machine to obtain these two figures, when set ```num_processors = 5```
in ```main.py```

## Overview of the corresponding functions

The following tables describe the mapping between content of our paper and the source code in this repository.

**Section 4.1** (RTC-based analysis):
On Paper | Source code --- | --- Theorem 4 | rtc_cb.wcrt_analysis_single()

**Section 4.2** (Our Analysis for Sporadic Tasks):
On Paper | Source code --- | --- Theorem 7 | our_analysis.wcrt_analysis_single()

## Miscellaneous

### Authors

* Kuan-Hsun Chen (University of Twente)
* Mario Günzel (TU Dortmund University)
* Boguslaw Jablkowski (EMVICORE GmbH)
* Markus Buschhoff (EMVICORE GmbH)
* Jian-Jia Chen (TU Dortmund University)

### Acknowledgments

This work has been supported by European Research Council (ERC) Consolidator Award 2019, as part of PropRT (Number
865170), and by Deutsche Forschungsgemeinschaft (DFG), as part of Sus-Aware (Project no. 398602212).

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.