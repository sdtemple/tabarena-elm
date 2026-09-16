# how many unique task ids are in the json file

import numpy as np
import sys


fn = sys.argv[1]

with open(fn, 'r') as f:
    line = f.readline()

line_split = line.split("task_id")[1:]

keep = []
for _ in line_split:
    keep.append(_[3:9])
keep = np.unique(keep)

print(f"There are {len(keep)} unique task IDs")
print()
for _ in keep:
    print(f"Task {_}\n")
