import numpy as np

def read_input_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        num_processes = int(lines[0])
        arrival_mean, arrival_std = map(float, lines[1].split())
        burst_mean, burst_std = map(float, lines[2].split())
        priority_lambda = float(lines[3])
    return num_processes, arrival_mean, arrival_std, burst_mean, burst_std, priority_lambda

def generate_processes(num, arrival_mean, arrival_std, burst_mean, burst_std, priority_lambda):
    processes = []
    for i in range(num):
        arrival = max(0, int(np.random.normal(arrival_mean, arrival_std)))
        burst = max(1, int(np.random.normal(burst_mean, burst_std)))
        priority = np.random.poisson(priority_lambda)
        processes.append((f"P{i+1}", arrival, burst, priority))
    return processes

def write_output_file(filename, processes):
    with open(filename, 'w') as f:
        f.write(f"{len(processes)}\n")
        for p in processes:
            f.write(f"{p[0]} {p[1]} {p[2]} {p[3]}\n")

# --- Example run ---
input_file = 'input.txt'
output_file = 'processes.txt'

num, amean, astd, bmean, bstd, plambda = read_input_file(input_file)
processes = generate_processes(num, amean, astd, bmean, bstd, plambda)
write_output_file(output_file, processes)

print("✔️ Process generation completed. Check 'processes.txt'")

