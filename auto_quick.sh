#!/bin/bash

# Script to obtain the Paper results automatically.

python3 main.py -q 1
python3 main.py -q 2
python3 main.py -q 3
python3 main.py -q 4
python3 main.py -q 5a
python3 main.py -q 5b
python3 main.py -q 6a
python3 main.py -q 6b

python3 runtime.py -q 1
