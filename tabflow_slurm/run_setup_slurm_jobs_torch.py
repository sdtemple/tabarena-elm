"""Code to use pre-defined benchmark environment and setup slurm jobs for (parallel) scheduling."""

from __future__ import annotations

from tabflow_slurm.setup_slurm_base import BenchmarkSetup
from datetime import datetime

base_path = "/users/sdtemple/"
storage_path = "/lustre/scratch5/sdtemple/"
env = ".venv"
partial_path = "rvfl-proj/eiviani/tabarena-elm"
formatted_date = datetime.today().strftime("%y%m%d")

# # -- ELM Benchmark 07/30/2026
BenchmarkSetup(
    base_path = base_path,
    storage_path = storage_path,
    python_from_base_path = f"{partial_path}/{env}/bin/python",
    run_script_from_base_path = (
        f"{partial_path}/tabflow_slurm/run_tabarena_experiment_torch.py"
    ),
    benchmark_name=f"elm_experiment_{formatted_date}_torch",
    openml_cache_from_base_path = f"{partial_path}/tabflow_slurm/openml-cache",
    configs_path_from_base_path = (
        f"{partial_path}/tabflow_slurm/benchmark_configs_"
    ),
    slurm_cpu_partition = "standard",
    slurm_extra_gres = False,
    models = [
        ("ELMTorch", "all"),
        ("RVFLTorch", "all"),
        ("ELMPRTorch", "all"),
        ("RVFLPRTorch", "all"),
    ],
    num_gpus=0,
    configs_per_job=400,
    tabarena_lite=False,
    n_random_configs=100
).setup_jobs()
