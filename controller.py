from model import Model
from view import View
from datetime import datetime, date
from nicegui import ui
# Import libraries
# We do import nicegui here
# NOTE: I JUST NOTICED THAT ALL THE DATES SEEM TO BE AHEAD BY ONE FOR SOME REASON
# NOTE: ^ Seems that it's due to VPN. Check later

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # Init View and Model
        
        self.view.login_page()
        self.view.register_button.on_click(self.handle_register)
        self.view.login_button.on_click(self.handle_login)
        # Display login page and require auth

    def handle_register(self):
        username = self.view.login_user_input.value
        password = self.view.login_pass_input.value
        ok, msg = self.model.register(username, password)
        self.view.set_login_message(msg)
        # If user presses register, show a label that either confirms or disallows user to continue

    def handle_login(self):
        username = self.view.login_user_input.value
        password = self.view.login_pass_input.value
        ok, msg = self.model.login(username, password)
        self.view.set_login_message(msg)
        if ok:
            self.show_app_page()
        # If login works, then it shows the actual todo list/calendar 

    def show_app_page(self):
        self.view.app_page()
        self.view.add_button.on_click(self.handle_add_task)
        self.view.refresh_button.on_click(self.handle_refresh)
        self.view.share_button.on_click(self.handle_share)
        self.view.checkbox_togg = self.handle_toggle
        self.view.date_picker.on('update:model-value', self.handle_date_change)
        self.refresh_all()
        # Refresh everything

    def handle_add_task(self):
        text = self.view.task_input.value
        picked = self.view.date_picker.value
        if type(picked) is date:
            date_str = picked.strftime('%Y-%m-%d')
        else:
            try:
                parsed = datetime.strptime(str(picked), '%Y-%m-%d').date()
                date_str = parsed.strftime('%Y-%m-%d')
            except:
                # Again, all errors need to be ignored (though there shouldn't be any,
                # since NiceGUI's datepicker element returns datetype object)
                date_str = date.today().strftime('%Y-%m-%d')
        
        ok, msg = self.model.add_task(text, date_str)
        if ok:
            self.view.task_input.value = ''
            self.refresh_all()

    def handle_refresh(self):
        # Changes the "tasks for selected day" label
        self.refresh_all()

    def handle_date_change(self, go):
        self.draw_selected_day(go.args)

    def handle_toggle(self, task_id):
        # Check or uncheck task
        self.model.toggle_task(task_id)
        self.refresh_all()

    def handle_share(self):
        task_val = self.view.share_task_dropdown.value
        user_val = self.view.share_user_dropdown.value
        
        if not task_val or not user_val:
            self.view.set_share_message('Select a task and a user')
            return
        
        try:
            task_id = int(task_val)
        except:
            self.view.set_share_message('Invalid task')
            return
        # Should never run. Failsafe

        ok, msg = self.model.share_task(task_id, user_val)
        self.view.set_share_message(msg)
        if ok:
            self.refresh_all()

    def refresh_all(self):
        tasks = self.model.get_tasks()
        self.draw_week(tasks)
        
        pick = self.view.date_picker.value
        if type(pick) is date:
            date_str = pick.strftime('%Y-%m-%d')
        else:
            if pick != "" :
                date_str = str(pick)
            else:
                # Should never run
                date_str = date.today().strftime('%Y-%m-%d')

        
        self.draw_selected_day(date_str, tasks)
        self.update_dropdowns()

    def update_dropdowns(self):
        users = self.model.get_all_users()
        self.view.share_user_dropdown.options = users
        self.view.share_user_dropdown.update()
        
        my_tasks = self.model.fetch_tasks_to_share()
        options = {}
        for task in my_tasks:
            options[str(task['id'])] = (task['date'] + ': ' + task['text'][:25])
            # Very ugly in code. We need this for the date, and to cut off long text
        self.view.share_task_dropdown.options = options
        self.view.share_task_dropdown.update()

    def draw_week(self, tasks):
        self.view.draw_next_seven_days(tasks, self.handle_toggle)

    def draw_selected_day(self, selected_date, tasks=None):
        if tasks is None:
            tasks = self.model.get_tasks()
        self.view.clear_tasks()
        
        if type(selected_date) is date:
            date_str = selected_date.strftime('%Y-%m-%d')
        else:
            try:
                cleaned = datetime.strptime(str(selected_date), '%Y-%m-%d').date()
                date_str = cleaned.strftime('%Y-%m-%d')
            except:
                date_str = date.today().strftime('%Y-%m-%d')
                
        found = False
        for task in tasks:
            if task['date'] == date_str:
                found = True
                
                done_text = 'Done' if task['completed'] else 'Pending'
                shared_text = ''
                if task['is_shared']:
                    shared_text = ' [from ' + task['owner'] + ']'
                
                with self.view.tasks_column:
                    with ui.row().classes('items-center'):
                        check = ui.checkbox(value=task['completed'])
                        check.on('update:model-value', lambda checkbox, task_id=task['id']: self.handle_toggle(task_id)) 
                        # We have to use lambda since it wants a function. Won't work otherwise
                        ui.label(task['text'] + shared_text + ' [' + done_text + ']')
        
        if not found:
            with self.view.tasks_column:
                ui.label('No tasks for this day')
