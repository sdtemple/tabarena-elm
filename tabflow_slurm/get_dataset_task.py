import openml
import pandas as pd

# 1. Fetch the official TabArena-v0.1 benchmark suite
suite = openml.study.get_suite(457)

# 2. Extract the 1-to-1 mapping
mapping = []
for task_id in suite.tasks:
    print(task_id)
    try:
        # Fetch minimal task metadata (fast, doesn't download the heavy data)
        task = openml.tasks.get_task(task_id, 
                                     download_data=False,
                                     download_qualities=False,
                                     download_splits=False,
                                     )
        mapping.append({
            "task_id": task_id,
            "dataset_id": task.dataset_id,
            "dataset_name": task.get_dataset().name
        })
    except Exception as e:
        print(f"Skipping task {task_id} due to error: {e}")

# 3. View the results as a clean table
df = pd.DataFrame(mapping)
df.to_csv("tabarena_dataset_task.tsv",sep='\t',index=False)
print(df.to_string(index=False))