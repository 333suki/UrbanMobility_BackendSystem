from enum import Enum
from datetime import datetime

class Role(Enum):
    SUPER_ADMIN = 0
    SYSTEM_ADMIN = 1
    SERVICE_ENGINEER = 2


class User:
    def __init__(self, ID: int, username: str, role: Role, first_name: str | None, last_name: str | None, registration_date: datetime | None):
        self.ID: int = ID
        self.username: str = username
        self.role: Role = role
        self.first_name: str | None = first_name
        self.last_name: str | None = last_name
        self.registration_date: datetime | None = registration_date
