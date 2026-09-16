#!/bin/bash

INPUT_JSON=${1:-slurm_run_data_elm_experiment_083126.json}
OUTPUT_JSON=${2:-slurm_run_data_elm_experiment_083126_short.json}
NUMJOBS=${3:-3}

python -m json.tool $INPUT_JSON > readable.json
python shrink_json.py readable.json $OUTPUT_JSON $NUMJOBS