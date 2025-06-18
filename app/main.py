from database import Database
from login import login_screen
import state
from state import Menu
import os

if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    
    Database.set_database_file_name("data/database.db")
    Database.create_users_table()
    Database.create_travelers_table()
    Database.create_scooter_table()
    Database.create_logs_table()
    Database.creat_suspicious_logs_table()
    state.menu_stack.append(Menu.LOGIN)
    login_screen()
