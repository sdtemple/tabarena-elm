#!/bin/bash
basepath=${1:-/Users/sdtemple}
partialpath=${2:-rvfl-proj/eiviani/tabarena-elm/tabflow_slurm}
taskid=${3:-363612}
experiment=${4:-elm_experiment_083126}

python run_tabarena_experiment.py \
    --task_id $taskid \
    --fold 1 \
    --repeat 0 \
    --configs_yaml_file $basepath/$partialpath/benchmark_configs_$experiment.yaml \
    --config_index 0,1,2 \
    --openml_cache_dir $basepath/$partialpath/openml-cache/org/openml/www \
    --output_dir /$basepath/output/$experiment \
    --num_cpus 1 \
    --num_gpus 0 \
    --memory_limit 8 \
    --setup_ray_for_slurm_shared_resources_environment false \
    --ignore_cache true \
    --sequential_local_fold_fitting false