import tkinter as tk
from model import Model
from view import View
from controller import Controller
# Import libraries and classes from other files
# Check for logic issues please future me
# For the love of everything please use pygame

def main():
    root = tk.Tk()
    model = Model()
    view = View(root)
    controller = Controller(model, view, root)
    root.mainloop()

if __name__ == "__main__":
    main()
