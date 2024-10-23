import matplotlib.pyplot as plt

def SJF(algorithm):
    algorithm.sort(key=lambda x: (x[1], x[2]))  # Sort first by arrival and then burst time
    time = 0  # Keeps track of the current time
    result = []  # Array to store the output
    remaining_algorithm = algorithm[:]

    while remaining_algorithm:
        available_algorithm = [p for p in remaining_algorithm if p[1] <= time]
        if available_algorithm:
            # Only choose the process with the shortest burst time
            shortest_path = min(available_algorithm, key=lambda x: x[2])
            # Remove the selected process from the remaining processes
            remaining_algorithm.remove(shortest_path)
            pid, arrival_time, burst_time = shortest_path  # Extract process ID, arrival time, and burst time
            # Calculating completion time for the process
            completion_time = time + burst_time
            # Calculating turnaround time: total time taken from arrival to completion
            turnaround = completion_time - arrival_time
            # Calculating waiting time: time the process spent waiting in the queue
            waiting = turnaround - burst_time
            result.append((pid, completion_time, waiting, turnaround))
            time = completion_time
        else:
            # If no process is available, increment time (CPU is idle)
            time += 1
    # Return the final result list with all process details
    return result

def plot_gantt_chart(result, title):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Setting up the Gantt chart
    for res in result:
        pid, completion_time, waiting, turnaround = res
        # Start time calculation
        start_time = completion_time - (waiting + (completion_time - turnaround))
        ax.barh(pid, completion_time - start_time, left=start_time, color='lightgreen')
        
        # Adding annotations for CT, TAT, and WT
        ax.text(completion_time + 0.5, pid, f'CT={completion_time}\nTAT={turnaround}\nWT={waiting}', 
                color='black', va='center', ha='left')

    # Adding a legend for CT, TAT, and WT
    ax.text(0, 1, 'Legend:\nCT = Completion Time\nTAT = Turnaround Time\nWT = Waiting Time', 
            transform=ax.transAxes, fontsize=10, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

    ax.set_xlabel('Time')
    ax.set_ylabel('Processes')
    ax.set_title(title)
    ax.set_yticks([res[0] for res in result])  # Set y-ticks to process IDs
    ax.set_yticklabels([f'P{res[0]}' for res in result])  # Set y-tick labels
    plt.grid(axis='x', linestyle='--')
    plt.show()

# Test Case 1: (PID, Arrival_Time, Burst_Time)
test_case_1 = [(1, 0, 6), (2, 1, 4), (3, 2, 8), (4, 3, 5)]
print("---- Test Case 1 ----")
result_tc1 = SJF(test_case_1)

# Print process details for Test Case 1
for res in result_tc1:
    print(f"Process {res[0]}: Completion Time = {res[1]}, Waiting Time = {res[2]}, Turnaround Time = {res[3]}")

# Plot the Gantt chart for Test Case 1
plot_gantt_chart(result_tc1, 'Gantt Chart for SJF Test Case 1')

# Test Case 2: (PID, Arrival_Time, Burst_Time)
test_case_2 = [(1, 0, 10), (2, 1, 4), (3, 2, 2), (4, 3, 6)]
print("---- Test Case 2 ----")
result_tc2 = SJF(test_case_2)

# Print process details for Test Case 2
for res in result_tc2:
    print(f"Process {res[0]}: Completion Time = {res[1]}, Waiting Time = {res[2]}, Turnaround Time = {res[3]}")

# Plot the Gantt chart for Test Case 2
plot_gantt_chart(result_tc2, 'Gantt Chart for SJF Test Case 2')
