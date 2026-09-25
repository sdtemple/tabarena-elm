#!/bin/bash

set -euo pipefail

START=${1:-0}
FINAL=${2:-1} # change to value from stdout
CHUNK_SIZE=98 # one reserved for controller

EXPERIMENT=${3:-elm_experiment_260921}

BASEPATH=${4:-/users/sdtemple}
PARTIALPATH=${5:-rvfl-proj/eiviani/tabarena-elm/tabflow_slurm}

if (( START > FINAL )); then
    echo "All array tasks have been submitted."
    exit 0
fi

END=$((START + CHUNK_SIZE - 1))
if (( END > FINAL )); then
    END=$FINAL
fi

# Hugging Face Configuration
export HF_DATASETS_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

# OpenML Configuration
export OPENML_CACHEDIR=${BASEPATH}/${PARTIALPATH}/openml-cache
export OPENML_AVOID_DUPLICATE_RUNS="False"

# Tabular Models Configuration
export TABPFN_DISABLE_TELEMETRY=1

echo "Submitting array tasks${START}-${END}"

ARRAY_JOB_ID=$(
    sbatch --parsable \
        --array="${START}-${END}%${CHUNK_SIZE}" \
        --partition=standard \
        --cpus-per-task=8 \
        --mem=480G \
        --time=8:00:00 \
        --requeue \
        --job-name tabarena \
        --propagate=NONE \
        --export=ALL \
        --output="$BASEPATH/slurm_out/${EXPERIMENT}/%A/slurm-%A_%a.out" \
        $BASEPATH/$PARTIALPATH/submit_template.sh \
        $BASEPATH/$PARTIALPATH/slurm_run_data_${EXPERIMENT}.json
)

echo "Submitted array job${ARRAY_JOB_ID}"

NEXT_START=$((END + 1))

if (( NEXT_START <= FINAL )); then
    NEXT_JOB_ID=$(
        sbatch --parsable \
            --dependency="afterany:${ARRAY_JOB_ID}" \
            "$0" "${NEXT_START}" "${FINAL}" "${EXPERIMENT}"
    )

    echo "Queued controller${NEXT_JOB_ID} for tasks ${NEXT_START}-${FINAL}"
fi