import tkinter as tk
from tkinter import ttk, messagebox
from module1 import read_input_file, generate_processes, write_output_file
from module2 import read_processes, fcfs_scheduler, sjf_scheduler, priority_scheduler, round_robin_scheduler

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

def get_process_color(pid):
    color_map = [
        "#e17055", "#0984e3", "#6c5ce7", "#00b894", "#fd79a8",
        "#fab1a0", "#ffeaa7", "#55efc4", "#a29bfe", "#74b9ff"
    ]
    index = int(pid[1:]) - 1
    return color_map[index % len(color_map)]

def draw_gantt_chart(canvas, schedule_data):
    canvas.delete("all")
    x = 10
    y = 20
    height = 40
    scale = 10

    last_finish = 0
    for item in schedule_data:
        if 'segments' in item:
            for seg in item['segments']:
                start = seg['start']
                dur = seg['duration']
                color = get_process_color(item['id'])
                width = dur * scale

                canvas.create_rectangle(x + start * scale, y, x + (start + dur) * scale, y + height,
                                        fill=color, outline="black")
                canvas.create_text(x + (start + dur / 2) * scale, y + height / 2,
                                   text=item['id'], fill="white", font=("Arial", 10, "bold"))
                canvas.create_text(x + start * scale, y + height + 10, text=str(start), font=("Arial", 9))
                last_finish = max(last_finish, start + dur)
        else:
            start = item['start']
            dur = item['burst']
            color = get_process_color(item['id'])
            canvas.create_rectangle(x + start * scale, y, x + (start + dur) * scale, y + height,
                                    fill=color, outline="black")
            canvas.create_text(x + (start + dur / 2) * scale, y + height / 2,
                               text=item['id'], fill="white", font=("Arial", 10, "bold"))
            canvas.create_text(x + start * scale, y + height + 10, text=str(start), font=("Arial", 9))
            last_finish = max(last_finish, start + dur)

    canvas.create_text(x + last_finish * scale, y + height + 10, text=str(last_finish), font=("Arial", 9))

def display_results(result, title):
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"{title} Scheduling Result:\n\n")
    output_text.insert(tk.END, "ID\tArrival\tBurst\tWaiting\tTurnaround\tFinish\n")
    for p in result:
        output_text.insert(tk.END, f"{p['id']}\t{p['arrival']}\t{p['burst']}\t{p['waiting']}\t{p['turnaround']}\t\t{p['finish']}\n")
    output_text.config(state='disabled')

    draw_gantt_chart(gantt_canvas, result)

# ===== GUI Setup =====
root = tk.Tk()
root.title("🌈 CPU Scheduling Simulator")
root.geometry("1000x900")
root.configure(bg="#f3f0ff")

style = ttk.Style()
style.theme_use("clam")

primary_color = "#6c5ce7"
accent_color = "#74b9ff"
button_color = "#a29bfe"
text_bg = "#dfe6e9"
text_fg = "#2d3436"
title_fg = "#2d3436"

style.configure("TFrame", background="#f3f0ff")
style.configure("TLabel", background="#f3f0ff", font=("Segoe UI", 11), foreground=title_fg)
style.configure("TButton", font=("Segoe UI", 10, "bold"), background=button_color, foreground="black", padding=8)
style.map("TButton",
          background=[("active", accent_color)],
          foreground=[("active", "black")])

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(main_frame, text="🧠 CPU Scheduling Algorithms", font=("Segoe UI", 17, "bold"), foreground=primary_color)
title_label.pack(pady=10)

ttk.Label(main_frame, text="🔄 Generate Processes from 'input.txt':").pack(pady=5)
ttk.Button(main_frame, text="Generate Processes", command=run_generation).pack(pady=6)

ttk.Label(main_frame, text="⚙️ Select Scheduling Algorithm:").pack(pady=10)

button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=6)

ttk.Button(button_frame, text="FCFS", width=15, command=lambda: run_algorithm("FCFS")).grid(row=0, column=0, padx=6, pady=5)
ttk.Button(button_frame, text="SJF", width=15, command=lambda: run_algorithm("SJF")).grid(row=0, column=1, padx=6, pady=5)
ttk.Button(button_frame, text="Priority", width=15, command=lambda: run_algorithm("Priority")).grid(row=0, column=2, padx=6, pady=5)
ttk.Button(button_frame, text="Round Robin", width=15, command=lambda: run_algorithm("Round Robin")).grid(row=0, column=3, padx=6, pady=5)

ttk.Label(main_frame, text="📋 Scheduling Output:").pack(pady=12)

output_text = tk.Text(main_frame, height=15, width=105, font=("Consolas", 11), bg=text_bg, fg=text_fg, relief=tk.GROOVE, bd=2)
output_text.pack()

ttk.Label(main_frame, text="🕒 Gantt Chart:").pack(pady=10)
gantt_canvas = tk.Canvas(main_frame, height=100, bg="white", bd=2, relief=tk.SUNKEN)
gantt_canvas.pack(pady=10, fill=tk.X)

root.mainloop()
