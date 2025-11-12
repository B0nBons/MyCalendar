import datetime
import calendar
import os
# Import needed libraries

class Model:
    def __init__(self):
        self.tasks = []
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year
        self.db = self.Database()

    def monthDOWN(self): # Go BACK in time (feb -> Jan)
        if self.current_month < 12:
            self.current_month += 1
        else:
            self.current_month = 1
            self.current_year += 1

    def monthUP(self): # Go FORWARD in time (sept -> oct)
        if self.current_month > 1:
            self.current_month -= 1
        else:
            self.current_month = 12
            self.current_year -= 1

    def check_tasks(self): # common sense, but looks nice
        return self.tasks

    def check_leap(self): # Mainly unused for now, needed for calendar dates on GUI in the future
        return calendar.isleap(self.current_year)

    def add_task(self, task): # NOTE: MAKE THIS SAFE FROM COMMAND INJECTION. THIS IS UNSAFE
        if task != "":
            task = task.strip()
            self.tasks.append(task)

    def remove_task(self, index):
        if index >= 0 and index < len(self.tasks):
            del self.tasks[index] # NOTE: Make it so the user can actually use a CHECKLIST.
                                  # NOTE: And their tasks aren't deleted off the face of earth
                
    def change_colour_theme(self, req = 1):
        theme1 = {'bg' :'lightblue', 
                  'fg' : 'darkblue'}
        theme2 = {"bg" : 'honeydew2',
                  'fg' : 'SlateBlue4'}
        theme3 = {"bg" : 'LightPink1', 
                  'fg' : 'firebrick4'}
        if req == 1:
            return theme1
        elif req == 2:
            return theme2
        else:
            return theme3

    class Database: # Make this a standalone class maybe? Works fine so maybe not
        def __init__(self):
            self.filename = "data.csv" # CAN CHANGE THIS TO DATA.TXT instead

        def check_data_path(self):
            return os.path.exists(self.filename)

        def load_tasklist(self):
            tasks = []
            if self.check_data_path():
                with open(self.filename, "r") as file:
                    for line in file:
                        line = line.strip()
                        if line:
                            tasks.append(line)
            return tasks

        def save_tasklist(self, tasks): 
            with open(self.filename, "w") as file:  # Maybe change this to append instead(?)
                for task in tasks:
                    file.write(task + "\n")
