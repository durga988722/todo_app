import tkinter as tk
from tkinter import messagebox
import requests

# Base URL for the API
API_BASE_URL = "http://127.0.0.1:5000"

# Function to fetch and create buttons for tasks
def fetch_and_display_tasks():
    # Clear the existing task buttons in tasks_frame
    for widget in tasks_frame.winfo_children():
        widget.destroy()

    response = requests.get(f"{API_BASE_URL}/tasks")
    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            # Create a frame for each task
            task_frame = tk.Frame(tasks_frame, bg="#f0f0f0", borderwidth=2, relief="ridge")
            task_frame.pack(fill="x", pady=5, padx=5)

            # Create a label to show task information
            task_info = f"ID: {task['id']} - Name: {task['task_name']} - Status: {task['status']}"
            task_label = tk.Label(task_frame, text=task_info, bg="#f0f0f0", font=("Arial", 12))
            task_label.pack(side="left", padx=10)

            # Create an update button for each task
            update_button = tk.Button(task_frame, text="Update", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=lambda t=task: update_task_popup(t))
            update_button.pack(side="right", padx=5)

            # Create a delete button for each task
            delete_button = tk.Button(task_frame, text="Delete", font=("Arial", 10, "bold"), bg="#F44336", fg="white", command=lambda t=task: delete_task(t['id']))
            delete_button.pack(side="right", padx=5)
    else:
        messagebox.showerror("Error", "Failed to fetch tasks")

# Function to add a task
def add_task():
    task_name = task_name_entry.get()
    status = task_status_entry.get()

    if not task_name:
        messagebox.showerror("Input Error", "Task name is required")
        return

    response = requests.post(f"{API_BASE_URL}/tasks", json={"task_name": task_name, "status": status or "Pending"})
    if response.status_code == 201:
        messagebox.showinfo("Success", "Task added successfully!")
        task_name_entry.delete(0, tk.END)
        task_status_entry.delete(0, tk.END)
        fetch_and_display_tasks()  # Refresh task list
    else:
        messagebox.showerror("Error", "Failed to add task")

# Function to delete a task
def delete_task(task_id):
    response = requests.delete(f"{API_BASE_URL}/tasks/{task_id}")
    if response.status_code == 200:
        messagebox.showinfo("Success", "Task deleted successfully!")
        fetch_and_display_tasks()  # Refresh task list
    else:
        messagebox.showerror("Error", "Failed to delete task")

# Function to show a popup for updating a task
def update_task_popup(task):
    popup = tk.Toplevel()
    popup.title("Update Task")
    popup.geometry("300x200")
    popup.configure(bg="#f7f7f7")

    tk.Label(popup, text="New Task Name", font=("Arial", 12), bg="#f7f7f7").pack(pady=5)
    new_name_entry = tk.Entry(popup, font=("Arial", 12))
    new_name_entry.pack()
    new_name_entry.insert(0, task["task_name"])

    tk.Label(popup, text="New Status", font=("Arial", 12), bg="#f7f7f7").pack(pady=5)
    new_status_entry = tk.Entry(popup, font=("Arial", 12))
    new_status_entry.pack()
    new_status_entry.insert(0, task["status"])

    tk.Button(popup, text="Update", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=lambda: update_task(task['id'], new_name_entry.get(), new_status_entry.get(), popup)).pack(pady=10)

# Function to update a task
def update_task(task_id, new_name, new_status, popup):
    response = requests.put(f"{API_BASE_URL}/tasks/{task_id}", json={"task_name": new_name, "status": new_status})
    if response.status_code == 200:
        messagebox.showinfo("Success", "Task updated successfully!")
        popup.destroy()
        fetch_and_display_tasks()  # Refresh task list
    else:
        messagebox.showerror("Error", "Failed to update task")

# Create the main window
window = tk.Tk()
window.title("To-Do App")
window.geometry("600x700")
window.configure(bg="#f2f2f2")

# Add Task Section
add_task_frame = tk.Frame(window, borderwidth=1, relief="ridge", bg="#e0e0e0", padx=10, pady=10)
add_task_frame.pack(fill="x", pady=10)

tk.Label(add_task_frame, text="Add Task", font=("Arial", 14, "bold"), bg="#e0e0e0").pack(pady=5)
tk.Label(add_task_frame, text="Task Name", font=("Arial", 12), bg="#e0e0e0").pack()
task_name_entry = tk.Entry(add_task_frame, font=("Arial", 12))
task_name_entry.pack()

tk.Label(add_task_frame, text="Status", font=("Arial", 12), bg="#e0e0e0").pack()
task_status_entry = tk.Entry(add_task_frame, font=("Arial", 12))
task_status_entry.pack()

add_task_button = tk.Button(add_task_frame, text="Add Task", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=add_task)
add_task_button.pack(pady=10)

# Frame to hold the task buttons
tasks_frame = tk.Frame(window, bg="#f2f2f2")
tasks_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Fetch and display all tasks with buttons for each task
fetch_and_display_tasks_button = tk.Button(window, text="Refresh Tasks", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", command=fetch_and_display_tasks)
fetch_and_display_tasks_button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
