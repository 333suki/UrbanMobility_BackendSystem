from models.user import User
from enum import Enum

class Menu(Enum):
    LOGIN = 0
    SUPER_ADMIN_MAIN = 1
    SUPER_ADMIN_CREATE_ACCOUNT = 2
    SUPER_ADMIN_UPDATE_ACCOUNT = 3
    SUPER_ADMIN_DELETE_ACCOUNT = 4
    SUPER_ADMIN_LIST_USERS = 5

menu_stack: list = []
current_user: User | None = None
last_menu_choice: str = "List Users"
