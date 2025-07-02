from collections import deque

# -------- قراءة العمليات من ملف --------
def read_processes(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        n = int(lines[0])
        processes = []
        for line in lines[1:]:
            pid, arrival, burst, priority = line.strip().split()
            processes.append({
                "id": pid,
                "arrival": int(arrival),
                "burst": int(burst),
                "priority": int(priority)
                
            })
    return processes

# -------- خوارزمية FCFS --------
def fcfs_scheduler(processes):
    processes.sort(key=lambda p: p['arrival'])
    time = 0
    result = []

    for p in processes:
        start_time = max(time, p['arrival'])
        finish_time = start_time + p['burst']
        waiting_time = start_time - p['arrival']
        turnaround_time = finish_time - p['arrival']

        result.append({
            'id': p['id'],
            'arrival': p['arrival'],
            'burst': p['burst'],
            'waiting': waiting_time,
            'turnaround': turnaround_time,
            'finish': finish_time,
            'start': start_time 
        })

        time = finish_time

    return result

# -------- خوارزمية SJF --------
def sjf_scheduler(processes):
    processes.sort(key=lambda p: (p['arrival'], p['burst']))
    completed = []
    ready_queue = []
    time = 0
    index = 0
    n = len(processes)

    while len(completed) < n:
        while index < n and processes[index]['arrival'] <= time:
            ready_queue.append(processes[index])
            index += 1

        if ready_queue:
            ready_queue.sort(key=lambda p: p['burst'])
            current = ready_queue.pop(0)
        else:
            time = processes[index]['arrival']
            continue

        start_time = time
        finish_time = start_time + current['burst']
        waiting_time = start_time - current['arrival']
        turnaround_time = finish_time - current['arrival']

        completed.append({
            'id': current['id'],
            'arrival': current['arrival'],
            'burst': current['burst'],
            'waiting': waiting_time,
            'turnaround': turnaround_time,
            'finish': finish_time,
            'start': start_time 
        })

        time = finish_time

    return completed

# -------- خوارزمية Priority --------
def priority_scheduler(processes):
    processes.sort(key=lambda p: (p['arrival'], p['priority']))
    completed = []
    ready_queue = []
    time = 0
    index = 0
    n = len(processes)

    while len(completed) < n:
        while index < n and processes[index]['arrival'] <= time:
            ready_queue.append(processes[index])
            index += 1

        if ready_queue:
            ready_queue.sort(key=lambda p: p['priority'])
            current = ready_queue.pop(0)
        else:
            time = processes[index]['arrival']
            continue

        start_time = time
        finish_time = start_time + current['burst']
        waiting_time = start_time - current['arrival']
        turnaround_time = finish_time - current['arrival']

        completed.append({
            'id': current['id'],
            'arrival': current['arrival'],
            'burst': current['burst'],
            'waiting': waiting_time,
            'turnaround': turnaround_time,
            'finish': finish_time,
            'start': start_time 
            
        })

        time = finish_time

    return completed

# -------- خوارزمية Round Robin --------
def round_robin_scheduler(processes, quantum):
    from collections import deque
    queue = deque()
    time = 0
    remaining = {p['id']: p['burst'] for p in processes}
    arrived = []
    completed = []
    timeline = []
    index = 0
    n = len(processes)

    processes.sort(key=lambda p: p['arrival'])

    while len(completed) < n:
        while index < n and processes[index]['arrival'] <= time:
            queue.append(processes[index])
            arrived.append(processes[index]['id'])
            index += 1

        if not queue:
            time = processes[index]['arrival']
            continue

        current = queue.popleft()
        pid = current['id']
        exec_time = min(quantum, remaining[pid])
        start_time = time
        time += exec_time
        remaining[pid] -= exec_time

        timeline.append({
            'id': pid,
            'start': start_time,
            'finish': time
        })

        while index < n and processes[index]['arrival'] <= time:
            if processes[index]['id'] not in arrived:
                queue.append(processes[index])
                arrived.append(processes[index]['id'])
            index += 1

        if remaining[pid] > 0:
            queue.append(current)
        else:
            turnaround_time = time - current['arrival']
            waiting_time = turnaround_time - current['burst']
            completed.append({
                'id': pid,
                'arrival': current['arrival'],
                'burst': current['burst'],
                'waiting': waiting_time,
                'turnaround': turnaround_time,
                'finish': time,
                'start': start_time 
            })

    return completed, timeline

# -------- طباعة النتائج --------
def print_output(result, title):
    print(f"\n{title} Scheduling Result:")
    print("ID  Arrival  Burst  Waiting  Turnaround  Finish")
    for p in result:
        print(f"{p['id']:>2}  {p['arrival']:>7}  {p['burst']:>5}  {p['waiting']:>7}  {p['turnaround']:>10}  {p['finish']:>6}")

# -------- تشغيل البرنامج --------
if __name__ == "__main__":
    input_file = "processes.txt"
    quantum = 2  # تقدر تغيره حسب اللي عايزه

    processes = read_processes(input_file)

    print_output(fcfs_scheduler(processes.copy()), "FCFS")
    print_output(sjf_scheduler(processes.copy()), "SJF")
    print_output(priority_scheduler(processes.copy()), "Priority")
    print_output(round_robin_scheduler(processes.copy(), quantum), f"Round Robin (Q={quantum})")
