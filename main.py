from nicegui import ui
from datetime import date, timedelta

def root():
    ui.tab("Calendar")
    next_week()
    colourmode()

def next_week():
    today = date.today()
    tomorrow1 = (today + timedelta(days = 1)).strftime("%Y-%m-%d")
    tomorrow2 = (today + timedelta(days = 2)).strftime("%Y-%m-%d")
    tomorrow3 = (today + timedelta(days = 3)).strftime("%Y-%m-%d")
    tomorrow4 = (today + timedelta(days = 4)).strftime("%Y-%m-%d")
    tomorrow5 = (today + timedelta(days = 5)).strftime("%Y-%m-%d")
    tomorrow6 = (today + timedelta(days = 6)).strftime("%Y-%m-%d")

    next_week = [today, tomorrow1, tomorrow2, tomorrow3, tomorrow4, tomorrow5, tomorrow6]
    with ui.page_sticky("top-left", x_offset = 20, y_offset = 20):

        with ui.row():
            for item in range(len(next_week)):
                with ui.card():
                    if next_week[item] == today:
                        ui.label(f"Today\n{today}").style('white-space: pre-wrap;')
                    elif next_week[item] == tomorrow1:
                        ui.label(f"Tomorrow\n{tomorrow1}").style('white-space: pre-wrap;')
                    else:
                        ui.label(f"Soon\n{next_week[item]}").style('white-space: pre-wrap;')
                    
            ui.separator()
    

def colourmode():
    with ui.page_sticky("top-right", x_offset = 20, y_offset = 20):
        with ui.card():
            dark = ui.dark_mode()
            ui.button("Dark Mode", on_click = dark.enable).props('color=purple-7')
            ui.button("Light Mode", on_click = dark.disable).props('color=purple-7')
            ui.button("Auto", on_click = dark.auto).props('color=purple-7')

ui.run(root, dark = True)