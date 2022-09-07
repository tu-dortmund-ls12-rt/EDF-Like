TODO:

- troubleshooting: maximum number of processes may be limited by the operating system.
- copy to private repo and remove branch "tuning"

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
matplotlib~=3.5.3
numpy~=1.23.2
```

Assuming that Python 3.10 is installed in the targeted machine, to install the required packages:

```
python3.10 -m pip install matplotlib numpy
```

In case any dependent packages are missing, please install them accordingly.

TODO: CONTINUE HERE =====

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

| Paper figure    | Plot in effsstsPlot/Data |
|-----------------|--------------------------|
| Fig. 5(a)       | 1_dm.pdf                 |
| Fig. 5(b)       | 2_edf.pdf                |
| Fig. 6(a)       | 3_eqdf.pdf               |
| Fig. 6(b)       | 4_saedf.pdf              |
| Fig. 7(a)       | 5a_arb_dl_dm.pdf         |
| Fig. 7(b)       | 5b_arb_dl_dm.pdf         |
| Fig. 8(a)       | 6a_arb_dl_edf.pdf        |
| Fig. 8(b)       | 6b_arb_dl_edf.pdf        |
| Fig. 9(a)       |                          |
| Fig. 9(b)       |                          |
| (not presented) | runtime_eval_1_avg.pdf   |
| (not presented) | runtime_eval_1_avg.pdf   |

TODO: CONTINUE ===================================================================

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

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details. # TODO: add license
file