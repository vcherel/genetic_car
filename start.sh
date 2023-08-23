#!/bin/bash

. $PWD"/miniconda/etc/profile.d/conda.sh"

conda activate sim_gen
python3 src/main.py
