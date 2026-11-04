#!/bin/bash
#!/usr/bin/env bash

shopt -s nullglob nocasematch
files=(slurm-*.out)

classify_final_line() {
    local last=$1

    if [[ $last == 'Metric error:'* ]]; then
        printf 'metric'
    elif [[ $last =~ \[repeated[[:space:]]+[0-9]+x[[:space:]]+across[[:space:]]+cluster\] ]]; then
        printf 'repeated'
    elif [[ $last =~ (^|[^[:alnum:]_])(segmentation[[:space:]]+fault|segfault)([^[:alnum:]_]|$) ]]; then
        printf 'segfault'
    elif [[ $last =~ (out[[:space:]-]*of[[:space:]-]*memory|ran[[:space:]]+out[[:space:]]+of[[:space:]]+memory|outofmemory(error)?|memoryerror|cannot[[:space:]]+allocate[[:space:]]+memory|(^|[^[:alnum:]_])oom([^[:alnum:]_]|$)) ]]; then
        printf 'memory'
    elif [[ $last =~ (time[[:space:]-]*limit|out[[:space:]-]*of[[:space:]-]*time|timed[[:space:]-]*out|timeout|walltime) ]]; then
        printf 'time'
    else
        printf 'other'
    fi
}

metric_count=0
repeated_count=0
memory_count=0
time_count=0
segfault_count=0
other_count=0

# Classify and count each file once.
for f in "${files[@]}"; do
    last=$(tail -n 1 -- "$f")
    case "$(classify_final_line "$last")" in
        metric)   ((++metric_count)) ;;
        repeated) ((++repeated_count)) ;;
        memory)   ((++memory_count)) ;;
        time)     ((++time_count)) ;;
        segfault) ((++segfault_count)) ;;
        other)    ((++other_count)) ;;
    esac
done

# Print each category with its individual file line counts.
for group in metric repeated memory time segfault other; do
    printf '\n=== %s ===\n' "$group"

    for f in "${files[@]}"; do
        last=$(tail -n 1 -- "$f")
        [[ $(classify_final_line "$last") == "$group" ]] || continue

        lines=$(wc -l < "$f")
        printf '%7s lines  %-35s  %s\n' "$lines" "$f" "$last"
    done
done

printf '\n=== summary ===\n'
printf 'Metric error:       %d\n' "$metric_count"
printf 'Repeated cluster:   %d\n' "$repeated_count"
printf 'Out of memory:      %d\n' "$memory_count"
printf 'Time limit/timeout: %d\n' "$time_count"
printf 'Segmentation fault: %d\n' "$segfault_count"
printf 'Other:              %d\n' "$other_count"
printf 'Total:              %d\n' \
    "$((metric_count + repeated_count + memory_count + time_count + segfault_count + other_count))"
