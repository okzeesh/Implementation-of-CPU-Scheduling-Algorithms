import matplotlib.pyplot as plt

# FCFS Scheduling Algorithm
def fcfs_scheduling(processes):
    n = len(processes)
    # Sort processes by arrival time
    processes.sort(key=lambda x: x['arrival_time'])

    completion_time = 0
    for i, p in enumerate(processes):
        # If CPU is idle, move to the process's arrival time
        if completion_time < p['arrival_time']:
            completion_time = p['arrival_time']
        # Add burst time to get completion time
        completion_time += p['burst_time']
        p['completion_time'] = completion_time
        # Calculate turnaround time
        p['turnaround_time'] = p['completion_time'] - p['arrival_time']
        # Calculate waiting time
        p['waiting_time'] = p['turnaround_time'] - p['burst_time']

    # Print results for each process
    print("FCFS Scheduling Results:")
    for p in processes:
        print(f"Process {p['pid']}: Completion Time: {p['completion_time']}, "
              f"Waiting Time: {p['waiting_time']}, Turnaround Time: {p['turnaround_time']}")

    return processes

# Plot bar charts for completion, waiting, and turnaround times
def plot_results(processes, title):
    # Get process IDs and their times
    pids = [p['pid'] for p in processes]
    completion_times = [p['completion_time'] for p in processes]
    waiting_times = [p['waiting_time'] for p in processes]
    turnaround_times = [p['turnaround_time'] for p in processes]

    fig, ax = plt.subplots(figsize=(10, 6))  # Create a new figure
    bar_width = 0.25  # Set bar width for the plot
    index = range(len(pids))  # X-axis positions for the bars

    # Plot Completion Time bars
    ax.bar([i - bar_width for i in index], completion_times, bar_width, label='Completion Time', color='blue')
    # Plot Waiting Time bars
    ax.bar(index, waiting_times, bar_width, label='Waiting Time', color='green')
    # Plot Turnaround Time bars
    ax.bar([i + bar_width for i in index], turnaround_times, bar_width, label='Turnaround Time', color='orange')

    # Adding annotations for CT, TAT, and WT
    for i in index:
        ax.text(i - bar_width, completion_times[i] + 0.2, str(completion_times[i]), ha='center', va='bottom')
        ax.text(i, waiting_times[i] + 0.2, str(waiting_times[i]), ha='center', va='bottom')
        ax.text(i + bar_width, turnaround_times[i] + 0.2, str(turnaround_times[i]), ha='center', va='bottom')

    # Set X-axis labels and chart title
    ax.set_xlabel('Process ID')
    ax.set_ylabel('Time (units)')
    ax.set_title(f'Scheduling Results: {title}')
    ax.set_xticks(index)  # Set X-axis tick positions
    ax.set_xticklabels(pids)  # Label X-axis ticks with process IDs
    ax.legend()  # Show the legend

    plt.grid(axis='y', linestyle='--')  # Add a grid for better readability
    plt.show()  # Display the plot

# Test Case 1
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

# Run FCFS Scheduling for Test Case 1 and plot results
print("---- Test Case 1: ----")
result_tc1 = fcfs_scheduling(processes_tc1)
plot_results(result_tc1, "Test Case 1")

# Run FCFS Scheduling for Test Case 2 and plot results
print("---- Test Case 2: ----")
result_tc2 = fcfs_scheduling(processes_tc2)
plot_results(result_tc2, "Test Case 2")
