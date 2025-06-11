from database import Database
from login_screen import login_screen
from state import Menu
import state

if __name__ == "__main__":
    database = Database("data/database.db")
    state.menu_stack.append(Menu.LOGIN)
    login_screen()
