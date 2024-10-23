import matplotlib.pyplot as plt

def RoundRobin(algorithm, time_span):
    queue = []  # This will store algorithm in the order of execution
    time = 0  # Keeps track of the current time where time=0
    result = []  # Array to store the output

    # Sort algorithm by arrival time
    algorithm.sort(key=lambda x: x['arrival_time'])
    
    # Dictionary to keep track of the remaining burst time for each process
    remaining_burst = {p['pid']: p['burst_time'] for p in algorithm}
    
    # Dictionary to keep track of the waiting time for each process
    waiting_time = {p['pid']: 0 for p in algorithm}
    
    # Initialize queue with processes that have arrived at time=0
    queue = [p for p in algorithm if p['arrival_time'] <= time]
    remaining_algorithm = algorithm[:]

    while remaining_algorithm:
        # Pop the first process from the queue
        if queue:
            current_process = queue.pop(0)
            pid = current_process['pid']
            arrival = current_process['arrival_time']
            burst = current_process['burst_time']

            if remaining_burst[pid] <= time_span:
                # Update the current time by adding the remaining burst time of the process
                time += remaining_burst[pid]
                remaining_burst[pid] = 0  # The process is finished
                
                # Calculating completion time for the process
                completion = time
                
                # Calculating turnaround time: total time taken from arrival to completion
                turnaround = completion - arrival
                
                # Calculating waiting time: time the process spent waiting in the queue
                waiting = turnaround - burst
                
                result.append((pid, completion, waiting, turnaround))
                remaining_algorithm.remove(current_process)
            else:
                # If the process cannot complete within the time span, it gets partial execution
                time += time_span
                remaining_burst[pid] -= time_span  # Reduce the remaining burst time
                
                # Put the process back in the queue to be executed in the next round
                queue.append(current_process)

            # Add newly available processes to the queue
            queue.extend([p for p in remaining_algorithm if p['arrival_time'] <= time and p not in queue])
        else:
            # If no processes are available, increment time (CPU is idle)
            time += 1

    return result

def plot_gantt_chart(result):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Setting up the Gantt chart
    current_time = 0
    for res in result:
        pid, completion_time, waiting, turnaround = res
        duration = completion_time - current_time
        ax.barh(pid, duration, left=current_time, color='lightblue')
        
        # Add text annotations for completion time, turnaround time, and waiting time
        ax.text(current_time + duration / 2, pid, 
                f'CT={completion_time}\nTAT={turnaround}\nWT={waiting}',
                color='black', va='center', ha='center')
        
        current_time = completion_time

    ax.set_xlabel('Time')
    ax.set_ylabel('Processes')
    ax.set_title('Gantt Chart for Round Robin Scheduling')
    ax.set_yticks([res[0] for res in result])  # Set y-ticks to process IDs
    ax.set_yticklabels([f'P{res[0]}' for res in result])  # Set y-tick labels
    plt.grid(axis='x', linestyle='--')
    plt.show()

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

# Time slice for Round Robin
time_slice = 2

# Run Round Robin Scheduling for Test Case 1 and plot results
print("---- Test Case 1 ----")
result_tc1 = RoundRobin(processes_tc1, time_slice)
for res in result_tc1:
    print(f"Process {res[0]}: Completion Time = {res[1]}, Waiting Time = {res[2]}, Turnaround Time = {res[3]}")
plot_gantt_chart(result_tc1)

# Run Round Robin Scheduling for Test Case 2 and plot results
print("---- Test Case 2 ----")
result_tc2 = RoundRobin(processes_tc2, time_slice)
for res in result_tc2:
    print(f"Process {res[0]}: Completion Time = {res[1]}, Waiting Time = {res[2]}, Turnaround Time = {res[3]}")
plot_gantt_chart(result_tc2)
