import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       description TEXT NOT NULL,
                       priority INTEGER NOT NULL,
                       status TEXT NOT NULL,
                       category TEXT,
                       due_date TEXT)''')
    conn.commit()
    conn.close()

# Adding a new task
def add_task(description, priority, category, due_date):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO tasks(description, priority, status, category, due_date)
                      VALUES (?, ?, ?, ?, ?)''', (description, priority, 'incomplete', category, due_date))
    conn.commit()
    conn.close()
    refresh_tasks()

# Viewing all tasks
def view_tasks():
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Updating a task
def update_task(task_id, description=None, priority=None, category=None, due_date=None, status=None):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    if description:
        cursor.execute('UPDATE tasks SET description = ? WHERE id = ?', (description, task_id))
    if priority:
        cursor.execute('UPDATE tasks SET priority = ? WHERE id = ?', (priority, task_id))
    if category:
        cursor.execute('UPDATE tasks SET category = ? WHERE id = ?', (category, task_id))
    if due_date:
        cursor.execute('UPDATE tasks SET due_date = ? WHERE id = ?', (due_date, task_id))
    if status:
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
    conn.commit()
    conn.close()
    refresh_tasks()

# Deleting a task
def delete_task(task_id):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    refresh_tasks()

# Filtering tasks
def filter_tasks(by='category', value=''):
    conn = sqlite3.connect('todo_list.db')
    cursor = conn.cursor()
    if by == 'category':
        cursor.execute('SELECT * FROM tasks WHERE category = ?', (value,))
    elif by == 'due_date':
        cursor.execute('SELECT * FROM tasks WHERE due_date = ?', (value,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Marking a task as complete
def mark_task_complete(task_id):
    update_task(task_id, status='complete')

# Refreshing the task list in the GUI
def refresh_tasks():
    for i in tree.get_children():
        tree.delete(i)
    tasks = view_tasks()
    for task in tasks:
        tree.insert('', 'end', values=task)

# Adding task to the database from GUI
def add_task_gui():
    description = description_entry.get()
    priority = int(priority_entry.get())
    category = category_entry.get()
    due_date = due_date_entry.get()
    add_task(description, priority, category, due_date)
    clear_entries()

# Clearing input fields
def clear_entries():
    description_entry.delete(0, tk.END)
    priority_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)

# Updating task in the database from GUI
def update_task_gui():
    selected_item = tree.selection()[0]
    task_id = tree.item(selected_item)['values'][0]
    description = description_entry.get()
    priority = int(priority_entry.get())
    category = category_entry.get()
    due_date = due_date_entry.get()
    status = 'complete' if status_var.get() == 1 else 'incomplete'
    update_task(task_id, description, priority, category, due_date, status)
    clear_entries()

# Deleting task in the database from GUI
def delete_task_gui():
    selected_item = tree.selection()[0]
    task_id = tree.item(selected_item)['values'][0]
    delete_task(task_id)

# Marking task as complete from GUI
def mark_task_complete_gui():
    selected_item = tree.selection()[0]
    task_id = tree.item(selected_item)['values'][0]
    mark_task_complete(task_id)
    refresh_tasks()

# Filtering tasks from GUI
def filter_tasks_gui():
    filter_by = filter_option.get()
    value = filter_value_entry.get()
    tasks = filter_tasks(by=filter_by, value=value)
    for i in tree.get_children():
        tree.delete(i)
    for task in tasks:
        tree.insert('', 'end', values=task)

# GUI setup
root = tk.Tk()
root.title("To-Do List Application")

frame = tk.Frame(root)
frame.pack(pady=20)

# Treeview for displaying tasks
columns = ("ID", "Description", "Priority", "Status", "Category", "Due Date")
tree = ttk.Treeview(frame, columns=columns, show='headings', height=8)
tree.pack()

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Input fields
description_label = tk.Label(root, text="Description:")
description_label.pack()
description_entry = tk.Entry(root, width=50)
description_entry.pack()

priority_label = tk.Label(root, text="Priority:")
priority_label.pack()
priority_entry = tk.Entry(root, width=50)
priority_entry.pack()

category_label = tk.Label(root, text="Category:")
category_label.pack()
category_entry = tk.Entry(root, width=50)
category_entry.pack()

due_date_label = tk.Label(root, text="Due Date (YYYY-MM-DD):")
due_date_label.pack()
due_date_entry = tk.Entry(root, width=50)
due_date_entry.pack()

status_var = tk.IntVar()
status_check = tk.Checkbutton(root, text="Mark as Complete", variable=status_var)
status_check.pack()

# Buttons
add_button = tk.Button(root, text="Add Task", command=add_task_gui)
add_button.pack(pady=5)

update_button = tk.Button(root, text="Update Task", command=update_task_gui)
update_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task_gui)
delete_button.pack(pady=5)

mark_complete_button = tk.Button(root, text="Mark Task as Complete", command=mark_task_complete_gui)
mark_complete_button.pack(pady=5)

# Filtering tasks
filter_option = tk.StringVar()
filter_option.set("category")
filter_label = tk.Label(root, text="Filter By:")
filter_label.pack()
filter_dropdown = ttk.Combobox(root, textvariable=filter_option)
filter_dropdown['values'] = ("category", "due_date")
filter_dropdown.pack()

filter_value_label = tk.Label(root, text="Value:")
filter_value_label.pack()
filter_value_entry = tk.Entry(root, width=50)
filter_value_entry.pack()

filter_button = tk.Button(root, text="Filter Tasks", command=filter_tasks_gui)
filter_button.pack(pady=5)

# Initialize the database and load tasks
init_db()
refresh_tasks()

root.mainloop()
