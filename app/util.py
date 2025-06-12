import re

from models.user import Role

def parse_string(string: str | None) -> str:
    return string if string else "None"

def role_to_string(role: Role) -> str | None:
    if role == Role.SUPER_ADMIN:
        return "Super Administrator"
    elif role == Role.SYSTEM_ADMIN:
        return "System Administrator"
    elif role == Role.SERVICE_ENGINEER:
        return "Service Engineer"
    else:
        return None

def string_to_role(role: str) -> Role | None:
    if role == "Super Administrator":
        return Role.SUPER_ADMIN
    elif role == "System Administrator":
        return Role.SYSTEM_ADMIN
    elif role == "Service Engineer":
        return Role.SERVICE_ENGINEER
    else:
        return None

def is_valid_password(password: str) -> bool:
    if not password:
        return False
    # Length 12-30, at least one digit, one special character, one lower- and one uppercase letter
    return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%&_\-+=`|\\(){}\[\]:;'<>,.?/]).{12,30}$", password))

def is_valid_username(username: str) -> bool:
    if not username:
        return False
    # Length 8-10, start with letter or underscore, case-insensitive
    return bool(re.match(r"^[a-zA-Z_][a-zA-Z0-9_'.]{7,9}$", username, re.IGNORECASE))

def is_valid_first_name(first_name: str) -> bool:
    return True if first_name else False

def is_valid_last_name(last_name: str) -> bool:
    return True if last_name else False
