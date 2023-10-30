import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry

# Функция для добавления задач
def add_task():
    task = task_entry.get("1.0", tk.END).strip()

    if task:
        task_list.insert(tk.END, f"☐ {task}")
        task_entry.delete("1.0", tk.END)
        
        # Insert the task into the database
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
    else:
        messagebox.showwarning("Please write your task")

def save_date():
    selected_date = date_picker.get()
    cursor.execute("DELETE FROM dates")
    cursor.execute("INSERT INTO dates (date) VALUES (?)", (selected_date,))
    conn.commit()

def load_tasks():
    cursor.execute("SELECT task FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        task_list.insert(tk.END, f"☐ {task[0]}")

# Функция для отметки задач
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

# Функция для обработки ввода даты
def handle_date_entry():
    entered_date = date_entry.get("1.0", tk.END).strip()
    if entered_date:
        date_entry.destroy()  
        date_label = tk.Label(date_frame, text=entered_date, font=("Montserrat", 16), bg="lightblue")
        date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        # Insert the date into the database
        cursor.execute("INSERT INTO dates (date) VALUES (?)", (entered_date,))
        conn.commit()

def load_dates():
    cursor.execute("SELECT date FROM dates")
    date = cursor.fetchone()
    if date:
        date_label = tk.Label(date_frame, text=date[0], font=("Montserrat", 16), bg="lightblue")
        date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Функция для обновления списка задач
def update_task_list(event):
    task_list.delete(0, tk.END)
    for task in task_entry.get("1.0", tk.END).split('\n'):
        if task.strip():
            task_list.insert(tk.END, f"☐ {task.strip()}")

def save_notes():
    note = notes_entry.get("1.0", tk.END).strip()
    
    # Delete existing note and insert the updated note
    cursor.execute("DELETE FROM notes")
    cursor.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()

def load_notes():
    cursor.execute("SELECT note FROM notes")
    note = cursor.fetchone()
    if note:
        notes_entry.insert(tk.END, note[0])

# Create a database connection and cursor
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Create tables for tasks, dates, and notes if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS dates (id INTEGER PRIMARY KEY, date TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)''')
conn.commit()

# Создание главного окна
root = tk.Tk()
root.title("To-Do List")

# Изменение шрифта на Montserrat
root.option_add("*Font", "Montserrat")

# Create a frame for the date
date_frame = tk.Frame(root, bg="white")
date_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Create a calendar widget for selecting the date
date_picker = DateEntry(date_frame, font=("Montserrat", 16), date_pattern="yyyy-mm-dd")
date_picker.grid(row=1, column=0, padx=10, pady=10, sticky="w")

save_date_button = tk.Button(date_frame, text="Save Date", command=save_date, font=("Montserrat", 16))
save_date_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# Create a frame for notes
notes_frame = tk.Frame(root, bg="white")
notes_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")

# Create a button for saving notes
save_notes_button = tk.Button(notes_frame, text="Save Notes", command=save_notes, font=("Montserrat", 16))
save_notes_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# Заголовок заметок
notes_label = tk.Label(notes_frame, text="Notes", font=("Montserrat", 24, "bold"), bg="#94b97d", fg="white")
notes_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Окно для заметок
notes_entry = tk.Text(notes_frame, font=("Montserrat", 16), height=10, width=30, bg="#94b97d")
notes_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Create a frame for tasks
task_frame = tk.Frame(root, bg="white")
task_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Заголовок задач
title_label = tk.Label(task_frame, text="Tasks", font=("Montserrat", 24, "bold"), bg="lightpink", fg="white")
title_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Отображение задач
task_list = tk.Listbox(task_frame, selectbackground="#c9ffc3", selectmode=tk.SINGLE, bg="lightpink", font=("Montserrat", 20, "bold"), height=10, width=30)
task_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Ввод задачи
task_entry = tk.Text(task_frame, font=("Montserrat", 15), height=3, width=30, bg="lightpink")
task_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
task_entry.bind("<KeyRelease>", lambda event: add_task() if event.keysym == "Return" else None)

# Обработчик нажатия мыши
task_list.bind("<Button-1>", toggle_task_completion)

# Настройка размеров фреймов 
task_frame.grid_rowconfigure(1, weight=1)
task_frame.grid_columnconfigure(0, weight=1)
notes_frame.grid_rowconfigure(1, weight=1)
notes_frame.grid_columnconfigure(0, weight=1)

# Изменение размера окна
root.geometry("720x1080")

load_tasks()
load_dates()
load_notes()

# Запуск приложения
root.mainloop()

