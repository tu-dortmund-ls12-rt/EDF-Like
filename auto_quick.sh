#!/bin/bash
# Script to obtain the Paper results automatically.

# Set number of processes
if [ $# -gt 0 ]
then
  processes="$1"
else
  processes="0"  # This means: default number
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
