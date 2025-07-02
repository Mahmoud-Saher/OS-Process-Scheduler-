import tkinter as tk
from tkinter import ttk, messagebox
from module1 import read_input_file, generate_processes, write_output_file
from module2 import read_processes, fcfs_scheduler, sjf_scheduler, priority_scheduler, round_robin_scheduler
import matplotlib.pyplot as plt

def run_generation():
    try:
        num, amean, astd, bmean, bstd, plambda = read_input_file("input.txt")
        processes = generate_processes(num, amean, astd, bmean, bstd, plambda)
        write_output_file("processes.txt", processes)
        messagebox.showinfo("Success", "✅ Process generation completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_algorithm(algorithm):
    try:
        processes = read_processes("processes.txt")
        if algorithm == "FCFS":
            result = fcfs_scheduler(processes.copy())
        elif algorithm == "SJF":
            result = sjf_scheduler(processes.copy())
        elif algorithm == "Priority":
            result = priority_scheduler(processes.copy())
        elif algorithm == "Round Robin":
            result = round_robin_scheduler(processes.copy(), quantum=2)

        display_results(result, algorithm)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_results(result, title):
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"{title} Scheduling Result:\n\n")
    output_text.insert(tk.END, "ID\tArrival\tBurst\tWaiting\tTurnaround\tFinish\n")
    for p in result:
        output_text.insert(tk.END, f"{p['id']}\t{p['arrival']}\t{p['burst']}\t{p['waiting']}\t{p['turnaround']}\t\t{p['finish']}\n")
    output_text.config(state='disabled')
    # رسم Gantt Chart
    fig, gnt = plt.subplots()
    gnt.set_title(f"{title} - Gantt Chart")
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Processes")

    gnt.set_yticks([10 * (i+1) for i in range(len(result))])
    gnt.set_yticklabels([f"P{p['id']}" for p in result])

    gnt.grid(True)

    for i, p in enumerate(result):
        gnt.broken_barh([(p['start'], p['burst'])], (10 * (i+1) - 2, 4), facecolors='tab:blue')

    plt.show()

# ===== GUI Setup =====
root = tk.Tk()
root.title("🌈 CPU Scheduling Simulator")
root.geometry("850x620")
root.configure(bg="#f3f0ff")  # Soft lavender background

# Style Setup
style = ttk.Style()
style.theme_use("clam")

# Custom colors
primary_color = "#6c5ce7"     # Purple
accent_color = "#74b9ff"      # Light blue
button_color = "#a29bfe"      # Soft purple
text_bg = "#dfe6e9"           # Light gray
text_fg = "#2d3436"           # Dark gray
title_fg = "#2d3436"

style.configure("TFrame", background="#f3f0ff")
style.configure("TLabel", background="#f3f0ff", font=("Segoe UI", 11), foreground=title_fg)
style.configure("TButton", font=("Segoe UI", 10, "bold"), background=button_color, foreground="black", padding=8)
style.map("TButton",
          background=[("active", accent_color)],
          foreground=[("active", "black")])

# Layout
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Title
title_label = ttk.Label(main_frame, text="🧠 CPU Scheduling Algorithms", font=("Segoe UI", 17, "bold"), foreground=primary_color)
title_label.pack(pady=10)

# Generate
ttk.Label(main_frame, text="🔄 Generate Processes from 'input.txt':").pack(pady=5)
ttk.Button(main_frame, text="Generate Processes", command=run_generation).pack(pady=6)

# Algorithms
ttk.Label(main_frame, text="⚙️ Select Scheduling Algorithm:").pack(pady=10)

button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=6)

ttk.Button(button_frame, text="FCFS", width=15, command=lambda: run_algorithm("FCFS")).grid(row=0, column=0, padx=6, pady=5)
ttk.Button(button_frame, text="SJF", width=15, command=lambda: run_algorithm("SJF")).grid(row=0, column=1, padx=6, pady=5)
ttk.Button(button_frame, text="Priority", width=15, command=lambda: run_algorithm("Priority")).grid(row=0, column=2, padx=6, pady=5)
ttk.Button(button_frame, text="Round Robin", width=15, command=lambda: run_algorithm("Round Robin")).grid(row=0, column=3, padx=6, pady=5)

# Output
ttk.Label(main_frame, text="📋 Scheduling Output:").pack(pady=12)

output_text = tk.Text(main_frame, height=15, width=100, font=("Consolas", 11), bg=text_bg, fg=text_fg, relief=tk.GROOVE, bd=2)
output_text.pack()
output_text.config(state='disabled')

root.mainloop()
