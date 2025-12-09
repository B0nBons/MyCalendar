from nicegui import ui
from model import Model
from view import View
from controller import Controller
# Import libraries and classes from other files

model = Model()
view = View()
controller = Controller(model, view)
ui.run(title = 'ToDo List', dark = True)
# Run UI
