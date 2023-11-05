import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
from datetime import date
import random

# add task fun.
def add_task():
    task = task_entry.get("1.0", tk.END).strip()

    if task:
        selected_date = date_label.cget("text")  # get date (calender)
        task_list.insert(tk.END, f"☐ {task} ({selected_date})")
        task_entry.delete("1.0", tk.END)
        
        # save task to database
        cursor.execute("INSERT INTO tasks (task, date) VALUES (?, ?)", (task, selected_date))
        conn.commit()
    else:
        messagebox.showwarning("Write task")

# save task list to the database fun.
def save_task_list():
    selected_date = date_label.cget("text")
    tasks = [task_list.get(i) for i in range(task_list.size())]
    cursor.execute("DELETE FROM tasks WHERE date=?", (selected_date,))
    for task in tasks:
        # Determine if the task is completed or not
        completed = 1 if task.startswith("☑ ") else 0
        # Remove the checkbox and space at the beginning
        task_text = task[2:]
        # Remove the date in parentheses at the end
        if "(" in task and ")" in task:
            task_text = task_text.rsplit(" (", 1)[0]
        cursor.execute("INSERT INTO tasks (task, date, completed) VALUES (?, ?, ?)", (task_text, selected_date, completed))
    conn.commit()

# toggle task completion fun.
def toggle_task_completion(event):
    selected_task_index = task_list.nearest(event.y)
    task_text = task_list.get(selected_task_index)
    
    if task_text.startswith("☐ "):
        task_text = task_text.replace("☐ ", "☑ ", 1)
        task_list.delete(selected_task_index)
        task_list.insert(selected_task_index, task_text)
        save_task_list() 
    elif task_text.startswith("☑ "):
        task_list.delete(selected_task_index)
        save_task_list()
    else:
        return

# saving selected date fun.
def save_date():
    selected_date = date_picker.get()
    date_label.config(text=selected_date)  # update displayed date
    cursor.execute("DELETE FROM dates")
    cursor.execute("INSERT INTO dates (date) VALUES (?)", (selected_date,))
    conn.commit() 

# update task list when a new date fun.
def update_task_list(event):
    task_list.delete(0, tk.END)
    selected_date = date_label.cget("text")
    cursor.execute("SELECT task FROM tasks WHERE date=?", (selected_date,))
    tasks = cursor.fetchall()
    for task in tasks:
        task_list.insert(tk.END, f"☐ {task[0]} ({selected_date})")

# load tasks and their dates fun.
def load_tasks():
    selected_date = date_label.cget("text")
    task_list.delete(0, tk.END)  # Clear the task list before loading tasks
    cursor.execute("SELECT task, completed FROM tasks WHERE date=?", (selected_date,))
    tasks = cursor.fetchall()
    for task, completed in tasks:
        # Add the correct checkbox based on the completed status
        checkbox = "☑" if completed else "☐"
        task_with_date = f"{checkbox} {task} ({selected_date})"
        task_list.insert(tk.END, task_with_date)
        
# load selected dates fun.
def load_dates():
    cursor.execute("SELECT date FROM dates")
    date = cursor.fetchone()
    if date:
        date_label.config(text=date[0])

# load notes fun.
def load_notes():
    cursor.execute("SELECT note FROM notes")
    note = cursor.fetchone()
    if note:
        notes_entry.delete("1.0", tk.END)  # Clear the existing content
        notes_entry.insert(tk.END, note[0])

# save notes fun.
def save_notes():
    note = notes_entry.get("1.0", tk.END).strip()

    # delete existing and insert the updated note
    cursor.execute("DELETE FROM notes")
    cursor.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    
# Create a function to split long sentences into multiple lines
def wrap_text(text, width=40):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= width:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)
    
# window close event fun.
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        save_task_list()
        root.destroy()

# database connection and cursor 
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# tables for tasks, dates, and notes (if  don't exist)
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, date TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS dates (id INTEGER PRIMARY KEY, date TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)''')
conn.commit()

# create the main window
root = tk.Tk()
root.title("To-Do List")

# font
root.option_add("*Font", "Montserrat")

# frame for date calendar thing
date_frame = tk.Frame(root, bg="white")
date_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# calendar widget for selecting the date
date_picker = DateEntry(date_frame, font=("Montserrat", 16), date_pattern="yyyy-mm-dd")
date_picker.grid(row=1, column=0, padx=20, pady=10, sticky="w")

# button to save the selected date
save_date_button = tk.Button(date_frame, text="Save", command=save_date, font=("Montserrat", 16), bg="#c998f5")
save_date_button.grid(row=4, column=0, padx=71, pady=10, sticky="w")

# Initialize the selected date label
date_label = tk.Label(date_frame, text="", font=("Montserrat", 16), bg="#c998f5", anchor="w")
date_label.grid(row=3, column=0, padx=20, pady=0, sticky="ew")

# Set the column weight to make the label span the entire width of date_frame
date_frame.grid_columnconfigure(0, weight=1)
#bind
date_label.bind("<Button-1>", update_task_list)

#today frame
today_frame = tk.Frame(root, bg="white")
today_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

#today title
today_label = tk.Label(today_frame, text="Today", font=("Montserrat", 24, "bold"), bg="light blue", fg="white")
today_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

#today date
today = date.today()
formatted_date = today.strftime('%B %d, %Y')
today_date = tk.Label(today_frame, text=formatted_date, font=("Montserrat", 16, "bold"), bg="white", fg="light blue")
today_date.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Open and read the text file

with open('sentences.txt', 'r', encoding="utf-8") as file:
    sentences = file.readlines()

sentences = [sentence.strip() for sentence in sentences]

random_sentence = random.choice(sentences)
random_sentence = random_sentence.replace(',', ',\n')

# Create a new frame for the light blue background
quote_frame = tk.Frame(today_frame, bg="light blue")
quote_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

# Create a label within the new frame for centering the text
today_quote = tk.Label(quote_frame, text=random_sentence, font=("Montserrat", 15, "bold"), bg="light blue", fg="white", wraplength=400, justify="center")
today_quote.grid(row=0, column=0, padx=10, pady=10)
quote_frame.grid_columnconfigure(0, weight=1)  # Make sure the frame stretches to match the today_frame width

# Update the grid size of the today_frame to make sure the background frame is centered
today_frame.grid_rowconfigure(2, weight=1)
today_frame.grid_columnconfigure(0, weight=1)

# create frame for notes
notes_frame = tk.Frame(root, bg="white")
notes_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# button to save notes
save_notes_button = tk.Button(notes_frame, text="Save Notes", command=save_notes, font=("Montserrat", 16), bg="#94b97d")
save_notes_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

# notes title
notes_label = tk.Label(notes_frame, text="Notes", font=("Montserrat", 24, "bold"), bg="#94b97d", fg="white",wraplength=100)
notes_label.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# text widget for notes
notes_entry = tk.Text(notes_frame, font=("Montserrat", 16), height=10, width=15, bg="#94b97d")
notes_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# frame for tasks
task_frame = tk.Frame(root, bg="white")
task_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# tasks title
title_label = tk.Label(task_frame, text="Tasks", font=("Montserrat", 24, "bold"), bg="lightpink", fg="white")
title_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# task list
task_list = tk.Listbox(task_frame, selectbackground="#c9ffc3", selectmode=tk.SINGLE, bg="lightpink", font=("Montserrat", 20, "bold"), height=10, width=30)
task_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# task entry
task_entry = tk.Text(task_frame, font=("Montserrat", 15), height=3, width=30, bg="lightpink")
task_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
task_entry.bind("<KeyRelease>", lambda event: add_task() if event.keysym == "Return" else None)
#bind
task_list.bind("<Button-1>", toggle_task_completion)

# config frame sizes
task_frame.grid_rowconfigure(1, weight=1)
task_frame.grid_columnconfigure(0, weight=1)
notes_frame.grid_rowconfigure(1, weight=1)
notes_frame.grid_columnconfigure(0, weight=1)
notes_frame.grid_columnconfigure(1, weight=0)

# Calculate the actual frame sizes
root.update_idletasks()

# Set the window size
root.geometry("730x950")

# load
load_dates()
load_tasks()
load_notes()

# window close event protocol
root.protocol("WM_DELETE_WINDOW", on_closing)

# start
root.mainloop()
