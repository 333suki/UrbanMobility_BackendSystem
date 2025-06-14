from models.user import User
from enum import Enum

class Menu(Enum):
    LOGIN = 0
    SUPER_ADMIN_MAIN = 1
    SUPER_ADMIN_CREATE_ACCOUNT = 2
    SUPER_ADMIN_UPDATE_ACCOUNT = 3
    SUPER_ADMIN_DELETE_ACCOUNT = 4
    SUPER_ADMIN_LIST_USERS = 5

    SYSTEM_ADMIN_MAIN = 7
    SYSTEM_ADMIN_LIST_USERS = 8
    SYSTEM_ADMIN_CREATE_ACCOUNT = 9
    SYSTEM_ADMIN_UPDATE_ACCOUNT = 10
    SYSTEM_ADMIN_DELETE_ACCOUNT = 11

menu_stack: list = []
current_user: User | None = None
last_menu_choice: str = "List Users"
