for directory in */; 
    do printf '%s: ' "${directory%/}" >> completed_results_pkl.txt ; 
    find "$directory" -mindepth 2 -maxdepth 2 -type d | wc -l >> completed_results_pkl.txt; 
done