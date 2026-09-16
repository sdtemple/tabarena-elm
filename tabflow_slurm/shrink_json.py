import json
import sys

# 1. Configuration
INPUT_FILE = sys.argv[1]           # Change this to your source JSON file name
OUTPUT_FILE = sys.argv[2]  # The name of your new, smaller JSON file
MAX_JOBS_TO_KEEP = sys.argv[3]               # Adjust this number to keep more or fewer jobs

MAX_JOBS_TO_KEEP = int(MAX_JOBS_TO_KEEP)

try:
    # 2. Load the original single-line JSON
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)
    
    # 3. Handle the "jobs" list contraction
    if "jobs" in data and isinstance(data["jobs"], list):
        original_count = len(data["jobs"])
        
        # Slice the list to keep only the first few items
        data["jobs"] = data["jobs"][:MAX_JOBS_TO_KEEP]
        
        print(f"Success! Sliced 'jobs' down from {original_count} to {len(data['jobs'])} items.")
    else:
        print("Warning: Could not find a 'jobs' list in the JSON file.")

    # 4. Save the result with clean indentation and newlines
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"Saved readable, shrunk file to: {OUTPUT_FILE}")

except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}. Make sure the file is valid.")
except FileNotFoundError:
    print(f"Error: The file '{INPUT_FILE}' was not found.")
