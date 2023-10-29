import tkinter as tk
from tkinter import messagebox

# Funkt. for adding tasks
def add_task():
    task = task_entry.get("1.0", tk.END).strip()

    if task:
        task_list.insert(tk.END, f"☐ {task}")
        task_entry.delete("1.0", tk.END)
    else:
        messagebox.showwarning("Please,write your task")

# Funkt. to mark done/not done in tasks
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

# Tasks update
def update_task_list(event):
    task_list.delete(0, tk.END)
    for task in task_entry.get("1.0", tk.END).split('\n'):
        if task.strip():
            task_list.insert(tk.END, f"☐ {task.strip()}")

# Task window
root = tk.Tk()
root.title("Список задач и заметки")

# Frame for tasks
task_frame = tk.Frame(root, bg="white")
task_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

#  Title for tasks
title_label = tk.Label(task_frame, text="Tasks", font=("Helvetica", 24, "bold"), bg="lightpink", fg="white")
title_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

#  Task display
task_list = tk.Listbox(task_frame, selectbackground="#c9ffc3", selectmode=tk.SINGLE, bg="lightpink", font=("Helvetica", 20, "bold"), height=10, width=30)
task_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Task adding
task_entry = tk.Text(task_frame, font=("Helvetica", 15), height=3, width=30, bg="lightpink")
task_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
task_entry.bind("<KeyRelease>", update_task_list)

#  Button for task adding
add_button = tk.Button(task_frame, text="Add new task", command=add_task, font=("Helvetica", 14), background="#94b97d", fg="black")
add_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# Linking a function to a mouse action for tasks
task_list.bind("<Button-1>", toggle_task_completion)

# Date entry frame
date_frame = tk.Frame(root, bg="white")
date_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

#  Title for date
date_label = tk.Label(date_frame, text="Date", font=("Helvetica", 24, "bold"), bg="lightblue", fg="white")
date_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

#  Window for date
date_entry = tk.Text(date_frame, font=("Helvetica", 16), height=0, width=15, bg="lightblue")
date_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")

#  Frame for notes
notes_frame = tk.Frame(root, bg="white")
notes_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")

# Title for notes
notes_label = tk.Label(notes_frame, text="Notes", font=("Montserrat", 24, "bold"), bg="#94b97d", fg="white")
notes_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

#  Window for notes
notes_entry = tk.Text(notes_frame, font=("Helvetica", 16), height=10, width=30, bg="#94b97d")
notes_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

#  Extension with task window
task_frame.grid_rowconfigure(1, weight=1)
task_frame.grid_columnconfigure(0, weight=1)

# Extension with notes window
notes_frame.grid_rowconfigure(1, weight=1)
notes_frame.grid_columnconfigure(0, weight=1)

root.geometry("800x600")  # Setting the window size

root.mainloop()
