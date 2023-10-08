import tkinter as tk
from tkinter import messagebox

# Add a task
def add_task():
    task = task_entry.get()
    if task:
        task_list.insert(tk.END, f"☐ {task}")
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

# Task completion and remove
def toggle_task_completion(event):
    selected_task_index = task_list.nearest(event.y)
    task_text = task_list.get(selected_task_index)
    
    if task_text.startswith("☐ "):
        task_text = task_text.replace("☐ ", "☑ ", 1)
        task_list.delete(selected_task_index)
        task_list.insert(selected_task_index, task_text)
    else:
        task_list.delete(selected_task_index)

# Window
root = tk.Tk()
root.title("To-Do List")

# Frame
task_frame = tk.Frame(root)
task_frame.grid(row=0, column=0, padx=20, pady=20)

# Display tasks
task_list = tk.Listbox(task_frame, selectbackground="light green", selectmode=tk.SINGLE, bg="white", font=("Helvetica", 14), height=10)
task_list.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Add task
task_entry = tk.Entry(task_frame, font=("Helvetica", 14))
task_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Button
add_button = tk.Button(task_frame, text="Add Task", command=add_task, font=("Helvetica", 14))
add_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

task_list.bind("<Button-1>", toggle_task_completion)

# Expand with window
task_frame.grid_rowconfigure(0, weight=1)
task_frame.grid_columnconfigure(0, weight=1)


root.mainloop()
