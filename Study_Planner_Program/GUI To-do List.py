### INITIAL CONFIGURATION ###

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import json
import os 
import calendar

users = {"Test_user": "0123"}
subjects = ["Python 101", "Microcontroller", "Mathematics", "Physics for Engineering", "General Science", "English","Social Studies","Health Education","Physical Education","Art","Music","Thai"]
teachers = ["Aj. Praphat","Aj. Tanapoom","T. Nas","Aj. Suwapat","T. Dan","Aj. Napasawan","Aj. Watchapol","T. Colin"]

user_entry = None
code_entry = None
root = None
task_entry = None
status_var = None
date_entry = None
notes_entry = None
tree = None
subj_var = None
teacher_var = None

event_entry = None
event_notes_entry = None
event_tree = None
event_status_var = None
event_date_entry = None
event_associates_var = None
priority_var = None 

current_user = None 

### JSON FILE SYSTEM ###

def get_data_file_path(username):
    return f"{username}_tasks_events.json"

def save_data_to_json():
    global current_user, tree, event_tree
    
    if not current_user:
        messagebox.showerror("Error", "No user logged in to save data.")
        return
    
    tasks = []
    for item in tree.get_children():
        task_data = tree.item(item, 'values')
        if len(task_data) >= 7:
            tasks.append({
                "task": task_data[0],
                "status": task_data[1],
                "subject": task_data[2],
                "date": task_data[3],
                "notes": task_data[4],
                "by": task_data[5],
                "priority": task_data[6]
            })
    
    events = []
    for item in event_tree.get_children():
        event_data = event_tree.item(item, 'values')
        if len(event_data) >= 5:
            events.append({
                "event": event_data[0],
                "status": event_data[1],
                "associates": event_data[2],
                "date": event_data[3],
                "notes": event_data[4]
            })

    data_to_save = {
        "tasks": tasks,
        "events": events
    }
    
    file_path = get_data_file_path(current_user)
    try:
        with open(file_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        messagebox.showinfo("Success", f"Data saved successfully to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def load_data_from_json():
    global current_user, tree, event_tree
    
    if not current_user:
        return
        
    file_path = get_data_file_path(current_user)
    if not os.path.exists(file_path):
        print(f"No data file found for {current_user}, starting with empty lists.")
        return
        
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        tree.delete(*tree.get_children())
        event_tree.delete(*event_tree.get_children())
        
        if "tasks" in data:
            for task in data["tasks"]:
                tags = ()
                if task.get("priority") == "Red: Critical":
                    tags = ('red',)
                elif task.get("priority") == "Yellow: Caution":
                    tags = ('yellow',)
                elif task.get("priority") == "White: Regular":
                    tags = ('white',)
                tree.insert("", tk.END, values=(
                    task.get("task", ""),
                    task.get("status", ""),
                    task.get("subject", ""),
                    task.get("date", ""),
                    task.get("notes", ""),
                    task.get("by", ""),
                    task.get("priority", "")
                ), tags=tags)
        
        if "events" in data:
            for event in data["events"]:
                event_tree.insert("", tk.END, values=(
                    event.get("event", ""),
                    event.get("status", ""),
                    event.get("associates", ""),
                    event.get("date", ""),
                    event.get("notes", "")
                ))
                
        print(f"Data loaded successfully for {current_user}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")

### CALENDAR SYSTEM ###

class CalendarPopup(tk.Toplevel):
    def __init__(self, parent, target_entry):
        super().__init__(parent)
        self.title("Select a Date")
        self.transient(parent)  
        self.grab_set() 
        self.target_entry = target_entry

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack(padx=10, pady=10)

        self.nav_frame = tk.Frame(self)
        self.nav_frame.pack(pady=5)

        tk.Button(self.nav_frame, text="<", command=self.prev_month).pack(side=tk.LEFT)
        self.month_label = tk.Label(self.nav_frame, text="", width=15)
        self.month_label.pack(side=tk.LEFT, padx=10)
        tk.Button(self.nav_frame, text=">", command=self.next_month).pack(side=tk.LEFT)
        
        self.daily_list_frame = tk.LabelFrame(self, text="Tasks & Events for the Selected Date")
        self.daily_list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.daily_list_label = tk.Label(self.daily_list_frame, text="Select a date to see tasks and events.", justify=tk.LEFT, wraplength=400)
        self.daily_list_label.pack(padx=5, pady=5)

        self.show_calendar()

    def show_calendar(self):
    
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days_of_week):
            tk.Label(self.calendar_frame, text=day).grid(row=0, column=i, padx=5, pady=5)

        cal_days = calendar.monthcalendar(self.current_year, self.current_month)
        for row_idx, week in enumerate(cal_days):
            for col_idx, day in enumerate(week):
                if day != 0:
                    day_button = tk.Button(self.calendar_frame, text=str(day),
                                           command=lambda d=day: self.select_date(d))
                    day_button.grid(row=row_idx + 1, column=col_idx, padx=2, pady=2)
                    
    def check_tasks_for_date(self, selected_date_str):
        tasks_on_date = []
        events_on_date = []

        for item in tree.get_children():
            task_data = tree.item(item, 'values')
            if len(task_data) > 3 and task_data[3] == selected_date_str:
                tasks_on_date.append(f"Task: {task_data[0]} ({task_data[1]})")

        for item in event_tree.get_children():
            event_data = event_tree.item(item, 'values')
            if len(event_data) > 3 and event_data[3] == selected_date_str:
                events_on_date.append(f"Event: {event_data[0]} ({event_data[1]})")

        display_text = ""
        if tasks_on_date or events_on_date:
            if tasks_on_date:
                display_text += "Tasks:\n" + "\n".join(tasks_on_date) + "\n\n"
            if events_on_date:
                display_text += "Events:\n" + "\n".join(events_on_date)
        else:
            display_text = "No tasks or events on this date."

        self.daily_list_label.config(text=display_text)


    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.show_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.show_calendar()

    def select_date(self, day):
        selected_date = datetime(self.current_year, self.current_month, day)
        selected_date_str = selected_date.strftime("%Y-%m-%d")
        
        self.target_entry.delete(0, tk.END)
        self.target_entry.insert(0, selected_date_str)
        self.check_tasks_for_date(selected_date_str)


def show_calendar_popup(target_entry):
    CalendarPopup(root, target_entry)


### LOG IN FUNCTION ###

def login():

    global current_user, root

    username = user_entry.get()
    password = code_entry.get()
    
    if username in users and users[username] == password:
        messagebox.showinfo("Alert Message:", f"Welcome {username}")
        print(f"{username} login successful")
        current_user = username 
        root.destroy() 
        main_window() 
    elif username in users and users[username] != password:
        messagebox.showwarning("Alert Message:", "Error 403 | Access Denied\nIncorrect Password, Please check again")
    else:
        messagebox.showwarning("Alert Message:", "Error 404 | User not found\nPlease register first")

### CLOCK FUNCTION ###

def update_clock(clock_label):
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    clock_label.config(text=time_string)
    clock_label.after(1000, update_clock, clock_label)

### TASK ADDER FUNCTION ###

def add_task():

    global tree, task_entry, status_var, subj_var, teacher_var, date_entry, notes_entry, priority_var
    
    task = task_entry.get()
    status = status_var.get()
    sub = subj_var.get()
    t = teacher_var.get()
    date = date_entry.get()
    notes = notes_entry.get()
    priority = priority_var.get()
    
    if task:
        tags = ()
        if priority == "Red: Critical":
            tags = ('red',)
        elif priority == "Yellow: Caution":
            tags = ('yellow',)
        elif priority == "White: Regular":
            tags = ('white',)

        tree.insert("", tk.END, values=(task, status, sub, date, notes, t, priority), tags=tags)
        
        task_entry.delete(0, tk.END)
        subj_var.set("N/A")
        teacher_var.set("N/A")
        date_entry.delete(0, tk.END)
        notes_entry.delete(0, tk.END)
        status_var.set("Not Started")
        priority_var.set("White: Regular") 
    else:
        messagebox.showwarning("Input Error", "Task field cannot be empty.")

### TASK COMPLETION FUNCTION ###

def mark_as_completed():

    selected_item = tree.selection()
    
    if selected_item:
        item_id = selected_item[0]
        current_values = list(tree.item(item_id, "values"))
        current_values[1] = "Completed ✅"
        current_tags = tree.item(item_id, "tags")
        tree.item(item_id, values=tuple(current_values), tags=current_tags)
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messagebox.showinfo("Alert Message:", f"Congratulations\nTask Completed at {order_time}")
    else:
        messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

### TASK DELETION FUNCTION ###

def delete_task():

    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

### EVENT ADDER FUNCTION ###

def add_event():

    global event_tree, event_entry, event_status_var, event_date_entry, event_notes_entry, event_associates_var

    event = event_entry.get()
    status = event_status_var.get()
    date = event_date_entry.get()
    notes = event_notes_entry.get()
    associates = event_associates_var.get()
    
    if event:
        event_tree.insert("", tk.END, values=(event, status, associates, date, notes))
        event_entry.delete(0, tk.END)
        event_notes_entry.delete(0, tk.END)
        event_date_entry.delete(0, tk.END)
        event_status_var.set("Not Started")
        event_associates_var.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Event field cannot be empty.")

### TASK COMPLETION FUNCTION ###

def mark_event_completed():

    selected_item = event_tree.selection()
    
    if selected_item:
        item_id = selected_item[0]
        current_values = list(event_tree.item(item_id, "values"))
        current_values[1] = "Completed ✅"
        event_tree.item(item_id, values=tuple(current_values))
        messagebox.showinfo("Alert Message:", "Event marked as completed!")
    else:
        messagebox.showwarning("Selection Error", "Please select an event to mark as completed.")
        
### EVENT DELETION FUNCTION ###

def delete_event():
    selected_item = event_tree.selection()
    if selected_item:
        event_tree.delete(selected_item)
    else:
        messagebox.showwarning("Selection Error", "Please select an event to delete.")

### LOGIN WINDOW DISPLAY ###

def display_login_window():

    global user_entry, code_entry, root
    
    root = tk.Tk()
    root.title("CMD")
    root.geometry('400x200')

    input_frame = tk.Frame(root)
    input_frame.pack(pady=20)
    
    password_frame = tk.Frame(root)
    password_frame.pack(pady=5)

    tk.Label(input_frame, text="System Login").pack(side="top", pady=10)
    tk.Label(input_frame, text="Username:").pack(side="left")
    user_entry = tk.Entry(input_frame, width=30)
    user_entry.pack(padx=10, side="left")

    tk.Label(password_frame, text="Password:").pack(side="left")
    code_entry = tk.Entry(password_frame, width=30, show="*")
    code_entry.pack(padx=10, side="left")

    tk.Button(root, text="Submit", command=login).pack(pady=15)
    root.mainloop()

### MAIN WINDOW DISPLAY ###

def main_window():

    global root, task_entry, status_var, date_entry, notes_entry, tree, subj_var, teacher_var, event_entry, event_notes_entry, event_tree, event_status_var, event_date_entry, event_associates_var, priority_var
    
    root = tk.Tk()
    root.title("To-Do List Application")
    root.geometry("1920x1080")

    myMenu = tk.Menu(root)
    root.config(menu=myMenu)
    file_menu = tk.Menu(myMenu, tearoff=0)
    myMenu.add_cascade(label="📁 File", menu=file_menu)
    file_menu.add_command(label="💾 Save", command=save_data_to_json)
    file_menu.add_command(label="✂️ Exit", command=root.destroy)
    

    input_frame = tk.Frame(root, padx=10, pady=10)
    input_frame.pack(fill="x")
    
    task_frame = tk.LabelFrame(input_frame, text="To-Do List", padx=10, pady=10)
    task_frame.pack(side=tk.LEFT, padx=10, pady=10, fill="both", expand=True)

    event_frame = tk.LabelFrame(input_frame, text="Your schedule", padx=10, pady=10)
    event_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill="both", expand=True)

### TO DO LIST CONTROL PANEL DISPLAY ###

    tk.Label(task_frame,text="Task:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    task_entry = tk.Entry( task_frame, width=30)
    task_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(task_frame, text="Status:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    status_var = tk.StringVar(root)
    status_var.set("Not Started")
    status_options = ["Not Started", "In Progress", "Completed"]
    tk.OptionMenu( task_frame, status_var, *status_options).grid(row=0, column=3, padx=5, pady=5, sticky="w")
    
    tk.Label(task_frame, text="Priority:").grid(row=0, column=6, padx=5, pady=5)
    priority_var = tk.StringVar(root)
    priority_var.set("White: Regular")
    priority_options = ["Red: Critical", "Yellow: Caution", "White: Regular"]
    tk.OptionMenu(task_frame, priority_var, *priority_options).grid(row=0, column=7, padx=5, pady=5, sticky="w")

    tk.Label( task_frame, text="Subj:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    subj_var = tk.StringVar(root)
    subj_var.set("N/A")
    tk.OptionMenu( task_frame, subj_var, *subjects).grid(row=0, column=5, padx=5, pady=5, sticky="w")
    
    tk.Label( task_frame, text="Teacher:").grid(row=1, column=4, padx=5, pady=5, sticky="e")
    teacher_var = tk.StringVar(root)
    teacher_var.set("N/A")
    tk.OptionMenu( task_frame, teacher_var, *teachers).grid(row=1, column=5, padx=5, pady=5, sticky="w")

    tk.Label( task_frame, text="Due Date:").grid(row=1, column=8, padx=5, pady=5, sticky="e")
    date_entry = tk.Entry( task_frame, width=15)
    date_entry.grid(row=1, column=9, padx=5, pady=5, sticky="w")
    date_entry.bind("<Button-1>", lambda event: show_calendar_popup(date_entry))

    tk.Label( task_frame, text="Notes:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    notes_entry = tk.Entry( task_frame, width=60)
    notes_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

    clock_label = tk.Label( task_frame, width=20, bg="#FFFFFF")
    clock_label.grid(row=0, column=8,columnspan=2 , pady=10)
    update_clock(clock_label)

    tk.Button( task_frame, text="➕ Add Task", bg="#11294F", fg='#FFFFFF', command=add_task).grid(row=2, column=1, pady=10)
    tk.Button( task_frame, text="✅ Mark as Completed", bg="#11294F", fg='#FFFFFF', command=mark_as_completed).grid(row=2, column=2, pady=10)
    tk.Button( task_frame, text="✂️ Delete Task", bg="#11294F", fg='#FFFFFF', command=delete_task).grid(row=2, column=3, pady=10)
    
### TO DO LIST TREE VIEW DISPLAY ###

    todo_table_frame = tk.Frame(root)
    todo_table_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    
    tree = ttk.Treeview(todo_table_frame, columns=("Task", "Status", "Subject", "Date", "Notes", "By", "Priority"), show="headings")
    tree.heading("Task", text="Task")
    tree.heading("Status", text="Status")
    tree.heading("Subject", text="Subject")
    tree.heading("Date", text="Due Date")
    tree.heading("Notes", text="Notes")
    tree.heading("By", text="By")
    tree.heading("Priority", text="Priority")

    tree.column("Task", width=150, anchor=tk.W)
    tree.column("Status", width=100, anchor=tk.W)
    tree.column("Subject", width=150, anchor=tk.W)
    tree.column("Date", width=100, anchor=tk.W)
    tree.column("Notes", width=300, anchor=tk.W)
    tree.column("By", width=100, anchor=tk.W)
    tree.column("Priority", width=100, anchor=tk.W)

    tree.tag_configure('red', background='red', foreground='white')
    tree.tag_configure('yellow', background='yellow')
    tree.tag_configure('green', background='green', foreground='white')

### EVENT LIST CONTROL PANEL DISPLAY ###
    
    tk.Label(event_frame,text="Event: ").grid(row=0, column=11, padx=5, pady=5, sticky="e")
    event_entry = tk.Entry( event_frame, width=30)
    event_entry.grid(row=0, column=12, padx=5, pady=5, sticky="w")

    tk.Label(event_frame, text="Status:").grid(row=0, column=13, padx=5, pady=5, sticky="e")
    event_status_var = tk.StringVar(root)
    event_status_var.set("Not Started")
    event_status_options = ["Not Started", "In Progress", "Completed"]
    tk.OptionMenu(event_frame, event_status_var , *event_status_options).grid(row=0, column=14, padx=5, pady=5)
    
    tk.Label(event_frame, text="Assosiciates:").grid(row=1, column=15, padx=5, pady=5, sticky="e")
    event_associates_var = tk.Entry(event_frame, width=15)
    event_associates_var.grid(row=1, column=16, padx=5, pady=5, sticky="w")

    tk.Label(event_frame, text="Date:").grid(row=1, column=17, padx=5, pady=5, sticky="e")
    event_date_entry = tk.Entry(event_frame, width=15)
    event_date_entry.grid(row=1, column=18, padx=5, pady=5, sticky="w")
    event_date_entry.bind("<Button-1>", lambda event: show_calendar_popup(event_date_entry))

    tk.Label(event_frame, text="Notes:").grid(row=1, column=11, padx=5, pady=5, sticky="e")
    event_notes_entry = tk.Entry(event_frame, width=60)
    event_notes_entry.grid(row=1, column=12,columnspan=3, padx=5, pady=5, sticky="ew")

    tk.Button(event_frame, text="➕ Add Event", bg="#11294F", fg='#FFFFFF', command=add_event).grid(row=2, column=12, pady=10)
    tk.Button(event_frame, text="✅ Event Finished", bg="#11294F", fg='#FFFFFF', command=mark_event_completed).grid(row=2, column=13, pady=10)
    tk.Button(event_frame, text="✂️ Delete Event", bg="#11294F", fg='#FFFFFF', command=delete_event).grid(row=2, column=14, pady=10)
    tk.Button(event_frame, text="📅 Show Calendar", bg="#11294F", fg='#FFFFFF', command=lambda: show_calendar_popup(event_date_entry)).grid(row=2, column=16, pady=10)

### EVENT LIST TREE VIEW DISPLAY ###

    event_table_frame = tk.Frame(root)
    event_table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
    event_tree = ttk.Treeview(event_table_frame, columns=("Event", "Status", "Associates", "Date", "Notes"), show="headings")
    event_tree.heading("Event", text="Event")
    event_tree.heading("Status", text="Status")
    event_tree.heading("Associates", text="Associates")
    event_tree.heading("Date", text="Date")
    event_tree.heading("Notes", text="Notes")

    event_tree.column("Event", width=150, anchor=tk.W)
    event_tree.column("Status", width=100, anchor=tk.W)
    event_tree.column("Associates", width=100, anchor=tk.W)
    event_tree.column("Date", width=100, anchor=tk.W)
    event_tree.column("Notes", width=400, anchor=tk.W)
    
    input_frame.pack(fill="x", padx=10, pady=10)
    tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    event_tree.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    load_data_from_json()
    
    root.mainloop()

### CODE TRIGGER ###

if __name__ == "__main__":
    display_login_window()
