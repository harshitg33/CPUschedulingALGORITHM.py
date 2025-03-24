# Intelligent CPU Scheduler Simulator
# simulator for CPU scheduling algorithms (FCFS, SJF, Round
# Robin, Priority Scheduling) with real-time visualizations. The simulator should allow
# users to input processes with arrival times, burst times, and priorities and visualize Gantt
# charts and performance metrics like average waiting time and turnaround time.

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk

# Process class jo ek process ko represent karta hai
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid  # Process ID
        self.arrival_time = arrival_time  # Jab process aata hai
        self.burst_time = burst_time  # CPU time jo process ko chahiye
        self.priority = priority  # Priority level (Priority Scheduling ke liye)
        self.remaining_time = burst_time  # Round Robin scheduling ke liye
        self.start_time = -1  # Jab process pehli baar CPU pe chalta hai
        self.completion_time = -1  # Jab process finish hota hai
        self.waiting_time = 0  # Queue me wait karne ka samay
        self.turnaround_time = 0  # Arrival se completion tak ka total samay

# First Come, First Served (FCFS) Scheduling Algorithm
# Ye algorithm jo pehle aata hai use pehle execute karta hai

def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)  # Arrival time ke hisaab se sort karte hain
    time = 0
    gantt_chart = []

    for process in processes:
        if time < process.arrival_time:
            time = process.arrival_time  # Agar CPU idle hai toh time aage badhao
        process.start_time = time
        process.completion_time = time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        gantt_chart.append((process.pid, time, process.completion_time))
        time += process.burst_time

    return processes, gantt_chart

# Shortest Job First (SJF) Scheduling Algorithm
# Isme sabse chhoti burst time wale process ko pehle execute karte hain

def sjf_scheduling(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    completed = 0
    time = 0
    gantt_chart = []
    ready_queue = []

    while completed < len(processes):
        available_processes = [p for p in processes if p.arrival_time <= time and p not in ready_queue]
        ready_queue.extend(available_processes)
        ready_queue.sort(key=lambda x: x.burst_time)  # Sabse chhoti burst time wale process ko pehle lete hain

        if ready_queue:
            process = ready_queue.pop(0)
            process.start_time = time
            process.completion_time = time + process.burst_time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            gantt_chart.append((process.pid, time, process.completion_time))
            time += process.burst_time
            completed += 1
        else:
            time += 1  # Agar koi process ready nahi hai toh time badhao

    return processes, gantt_chart

# Round Robin Scheduling Algorithm
# Isme har process ko fixed time quantum diya jata hai

def round_robin_scheduling(processes, quantum):
    time = 0
    gantt_chart = []
    processes.sort(key=lambda x: x.arrival_time)  # Arrival time ke hisaab se sort karte hain

    for process in processes:
        process.remaining_time = process.burst_time  # Remaining time reset karte hain

    while any(p.remaining_time > 0 for p in processes):
        for process in processes:
            if process.remaining_time > 0:
                start_time = time
                execution_time = min(process.remaining_time, quantum)  # Quantum time ya remaining time jitna ho
                time += execution_time
                process.remaining_time -= execution_time
                if process.remaining_time == 0:
                    process.completion_time = time
                    process.turnaround_time = process.completion_time - process.arrival_time
                    process.waiting_time = process.turnaround_time - process.burst_time
                gantt_chart.append((process.pid, start_time, time))

    return processes, gantt_chart

# Priority Scheduling Algorithm
# Ye algorithm priority ke basis pe process execute karta hai

def priority_scheduling(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.priority))  # Priority aur arrival time ke hisaab se sort
    time = 0
    gantt_chart = []

    for process in processes:
        if time < process.arrival_time:
            time = process.arrival_time  # Agar CPU idle hai toh time aage badhao
        process.start_time = time
        process.completion_time = time + process.burst_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        gantt_chart.append((process.pid, time, process.completion_time))
        time += process.burst_time

    return processes, gantt_chart

# Gantt Chart draw karne ka function

def draw_gantt_chart(gantt_chart, title):
    fig, ax = plt.subplots()
    for process_id, start, end in gantt_chart:
        ax.barh(1, end - start, left=start, edgecolor='black', label=f'P{process_id}')
    plt.xlabel('Time')
    plt.ylabel('Process')
    plt.title(title)
    plt.grid()
    plt.show()

# Example Usage
if __name__ == "__main__":
    processes = [
        Process(1, 0, 8, 2),  # Process 1: Arrives at 0, runs for 8 units, priority 2
        Process(2, 1, 4, 1),  # Process 2: Arrives at 1, runs for 4 units, priority 1
        Process(3, 2, 9, 3),  # Process 3: Arrives at 2, runs for 9 units, priority 3
        Process(4, 3, 5, 4)   # Process 4: Arrives at 3, runs for 5 units, priority 4
    ]

    scheduled_processes, gantt = fcfs_scheduling(processes)
    draw_gantt_chart(gantt, "FCFS Scheduling")

    scheduled_processes, gantt = sjf_scheduling(processes)
    draw_gantt_chart(gantt, "SJF Scheduling")

    scheduled_processes, gantt = round_robin_scheduling(processes, quantum=3)
    draw_gantt_chart(gantt, "Round Robin Scheduling")

    scheduled_processes, gantt = priority_scheduling(processes)
    draw_gantt_chart(gantt, "Priority Scheduling")
