"""Code to use pre-defined benchmark environment and setup slurm jobs for (parallel) scheduling."""

from __future__ import annotations

from tabflow_slurm.setup_slurm_base import BenchmarkSetup
from datetime import datetime

base_path = "/users/sdtemple/"
storage_path = "/lustre/scratch5/sdtemple/"
env = ".venv"
partial_path = "rvfl-proj/eiviani/tabarena-elm"
formatted_date = datetime.today().strftime("%y%m%d")

# # -- ELM Benchmark 04/03/2026
BenchmarkSetup(
    base_path = base_path,
    storage_path = storage_path,
    python_from_base_path = f"{partial_path}/{env}/bin/python",
    run_script_from_base_path = (
        f"{partial_path}/tabflow_slurm/run_tabarena_experiment.py"
    ),
    benchmark_name=f"elm_experiment_{formatted_date}_binary",
    openml_cache_from_base_path = f"{partial_path}/tabflow_slurm/openml-cache",
    configs_path_from_base_path = (
        f"{partial_path}/tabflow_slurm/benchmark_configs_"
    ),
    slurm_cpu_partition = "standard",
    slurm_extra_gres = False,
    models = [
        # -- Tree-based models
        ("CatBoost", "all"),
        ("EBM", "all"),
        ("ExtraTrees", "all"),
        ("LightGBM", "all"),
        ("RandomForest", "all"),
        ("XGBoost", "all"),
        # -- Baselines
        ("KNN", "all"),
        ("Linear", "all"),
        # -- Other
        ("xRFM", "all"),
        # ("ELM", "all"),
        # existing models …
        ("TabDPT", "all"),
        ("TabICL", "all"),
        ("TabPFNv2", "all"),
        ("Mitra", "all"),
        # -- Neural networks
        ("TabM", "all"),
        ("RealMLP", "all"),
        ("ModernNCA", "all"),
        ("FastaiMLP", "all"),
        ("TorchMLP", "all"),
    ],
    num_gpus=0,
    configs_per_job=20,
    problem_types_to_run="binary",
    tabarena_lite=True,
    n_random_configs=100
).setup_jobs()

# # -- ELM Benchmark 04/03/2026
BenchmarkSetup(
    base_path = base_path,
    storage_path = storage_path,
    python_from_base_path = f"{partial_path}/{env}/bin/python",
    run_script_from_base_path = (
        f"{partial_path}/tabflow_slurm/run_tabarena_experiment.py"
    ),
    benchmark_name=f"elm_experiment_{formatted_date}_multiclass",
    openml_cache_from_base_path = f"{partial_path}/tabflow_slurm/openml-cache",
    configs_path_from_base_path = (
        f"{partial_path}/tabflow_slurm/benchmark_configs_"
    ),
    slurm_cpu_partition = "standard",
    slurm_extra_gres = False,
    models = [
        # -- Tree-based models
        ("CatBoost", "all"),
        ("EBM", "all"),
        ("ExtraTrees", "all"),
        ("LightGBM", "all"),
        ("RandomForest", "all"),
        ("XGBoost", "all"),
        # -- Baselines
        ("KNN", "all"),
        ("Linear", "all"),
        # -- Other
        ("xRFM", "all"),
        # ("ELM", "all"),
        # existing models …
        ("TabDPT", "all"),
        ("TabICL", "all"),
        ("TabPFNv2", "all"),
        ("Mitra", "all"),
        # -- Neural networks
        ("TabM", "all"),
        ("RealMLP", "all"),
        ("ModernNCA", "all"),
        ("FastaiMLP", "all"),
        ("TorchMLP", "all"),
    ],
    num_gpus=0,
    configs_per_job=20,
    problem_types_to_run="multiclass",
    tabarena_lite=True,
    n_random_configs=100
).setup_jobs()

# # -- ELM Benchmark 04/03/2026
BenchmarkSetup(
    base_path = base_path,
    storage_path = storage_path,
    python_from_base_path = f"{partial_path}/{env}/bin/python",
    run_script_from_base_path = (
        f"{partial_path}/tabflow_slurm/run_tabarena_experiment.py"
    ),
    benchmark_name=f"elm_experiment_{formatted_date}_regression",
    openml_cache_from_base_path = f"{partial_path}/tabflow_slurm/openml-cache",
    configs_path_from_base_path = (
        f"{partial_path}/tabflow_slurm/benchmark_configs_"
    ),
    slurm_cpu_partition = "standard",
    slurm_extra_gres = False,
    models = [
        # -- Tree-based models
        ("CatBoost", "all"),
        ("EBM", "all"),
        ("ExtraTrees", "all"),
        ("LightGBM", "all"),
        ("RandomForest", "all"),
        ("XGBoost", "all"),
        # -- Baselines
        ("KNN", "all"),
        ("Linear", "all"),
        # -- Other
        ("xRFM", "all"),
        # ("ELM", "all"),
        # existing models …
        ("TabDPT", "all"),
        ("TabICL", "all"),
        ("TabPFNv2", "all"),
        ("Mitra", "all"),
        # -- Neural networks
        ("TabM", "all"),
        ("RealMLP", "all"),
        ("ModernNCA", "all"),
        ("FastaiMLP", "all"),
        ("TorchMLP", "all"),
    ],
    num_gpus=0,
    configs_per_job=20,
    
    problem_types_to_run="regression",
    tabarena_lite=True,
    n_random_configs=100
).setup_jobs()