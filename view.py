# view.py
from nicegui import ui
from datetime import date, timedelta

class View:
    def __init__(self):
        self.root_container = ui.column()
        
        self.login_user_input = None
        self.login_pass_input = None
        self.register_button = None
        self.login_button = None
        self.login_message_label = None

        self.date_picker = None
        self.task_input = None
        self.add_button = None
        self.refresh_button = None
        self.week_container = None
        self.tasks_column = None
        self.checkbox_callback = None
        
        self.share_task_dropdown = None
        self.share_user_dropdown = None
        self.share_button = None
        self.share_message_label = None
        # nicegui needs to hold the areas for the UI
        # This way there won't be any gross formatting and overlap

    def login_page(self):
        self.root_container.clear()
        with self.root_container:
            ui.label('Task Calendar').classes('text-3xl font-bold mb-4')
            ui.label('Register or Login')
            
            with ui.card().classes('w-96 p-4'):
                self.login_user_input = ui.input(label='Username').classes('w-full')
                self.login_pass_input = ui.input(label='Password', password=True).classes('w-full')
                
                with ui.row().classes('mt-4'):
                    self.register_button = ui.button('Register').props('color=purple-7')
                    self.login_button = ui.button('Login').props('color=purple-7')
                
                self.login_message_label = ui.label('').classes('mt-2 text-red-500')

# Above is for login and auth, below is for app
    
    def app_page(self):
        self.root_container.clear()
        with self.root_container:
            ui.label('Task Calendar').classes('text-3xl font-bold mb-4')

            with ui.card().classes('w-full p-4 mb-4'):
                ui.label('Add Task').classes('text-lg font-medium mb-2')
                with ui.row().classes('items-end gap-4'):
                    self.date_picker = ui.date(value=date.today()).classes('w-48')
                    # We define date_picker to initally have todays date
                    self.task_input = ui.input(label='Task').classes('w-64')
                    self.add_button = ui.button('Add').props('color=purple-7')
                    self.refresh_button = ui.button('Refresh').props('color=purple-7')

            with ui.card().classes('w-full p-4 mb-4'):
                ui.label('Share Task').classes('text-lg font-medium mb-2')
                with ui.row().classes('items-end gap-4'):
                    self.share_task_dropdown = ui.select({}, label='Your Task').classes('w-64')
                    self.share_user_dropdown = ui.select([], label='Share With').classes('w-48')
                    self.share_button = ui.button('Share').props('color=purple-7')
                self.share_message_label = ui.label('').classes('mt-2')

            ui.separator()
            ui.label('Next 7 Days').classes('text-xl font-bold mt-4 mb-2')
            self.week_container = ui.column().classes('w-full')

            ui.separator()
            ui.label('Tasks for Selected Day').classes('text-xl font-bold mt-4 mb-2')
            self.tasks_column = ui.column().classes('w-full p-2')

    def set_login_message(self, text):
        if self.login_message_label:
            self.login_message_label.text = text

    def set_share_message(self, text):
        if self.share_message_label:
            self.share_message_label.text = text

    def clear_week(self):
        if self.week_container:
            self.week_container.clear()

    def clear_tasks(self):
        if self.tasks_column:
            self.tasks_column.clear()

    def draw_next_seven_days(self, tasks, call):
        self.clear_week()
        
        with self.week_container:
            with ui.row().classes('gap-2 flex-wrap'):
                today = date.today()
                for i in range(7):
                    day = today + timedelta(days=i)
                    day_str = day.strftime('%Y-%m-%d')
                    
                    day_tasks = []
                    for t in tasks:
                        if t['date'] == day_str:
                            day_tasks.append(t)
                    
                    if i == 0:
                        label = 'Today'
                    elif i == 1:
                        label = 'Tomorrow'
                    else:
                        label = day.strftime('%A')
                        # Had to google date formatting
                    
                    with ui.card().classes('w-48 min-h-32'):
                        ui.label(label).classes('font-bold')
                        ui.label(day_str).classes('text-sm text-gray-500')
                        ui.label(str(len(day_tasks)) + ' task(s)').classes('text-sm')
                        
                        if len(day_tasks) > 0:
                            with ui.column().classes('mt-2'):
                                for t in day_tasks:
                                    with ui.row().classes('items-center'):
                                        cb = ui.checkbox(value=t['completed']).classes('text-sm')
                                        cb.on('update:model-value', lambda e, task_id=t['id']: call(task_id))
                                        # We again use lambda, since defining a func
                                        # For this task would be inefficient
                                        
                                        text = t['text']
                                        if len(text) > 18:
                                            text = text[:18] + '...'
                                            # Cut text that it too long for box
                                        if t['is_shared']:
                                            text = text + ' [' + t['owner'] + ']'
                                        
                                        style = 'text-sm'
                                        if t['completed']:
                                            style = 'text-sm line-through'
                                        
                                        ui.label(text).classes(style)
