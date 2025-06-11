from models.user import User
from enum import Enum

class Menu(Enum):
    LOGIN = 0
    SUPER_ADMIN_MAIN = 1
    SUPER_ADMIN_CREATE_SYSTEM_ADMIN = 2
    SUPER_ADMIN_DELETE_SYSTEM_ADMIN = 3
    SUPER_ADMIN_CREATE_SERVICE_ENGINEER = 4
    SUPER_ADMIN_DELETE_SERVICE_ENGINEER = 5
    SUPER_ADMIN_LIST_USERS = 6

menu_stack: list = []
current_user: User | None = None
last_menu_choice: str = "List Users"
