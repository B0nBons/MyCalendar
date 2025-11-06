import tkinter as tk
# Import needed libraries

class View:
    def __init__(self, root): # Define method with __ to ensure 'pythonic' language idk read too many articles
        self.root = root
        self.root.title("please work for once")
        # Name of application window

        self.month_label = tk.Label(root, text="Month: ")
        self.month_label.pack()
        # Month label for top

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack()
        # This is the field that lets the user type in tasks

        self.add_button = tk.Button(root, text="Add Task")
        self.add_button.pack()
        # Add task

        self.remove_button = tk.Button(root, text="Remove Selected")
        self.remove_button.pack()
        # Remove task

        self.save_button = tk.Button(root, text="Save Tasks")
        self.save_button.pack()
        # Save tasks by writing to csv

        self.load_button = tk.Button(root, text="Load Tasks")
        self.load_button.pack()
        # Load tasks from csv NOTE: can use txt, csv isnt needed
        # NOTE: DOES NOT SAVE UNSAVED TASKS

        self.task_listbox = tk.Listbox(root, width=50)
        self.task_listbox.pack(pady=20) # Change padding later

        self.prev_button = tk.Button(root, text="< Previous Month")
        self.prev_button.pack(side="left", padx=10)
        # This isnt really used yet

        self.next_button = tk.Button(root, text="Next Month >")
        self.next_button.pack(side="right", padx=10)
        # This still isnt used yet

# NOTE: Last two methods need to be implemented into an actual calendar view
# NOTE: They both do nothing for now