from models.user import User
from enum import Enum

class Menu(Enum):
    LOGIN = 0
    SUPER_ADMIN = 1

menu_stack: list = []
current_user: User | None = None
