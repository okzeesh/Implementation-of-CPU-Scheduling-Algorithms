import matplotlib.pyplot as plt
from copy import deepcopy

# Function to calculate average waiting time and turnaround time
def calculate_averages(processes):
    n = len(processes)
    total_waiting_time = sum([p['waiting_time'] for p in processes])
    total_turnaround_time = sum([p['turnaround_time'] for p in processes])
    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n
    return avg_waiting_time, avg_turnaround_time

# FCFS Scheduling Algorithm
def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x['arrival_time'])
    completion_time = 0
    for p in processes:
        if completion_time < p['arrival_time']:
            completion_time = p['arrival_time']
        completion_time += p['burst_time']
        p['completion_time'] = completion_time
        p['turnaround_time'] = p['completion_time'] - p['arrival_time']
        p['waiting_time'] = p['turnaround_time'] - p['burst_time']
    return processes

# SJF Scheduling Algorithm (Non-Preemptive)
def sjf_scheduling(processes):
    processes.sort(key=lambda x: (x['arrival_time'], x['burst_time']))
    completion_time = 0
    for p in processes:
        if completion_time < p['arrival_time']:
            completion_time = p['arrival_time']
        completion_time += p['burst_time']
        p['completion_time'] = completion_time
        p['turnaround_time'] = p['completion_time'] - p['arrival_time']
        p['waiting_time'] = p['turnaround_time'] - p['burst_time']
    return processes

# Round Robin Scheduling Algorithm
def round_robin_scheduling(processes, quantum):
    n = len(processes)
    remaining_burst_time = [p['burst_time'] for p in processes]
    waiting_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    time = 0

    while any(remaining_burst_time):
        for i in range(n):
            if remaining_burst_time[i] > 0:
                if remaining_burst_time[i] > quantum:
                    time += quantum
                    remaining_burst_time[i] -= quantum
                else:
                    time += remaining_burst_time[i]
                    remaining_burst_time[i] = 0
                    completion_time[i] = time
                    turnaround_time[i] = completion_time[i] - processes[i]['arrival_time']
                    waiting_time[i] = turnaround_time[i] - processes[i]['burst_time']

    for i, p in enumerate(processes):
        p['completion_time'] = completion_time[i]
        p['waiting_time'] = waiting_time[i]
        p['turnaround_time'] = turnaround_time[i]

    return processes

# Function to run all three algorithms and compare results
def compare_algorithms(processes, quantum):
    processes_fcfs = deepcopy(processes)
    processes_sjf = deepcopy(processes)
    processes_rr = deepcopy(processes)

    # Run FCFS
    result_fcfs = fcfs_scheduling(processes_fcfs)
    avg_waiting_fcfs, avg_turnaround_fcfs = calculate_averages(result_fcfs)

    # Run SJF
    result_sjf = sjf_scheduling(processes_sjf)
    avg_waiting_sjf, avg_turnaround_sjf = calculate_averages(result_sjf)

    # Run Round Robin
    result_rr = round_robin_scheduling(processes_rr, quantum)
    avg_waiting_rr, avg_turnaround_rr = calculate_averages(result_rr)

    # Print averages
    print(f"FCFS -> Avg Waiting Time: {avg_waiting_fcfs:.2f}, Avg Turnaround Time: {avg_turnaround_fcfs:.2f}")
    print(f"SJF  -> Avg Waiting Time: {avg_waiting_sjf:.2f}, Avg Turnaround Time: {avg_turnaround_sjf:.2f}")
    print(f"RR   -> Avg Waiting Time: {avg_waiting_rr:.2f}, Avg Turnaround Time: {avg_turnaround_rr:.2f}")

    # Visualization
    algorithms = ['FCFS', 'SJF', 'Round Robin']
    avg_waiting_times = [avg_waiting_fcfs, avg_waiting_sjf, avg_waiting_rr]
    avg_turnaround_times = [avg_turnaround_fcfs, avg_turnaround_sjf, avg_turnaround_rr]

    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(algorithms))

    # Plot bar charts for waiting time and turnaround time
    ax.bar(index, avg_waiting_times, bar_width, label='Avg Waiting Time', color='green')
    ax.bar([i + bar_width for i in index], avg_turnaround_times, bar_width, label='Avg Turnaround Time', color='blue')

    ax.set_xlabel('Scheduling Algorithms')
    ax.set_ylabel('Time (units)')
    ax.set_title('Comparison of CPU Scheduling Algorithms')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(algorithms)
    ax.legend()

    plt.show()

# Gantt Chart Plotting Function
def plot_gantt_chart(processes, algorithm_name):
    fig, ax = plt.subplots(figsize=(10, 6))

    current_time = 0
    for p in processes:
        pid = p['pid']
        burst_time = p['burst_time']
        arrival_time = p['arrival_time']
        
        # Calculate duration
        duration = p['completion_time'] - current_time
        ax.barh(pid, duration, left=current_time, color='lightblue')
        
        # Add text annotations for CT, TAT, and WT
        ax.text(current_time + duration / 2, pid, 
                f'CT={p["completion_time"]}\nTAT={p["turnaround_time"]}\nWT={p["waiting_time"]}',
                color='black', va='center', ha='center')
        
        current_time = p['completion_time']

    ax.set_xlabel('Time')
    ax.set_ylabel('Processes')
    ax.set_title(f'Gantt Chart for {algorithm_name}')
    ax.set_yticks([p['pid'] for p in processes])
    ax.set_yticklabels([f'P{p["pid"]}' for p in processes])
    plt.grid(axis='x', linestyle='--')
    plt.show()

# Test Case 1: Basic Test Case
processes_tc1 = [
    {'pid': 1, 'arrival_time': 0, 'burst_time': 6},
    {'pid': 2, 'arrival_time': 1, 'burst_time': 4},
    {'pid': 3, 'arrival_time': 2, 'burst_time': 8},
    {'pid': 4, 'arrival_time': 3, 'burst_time': 5}
]

# Test Case 2
processes_tc2 = [
    {'pid': 1, 'arrival_time': 0, 'burst_time': 10},
    {'pid': 2, 'arrival_time': 1, 'burst_time': 4},
    {'pid': 3, 'arrival_time': 2, 'burst_time': 2},
    {'pid': 4, 'arrival_time': 3, 'burst_time': 6}
]

# Compare FCFS, SJF, and Round Robin for Test Case 1 (Quantum = 4)
print("---- Test Case 1: Basic Test Case ----")
compare_algorithms(processes_tc1, quantum=4)
plot_gantt_chart(fcfs_scheduling(deepcopy(processes_tc1)), 'FCFS')
plot_gantt_chart(sjf_scheduling(deepcopy(processes_tc1)), 'SJF')
plot_gantt_chart(round_robin_scheduling(deepcopy(processes_tc1), quantum=4), 'Round Robin')

# Compare FCFS, SJF, and Round Robin for Test Case 2 (Quantum = 4)
print("---- Test Case 2: Processes Arriving at the Same Time ----")
compare_algorithms(processes_tc2, quantum=4)
plot_gantt_chart(fcfs_scheduling(deepcopy(processes_tc2)), 'FCFS')
plot_gantt_chart(sjf_scheduling(deepcopy(processes_tc2)), 'SJF')
plot_gantt_chart(round_robin_scheduling(deepcopy(processes_tc2), quantum=4), 'Round Robin')
