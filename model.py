import os
import csv
from datetime import datetime, date
# Import libraries

user_list_file = 'users.csv'
tasklist_file = 'tasks.csv'
shared_with_file = 'task_shares.csv'
# Define file names in case user needs to change it (data conflicts)

def clean_text(text):
    if text is None:
        return ''
    # Return empty string if given nothing
    text = str(text).strip()
    # Remove whitespace
    text = text.replace(',', ';')
    # csv uses commas as seperator, so replace input commas with semicolons
    return text
    # Sanitze gross strings

def ensure_files_exist():
    if not os.path.exists(user_list_file):
        # If file does not exist, create file with headers
        with open(user_list_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password'])
        # If task file doesn't exist, make it
    if not os.path.exists(tasklist_file):
        with open(tasklist_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['task_id', 'owner', 'date', 'text', 'completed'])
    
    if not os.path.exists(shared_with_file):
        # If task share file doesn't exist, create it
        with open(shared_with_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['task_id', 'shared_with'])

def get_next_task_id():
    if not os.path.exists(tasklist_file):
        return 1
        # Return Error if task file is not real
    
    max_id = 0
    with open(tasklist_file, 'r', newline='') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 1:
                try:
                    task_id = int(row[0])
                    if task_id > max_id:
                        max_id = task_id
                # We want to ignore ALL errors, so just except in general
                except:
                    pass
                    
    return max_id + 1
# All the code above is only for csv writing (maybe make it a class?)

class Model:
    def __init__(self):
        ensure_files_exist()
        self.logged_in_user = None

    def register(self, username, password):
        # NOTE: Use regex for password req?
        username = clean_text(username)
        password = clean_text(password)
        
        if username == '' or password == '':
            return False, 'Username and password required'

        with open(user_list_file, "r", newline = "") as f:
            reader = csv.reader(f)
            next(reader, None) # skip
            for row in reader:
                if len(row) >= 1 and row[0] == username:
                    f.close()
                    return False, 'Username already exists'
        
        with open(user_list_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, password])
        return True, 'Registered successfully'

    def login(self, username, password):
        username = clean_text(username)
        password = clean_text(password)
        
        with open(user_list_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            found = False
            for row in reader:
                if len(row) >= 2 and row[0] == username and row[1] == password:
                    found = True
                    break

        if found:
            self.logged_in_user = username
            return True, 'Logged in'
        else:
            return False, 'Invalid username or password'

    def add_task(self, text, date_string):
        text = clean_text(text)
        if text == '':
            return False, 'Task cannot be empty'
        
        if self.logged_in_user is None:
            return False, 'Not logged in'
        
        try:
            parsed = datetime.strptime(date_string, '%Y-%m-%d').date()
        except:
            return False, 'Invalid date'
        
        task_id = get_next_task_id()
        date_str = parsed.strftime('%Y-%m-%d')
        
        with open(tasklist_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([task_id, self.logged_in_user, date_str, text, '0'])
        
        return True, 'Task added'

    def get_tasks(self):
        tasks = []
        if self.logged_in_user is None:
            return tasks
        
        shared_task_ids = []
        with open(shared_with_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2 and row[1] == self.logged_in_user:
                    try:
                        shared_task_ids.append(int(row[0]))
                    except:
                        pass
        
        with open(tasklist_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 5:
                    task_id = 0
                    try:
                        task_id = int(row[0])
                    except:
                        continue
                    
                    owner = row[1]
                    task_date = row[2]
                    text = row[3]
                    completed = row[4] == '1'

                    if owner == self.logged_in_user:
                        is_mine = True
                    else:
                        is_mine = False
                    if task_id in shared_task_ids:
                        is_shared_to_me = True
                    else:
                        is_shared_to_me = False
                    # Pyright hates this for some reason. Check later
                    
                    if is_mine or is_shared_to_me:
                        tasks.append({
                            'id': task_id,
                            'date': task_date,
                            'text': text,
                            'completed': completed,
                            'owner': owner,
                            'is_shared': is_shared_to_me
                        })
        return tasks

    def toggle_task(self, task_id):
        if self.logged_in_user is None:
            return False, 'Not logged in'
        
        shared_task_ids = []
        with open(shared_with_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2 and row[1] == self.logged_in_user:
                    try:
                        shared_task_ids.append(int(row[0]))
                    except:
                        # As with everything, ignore all errors
                        pass
            
        all_rows = []
        with open(tasklist_file, 'r', newline='') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            for row in reader:
                all_rows.append(row)
        
        found = False
        for i in range(len(all_rows)):
            row = all_rows[i]
            if len(row) >= 5:
                try:
                    task_id_search = int(row[0])
                except:
                    continue
                
                if task_id_search == task_id:
                    owner = row[1]
                    can_toggle = owner == self.logged_in_user or task_id in shared_task_ids
                    
                    if can_toggle:
                        current = row[4]
                        if current == '1':
                            all_rows[i][4] = '0'
                        else:
                            all_rows[i][4] = '1'
                        found = True
                    break
        
        if found:
            with open(tasklist_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for row in all_rows:
                    writer.writerow(row)
            return True, 'Task has been marked'
        else:
            return False, 'Task not found or no permission'

    def share_task(self, task_id, share_with_username):
        if self.logged_in_user is None:
            return False, 'Not logged in'
        # Should never run since login is required
        # Who knows, maybe theres a random thing I didn't catch
        
        share_with_username = clean_text(share_with_username)
        if share_with_username == '':
            return False, 'Username required'
            # Shouldn'y occur if user has brain
        
        if share_with_username == self.logged_in_user:
            return False, 'Cannot share with yourself'
            # Duh
        
        user_exists = False
        with open(user_list_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            # ignore header
            for row in reader:
                if len(row) >= 1 and row[0] == share_with_username:
                    user_exists = True
                    break
        
        if not user_exists:
            return False, 'User not found. Please try again later'
        
        task_found = False
        with open(tasklist_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    try:
                        task_id_search = int(row[0])
                    except:
                        continue
                    if task_id_search == task_id and row[1] == self.logged_in_user:
                        task_found = True
                        break
        
        if not task_found:
            return False, 'Task not found or you are not the owner'
        
        already_shared = False
        with open(shared_with_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    try:
                        task_id_search = int(row[0])
                    except:
                        continue
                    if task_id_search == task_id and row[1] == share_with_username:
                        already_shared = True
                        break
        
        if already_shared:
            return False, 'Already shared with this user'
        
        with open(shared_with_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([task_id, share_with_username])
        
        return True, 'Task shared with ' + share_with_username
        # Everything upward is to share a task

    def get_all_users(self):
        users = []
        with  open(user_list_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 1 and row[0] != self.logged_in_user:
                    users.append(row[0])
        return users

    def fetch_tasks_to_share(self):
        tasks = []
        if self.logged_in_user is None:
            return tasks
        # Again, should never occur. I don't know why I added this
        
        with open(tasklist_file, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 5 and row[1] == self.logged_in_user:
                    try:
                        task_id = int(row[0])
                    except:
                        continue
                    tasks.append({
                        'id': task_id,
                        'text': row[3],
                        'date': row[2]
                    })
        return tasks
