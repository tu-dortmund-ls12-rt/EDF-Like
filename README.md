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
Moreover, the following Python packages are required:

```
matplotlib
numpy
```

Assuming that Python 3 is installed in the targeted machine, to install the required packages:

```
python3 -m pip install matplotlib numpy
```

In case any dependent packages are missing, please install them accordingly.

## File Structure

    .
    ├── README.md             
    ├── auto_full.sh          # bash-script to automize the full evaluation
    ├── auto_quick.sh         # bash-script to run evaluation with faster configuration (for testing)
    ├── effsstsPlot           # Plotting
    │ ├── __init__.py
    │ ├── Data                # Evaluation data and plots
    │ └── effsstsPlot.py      # Plot functionality
    ├── main.py               # Main function of the evaluation
    ├── runtime.py            # Main function to evaluate the runtime
    └── schedTest             # Schedulability tests and benchmark
      ├── __init__.py
      ├── EL.py               # Our analysis for EDF-Like scheduling
      ├── FP_Analyses.py
      ├── RTEDF.py
      ├── SCEDF.py
      ├── UDLEDF.py
      ├── UUniFast.py
      ├── UniFramework.py
      ├── WLAEDF.py
      ├── functions.py
      └── tgPath.py           # Benchmark

### Deployment

The following steps explain how to deploy this framework on a common PC:

First, clone the git repository or download
the [zip file](https://github.com/tu-dortmund-ls12-rt/EDF-Like/archive/refs/heads/main.zip):

```
git clone https://github.com/tu-dortmund-ls12-rt/EDF-Like.git
```

Move into the extracted/cloned folder, change the permissions of the script to be executable:

```
cd EDF-Like
chmod 777 auto_full.sh
chmod 777 auto_quick.sh
```

## How to run the experiments

- To test if the evaluation runs without errors, ```auto_quick.sh``` can be executed (run ```./auto_quick.sh```)
- To reproduce the evaluation from the RTSS paper, ```auto_full.sh``` can be executed (run ```./auto_full.sh```)
- The plotted figures can be found in the folder ```effsstsPlot/Data```:

| Paper figure    | Plot in effsstsPlot/Data            |
|-----------------|-------------------------------------|
| Fig. 5(a)       | 1_dm.pdf                            |
| Fig. 5(b)       | 2_edf.pdf                           |
| Fig. 6(a)       | 3_eqdf.pdf                          |
| Fig. 6(b)       | 4_saedf.pdf                         |
| Fig. 7(a)       | 5a_arb_dl_dm.pdf                    |
| Fig. 7(b)       | 5b_arb_dl_dm.pdf                    |
| Fig. 8(a)       | 6a_arb_dl_edf.pdf                   |
| Fig. 8(b)       | 6b_arb_dl_edf.pdf                   |
| Fig. 9(a)       | comparison_arb_DL_GUC21_0.8-1.2.pdf |
| Fig. 9(b)       | comparison_arb_DL_GUC21_1.0-1.2.pdf |
| (not presented) | runtime_eval_1_avg.pdf              |
| (not presented) | runtime_eval_1_avg.pdf              |

To speed up the evaluation, the multiprocessing package is utilized which generates several concurrent processes to run
the schedulability tests. For the quick evaluation there are 6 concurrent processes, while for the full evaluation there
are 100 concurrent processes. The number of concurrent processes can be modified by passing the desired number to the
bash script, i.e.,
``./auto_quick.sh <number processes>`` or ``./auto_full.sh <number processes>``. Please note that the maximum number of
processes may be limited by the operating system. Hence, if you receive an error
like ``OSError: [Errno 24] Too many open files`` please try to reduce the number of processes.

As a reference, we utilize a machine running Debian 4.19.98-1 (2020-01-26) x86_64 GNU/Linux, with 2 x AMD EPYC 7742
64-Core Processor (64 Cores, 128 Threads), i.e., in total 256 Threads with 2,25GHz and 256GB RAM.
Running ```./auto_full.sh``` (i.e., with 100 processes) takes about 1 hour with this machine. TODO: Update

## Overview of the corresponding functions

The following table describes the mapping between content of our paper and the source code in this repository.

| On Paper   | Pseudocode  | Source Code in folder schedTest: |
|------------|-------------|----------------------------------|
| Theorem 12 | Algorithm 1 | EL.EL_fixed                      |
| Theorem 15 | Algorithm 2 | EL.EL_var                        |

## Miscellaneous

### Authors

* Mario Günzel (TU Dortmund University)
* Georg von der Brüggen (TU Dortmund University)
* Kuan-Hsun Chen (University of Twente)
* Jian-Jia Chen (TU Dortmund University)

### Acknowledgments

This work has been supported by Deutsche Forschungsgemeinschaft (DFG), as part of Sus-Aware (Project No. 398602212).
This result is part of a project (PropRT) that has received funding from the European Research Council (ERC) under the
European Union’s Horizon 2020 research and innovation programme (grant agreement No. 865170).

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.