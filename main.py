from nicegui import ui
from datetime import date, timedelta
import os
import csv

from model import Model
from view import View
from controller import Controller
# Import libraries


def root():
    ui.tab("Calendar")
    data = read_data()
    print(data)
    colourmode()

model = Model()
view = View()
database = Database()
controller = Controller(model, view, database)

class Model:
    def __init__(self):
        self.model = Model

    def load_next_week():
        today = date.today()
        tomorrow1 = (today + timedelta(days = 1)).strftime("%Y-%m-%d")
        tomorrow2 = (today + timedelta(days = 2)).strftime("%Y-%m-%d")
        tomorrow3 = (today + timedelta(days = 3)).strftime("%Y-%m-%d")
        tomorrow4 = (today + timedelta(days = 4)).strftime("%Y-%m-%d")
        tomorrow5 = (today + timedelta(days = 5)).strftime("%Y-%m-%d")
        tomorrow6 = (today + timedelta(days = 6)).strftime("%Y-%m-%d")
        return [today, tomorrow1, tomorrow2, tomorrow3, tomorrow4, tomorrow5, tomorrow6]
    

class View:
    def __init__(self, model):
        self.model = Model()

    def display_date_picker():
        today = date.today().strftime("%Y-%m-%d")
        ui.date(value = today)

    def display_next_week_tasks(next_week, tasks_this_week):
        with ui.page_sticky("top-left", x_offset = 20, y_offset = 20):
            with ui.row():
                for date in next_week:
                    with ui.expansion(date):
                        ui.label(f"{PLACEHOLDER}").style('white-space: pre-wrap;')

    def light_or_dark_toggle():
        with ui.page_sticky("bottom-left", x_offset = 20, y_offset = 20):
            with ui.card():
                dark = ui.dark_mode()
                ui.button("Dark Mode", on_click = dark.enable).props('color=purple-7')
                ui.button("Light Mode", on_click = dark.disable).props('color=purple-7')
                ui.button("Auto", on_click = dark.auto).props('color=purple-7')  

    def login_signup_page():
        pass
    # idk this is not major rn

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
class Database:
    def __init__(self, recieved_dict):
        self.filename = "data.csv"
        self.recieved_dict = recieved_dict

    def check_file(self):
        if os.path.exists(self.filename):
            return True
        return False

    def read_data(self):
        if self.check_file(self):
            with open('todo.csv', 'r') as f:
                lines = f.readlines()
                return lines
        else:
            f = open('data.csv', 'x')
            f.close()
            return "No data could be found."

    def write_data(self, new_task_list, status_list, date, data):
        data = [
            {'ymd-date' : '2025/12/12', # YYYY-MM-DD
             'user' : 'cat',  # User
             'shared' : 'cat|dog', # Original task location | Copy location
             'taskname' : 'Test code', # Name to show task
             'status' : True} # True - complete | False - incomplete
        ] # Example expected format of data

        fieldnames = ['ymd-date', 'user', 'shared', 'taskname', 'status']
        with open(self.filename, 'a') as file:
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def clean_string(self):
        dictA = self.recieved_dict
        dictA.strip()
        if "," in string:
            string = string.replace(",", ";") # Replace comma with semicolon - close enough
        if not isinstance(dictA['status'], bool):
            pass


ui.run(root, dark = True)
