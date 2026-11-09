import openml

# task_ids = [363615, 363621]  # replace with your TabArena task IDs
task_ids = range(363613, 363713, 1)

for task_id in task_ids:
    task = openml.tasks.get_task(task_id)
    dataset = task.get_dataset()

    qualities = dataset.qualities
    print(
        f"{task_id:>6}  {dataset.name:<45} "
        f"rows={qualities.get('NumberOfInstances')}  "
        f"features={qualities.get('NumberOfFeatures')}  "
        f"missing={qualities.get('NumberOfMissingValues')} "
        f"values={qualities.get('NumberOfInstances') * qualities.get("NumberOfFeatures")}"
    )