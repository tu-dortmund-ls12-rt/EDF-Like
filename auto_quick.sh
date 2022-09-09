#!/bin/bash
# Script to run the RTSS experiments with faster configuration, to test if the program runs without errors.

# Set number of processes
if [ $# -gt 0 ]
then
  processes="$1"
else
  processes="0"  # This means: default number, which is 6
fi

# Run performance comparison
python3 main.py -q "-p$processes" 1
python3 main.py -q "-p$processes" 2
python3 main.py -q "-p$processes" 3
python3 main.py -q "-p$processes" 4
python3 main.py -q "-p$processes" 5a
python3 main.py -q "-p$processes" 5b
python3 main.py -q "-p$processes" 6a
python3 main.py -q "-p$processes" 6b

# Run runtime evaluation
python3 runtime.py -q "-p$processes" 1

# Run comparison with arbitrary DL FP analysis
python3 comparison.py -q "-p$processes" 1
python3 comparison.py -q "-p$processes" 2