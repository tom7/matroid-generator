import subprocess
import time
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

SEEDS = [1003, 1011, 1013, 1014, 1018, 1026, 1027, 1028, 976, 977, 981, 982]

# 1003
# 1011
# 1013
# 1014
# 1018
# 1026
# 1027
# 1028
# 976
# 977
# 981
# 982


# Number of times to repeat the whole benchmark
N_ITERATIONS = 5

# Path to the executable
BINARY = "build/IC"
# =================================================

def run_seed(seed):
    """Runs a single instance of IC and returns the elapsed time."""
    start_time = time.perf_counter()
    
    # Run the process, hiding its output so it doesn't mess up our console
    result = subprocess.run(
        [BINARY, str(seed)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    elapsed = time.perf_counter() - start_time
    
    if result.returncode != 0:
        print(f"\n[WARNING] Seed {seed} failed with return code {result.returncode}!")
        
    return seed, elapsed

def main():
    if len(SEEDS) == 0:
        print("Please add your seeds to the SEEDS array.")
        sys.exit(1)

    print(f"Starting benchmark: {len(SEEDS)} parallel parallel jobs, {N_ITERATIONS} iterations.")
    print(f"Command: {BINARY} <seed>\n")

    # Data structures to hold our results
    seed_times = {seed: [] for seed in SEEDS}
    batch_max_times = []

    # Run the iterations
    for i in range(1, N_ITERATIONS + 1):
        print(f"--- Iteration {i}/{N_ITERATIONS} ---")
        
        iteration_times = {}
        
        # Launch them all in parallel using exactly as many threads as we have seeds
        start_batch_time = time.perf_counter()
        with ThreadPoolExecutor(max_workers=len(SEEDS)) as executor:
            # Submit all tasks
            futures = {executor.submit(run_seed, seed): seed for seed in SEEDS}
            
            # As they finish, record the time and print progress
            for future in as_completed(futures):
                seed, elapsed = future.result()
                iteration_times[seed] = elapsed
                print(f"  Seed {seed:4d} finished in {elapsed:6.2f}s")
                
        batch_duration = time.perf_counter() - start_batch_time
        batch_max_times.append(batch_duration)
        
        # Store data for stats
        for seed in SEEDS:
            seed_times[seed].append(iteration_times[seed])
            
        print(f"-> Batch completed. Max wall-clock time: {batch_duration:6.2f}s\n")

    # ================= PRINT STATISTICS =================
    print("=================== FINAL STATISTICS ===================")
    print(f"{'Seed':<10} | {'Mean (s)':<10} | {'Variance':<10} | {'Std Dev (s)':<10}")
    print("-" * 48)
    
    for seed in SEEDS:
        times = seed_times[seed]
        mean_val = statistics.mean(times)
        
        # Variance and stdev require at least 2 data points
        if len(times) > 1:
            var_val = statistics.variance(times)
            std_val = statistics.stdev(times)
            print(f"{seed:<10} | {mean_val:<10.2f} | {var_val:<10.2f} | {std_val:<10.2f}")
        else:
            print(f"{seed:<10} | {mean_val:<10.2f} | {'N/A':<10} | {'N/A':<10}")
            
    print("=" * 48)
    
    batch_mean = statistics.mean(batch_max_times)
    if len(batch_max_times) > 1:
        batch_var = statistics.variance(batch_max_times)
        batch_std = statistics.stdev(batch_max_times)
        print(f"{'BATCH MAX':<10} | {batch_mean:<10.2f} | {batch_var:<10.2f} | {batch_std:<10.2f}")
    else:
        print(f"{'BATCH MAX':<10} | {batch_mean:<10.2f} | {'N/A':<10} | {'N/A':<10}")
    print("========================================================")

if __name__ == "__main__":
    main()
