from pathlib import Path
import pickle
import pandas as pd
import sys

folder_input, file_output = sys.argv[1:] 

wanted_keys = {
    "framework": None,
    "problem_type": None,
    "task_metadata": ["tid", "name", "fold"],
    "time_train_s": None,
    "time_infer_s": None,
    "memory_usage": ["peak_mem_cpu"],
    "metric_error": None,
    "metric_error_val": None,
    "metric": None,
}

header = [k for k, v in wanted_keys.items() if v is not None]
for k, v in wanted_keys.items():
    header.extend(v)

rows = {k: [] for k in header}

for path in Path(".").glob(f"{folder_input}/*/*/*/results.pkl"):  # adjust pattern as needed
    try:
        with path.open("rb") as f:
            result = pickle.load(f)

        row = {key: result.get(key) for key in wanted_keys.keys()}
        for k, v in row.items():
            if wanted_keys[k] is None:
                rows[k].append(v)
            else:
                for a, b in row.items():
                    try:
                        rows[a].append(b)
                    except:
                        pass

    except (OSError, pickle.UnpicklingError, EOFError) as exc:
        print(f"Skipping {path}: {exc}")

df = pd.DataFrame(rows)
df.to_parquet(file_output, index=False)