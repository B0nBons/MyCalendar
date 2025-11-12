import tkinter as tk
from tkcalendar import Calendar, DateEntry
from datetime import date
# Import needed libraries

class View:
    def __init__(self, root): # Define method with __ to ensure 'pythonic' language idk read too many articles
        self.root = root
        self.root.configure(background = "ivory")

        self.root.title("Test123's Tasks") # CHANGE THIS TO AN OFFICIAL NAME
        # Name of application window

        self.month_label = tk.Label(root, text="Month: ")
        self.month_label.pack()
        # Month label for top
        # Overall, somewhat useless seeing as their is no physical calendar

        self.task_entry = tk.Entry(root)
        self.task_entry.pack()
        # This is the field that lets the user type in tasks
        # It looks ugly. 

        self.add_button = tk.Button(root, text="Add Task")
        self.add_button.pack()
        # Add task

        self.remove_button = tk.Button(root, text="Remove Selected")
        self.remove_button.pack()
        # Remove task (you need to click on the task, then select to remove it)

        self.save_button = tk.Button(root, text="Save Tasks")
        self.save_button.pack()
        # Save tasks by writing to csv

        self.load_button = tk.Button(root, text="Load Tasks")
        self.load_button.pack()
        # Load tasks from csv NOTE: can use txt, csv isnt needed
        # NOTE: DOES NOT SAVE UNSAVED TASKS ON EXIT OF PROGRAM

        self.change_col_button = tk.Button(root, text = "Change Theme")
        self.change_col_button.pack()
        # IDK IF THIS WORKS

        self.task_listbox = tk.Listbox(root, width=50)
        self.task_listbox.pack(pady=20) # Change padding later

        self.prev_button = tk.Button(root, text="<-- Previous Month")
        self.prev_button.pack(side="left", padx=10)
        # This isnt really used yet

        self.next_button = tk.Button(root, text="Next Month -->")
        self.next_button.pack(side="right", padx=10)
        # This still isnt used yet

        self.calendar = Calendar(root,
                                 font = "Arial 12",
                                 selectmode = 'day'
                                 locale = 'en_us'
                                 cursor = 'hand1'
                                 year = date.today().year,
                                 month = date.today().month,
                                 day = date.today().day)


# NOTE: Last two methods need to be implemented into an actual calendar view
# NOTE: They both do nothing for now
