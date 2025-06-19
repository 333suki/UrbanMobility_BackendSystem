from database import Database
from login import login_screen
import state
from state import Menu
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    Database.set_database_file_name(os.path.join(DATA_DIR, "database.db"))
    Database.create_users_table()
    Database.create_travelers_table()
    Database.create_scooter_table()
    Database.create_logs_table()
    Database.creat_suspicious_logs_table()
    state.menu_stack.append(Menu.LOGIN)
    login_screen()
