from login import login_screen
import state
from state import Menu

if __name__ == "__main__":
    state.menu_stack.append(Menu.LOGIN)
    login_screen()
