import datetime as dt 
import random
import tkinter as tk
# Import libraries

class Controller:
    def __init__(self, model, view, root):
        self.model = model
        self.view = view
        self.root = root

        # Set initial month label
        self.update_month_label()

        # Add buttons from view
        self.view.add_button.config(command = self.add_task)
        self.view.remove_button.config(command = self.remove_task)
        self.view.save_button.config(command = self.save_tasks)
        self.view.load_button.config(command = self.load_tasks)
        self.view.next_button.config(command = self.next_month)
        self.view.prev_button.config(command = self.prev_month)
        self.view.change_col_button.config(command = self.change_col)

    def update_month_label(self): # This is literally useless right now
        month_name = dt.date(1900, self.model.current_month, 1).strftime('%B') # google said %B returns whole month name
        month_label = "Month: " + month_name + " " + str(self.model.current_year)
        self.view.month_label.config(text=month_label)
        # Only use if it has a visual calendar with tasks that change by month
        # Or a cool feature like that bc this is stupid why did i even do this

    def add_task(self):
        task = self.view.task_entry.get()
        self.model.add_task(task)
        self.view.task_entry.delete(0, 'end')
        self.refresh_tasklist()

    def remove_task(self):
        # User needs to click on the task they want to remove then click remove
        click = self.view.task_listbox.curselection()
        if click:
            index = click[0]
            self.model.remove_task(index)
            self.refresh_tasklist()

    def save_tasks(self):
        self.model.db.save_tasklist(self.model.tasks)

    def load_tasks(self):
        self.model.tasks = self.model.db.load_tasklist()
        self.refresh_tasklist()

    def next_month(self):
        self.model.monthDOWN()
        self.update_month_label()

    def prev_month(self):
        self.model.monthUP()
        self.update_month_label()
    
    def change_col(self):
        theme_num = random.randint(1,3)
        theme = self.model.change_colour_theme(theme_num)
        if theme_num == 1:    
            self.root.configure(background='lightblue')
            self.view.task_listbox.configure(bg = "mint cream", fg = "darkblue")

        elif theme_num == 2:
            self.root.configure(background = "honeydew2")
            self.view.task_listbox.configure(bg = "pale turquoise", fg = "SlateBlue4")

        else:
            self.root.configure(background = "LightPink1")
            self.view.task_listbox.configure(bg = "plum1", fg = "firebrick4")

        self.view.month_label.configure(**theme)
        self.view.task_entry.configure(**theme)
        self.view.add_button.configure(**theme)
        self.view.remove_button.configure(**theme)
        self.view.save_button.configure(**theme)
        self.view.load_button.configure(**theme)
        self.view.change_col_button.configure(**theme)
        self.view.prev_button.configure(**theme)
        self.view.next_button.configure(**theme)

    def refresh_tasklist(self):
        self.view.task_listbox.delete(0, 'end')
        for t in self.model.tasks:
            self.view.task_listbox.insert('end', t)
