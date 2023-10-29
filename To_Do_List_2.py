import tkinter as tk
from tkinter import messagebox

# Fun. adding tasks
def add_task():
    task = task_entry.get("1.0", tk.END).strip()

    if task:
        task_list.insert(tk.END, f"☐ {task}")
        task_entry.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Please write your task")

# Fun. mark tasks
def toggle_task_completion(event):
    selected_task_index = task_list.nearest(event.y)
    task_text = task_list.get(selected_task_index)
    
    if task_text.startswith("☐ "):
        task_text = task_text.replace("☐ ", "☑ ", 1)
        task_list.delete(selected_task_index)
        task_list.insert(selected_task_index, task_text)
    elif task_text.startswith("☑ "):
        task_list.delete(selected_task_index)
    else:
        return

# Fun. date kaka
def handle_date_entry():
    entered_date = date_entry.get("1.0", tk.END).strip()
    if entered_date:
        date_entry.destroy()  
        date_label = tk.Label(date_frame, text=entered_date, font=("Helvetica", 16), bg="lightblue")
        date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# tasks update
def update_task_list(event):
    task_list.delete(0, tk.END)
    for task in task_entry.get("1.0", tk.END).split('\n'):
        if task.strip():
            task_list.insert(tk.END, f"☐ {task.strip()}")

# task window
root = tk.Tk()
root.title("To-Do List")

# task frame size
task_frame = tk.Frame(root, bg="white")
task_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# title taskidel
title_label = tk.Label(task_frame, text="Tasks", font=("Helvetica", 24, "bold"), bg="lightpink", fg="white")
title_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# task display
task_list = tk.Listbox(task_frame, selectbackground="#c9ffc3", selectmode=tk.SINGLE, bg="lightpink", font=("Helvetica", 20, "bold"), height=10, width=30)
task_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# task add
task_entry = tk.Text(task_frame, font=("Helvetica", 15), height=3, width=30, bg="lightpink")
task_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
task_entry.bind("<KeyRelease>", lambda event: add_task() if event.keysym == "Return" else None)

# link mouse thing
task_list.bind("<Button-1>", toggle_task_completion)

# date (entry) frame
date_frame = tk.Frame(root, bg="white")
date_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# title date
date_label = tk.Label(date_frame, text="Date", font=("Helvetica", 24, "bold"), bg="lightblue", fg="white")
date_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# date entry wondow
date_entry = tk.Text(date_frame, font=("Helvetica", 16), height=1, width=15, bg="lightblue")
date_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")
date_entry.bind("<KeyRelease>", lambda event: handle_date_entry() if event.keysym == "Return" else None)

# notes frame
notes_frame = tk.Frame(root, bg="white")
notes_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")

# notes title
notes_label = tk.Label(notes_frame, text="Notes", font=("Montserrat", 24, "bold"), bg="#94b97d", fg="white")
notes_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# notes window
notes_entry = tk.Text(notes_frame, font=("Helvetica", 16), height=10, width=30, bg="#94b97d")
notes_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# mingi extensionid :3
task_frame.grid_rowconfigure(1, weight=1)
task_frame.grid_columnconfigure(0, weight=1)
notes_frame.grid_rowconfigure(1, weight=1)
notes_frame.grid_columnconfigure(0, weight=1)

root.geometry("720x1080")  # window size

root.mainloop()