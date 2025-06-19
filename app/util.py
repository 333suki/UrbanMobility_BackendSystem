import re
from datetime import datetime

from models.traveler import Gender
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

def gender_to_string(gender: Gender) -> str | None:
    if gender == Gender.MALE:
        return "Male"
    elif gender == Gender.FEMALE:
        return "Female"
    elif gender == Gender.OTHER:
        return "Other"
    else:
        return None

def string_to_gender(gender: str) -> Gender | None:
    if gender == "Male":
        return Gender.MALE
    elif gender == "Female":
        return Gender.FEMALE
    elif gender == "Other":
        return Gender.OTHER
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

def is_valid_serial_number(serial_number: str) -> bool:
    if serial_number is None:
        return False
    return bool(re.match(r"^[a-zA-Z0-9]{10,17}$", serial_number))

def is_valid_scooter_brand(brand: str) -> bool:
    return True if brand else False

def is_valid_scooter_model(model: str) -> bool:
    return True if model else False

def is_valid_top_speed(top_speed: str) -> bool:
    if top_speed is None:
        return False
    if not top_speed.isnumeric():
        return False
    try:
        if int(top_speed) < 0:
            return False
    except ValueError:
        return False

    return True

def is_valid_battery_capacity(battery_capacity: str) -> bool:
    if battery_capacity is None:
        return False
    if not battery_capacity.isnumeric():
        return False
    try:
        if int(battery_capacity) < 0:
            return False
    except ValueError:
        return False

    return True

def is_valid_state_of_charge(state_of_charge: str) -> bool:
    if state_of_charge is None:
        return False
    if not state_of_charge.isnumeric():
        return False
    try:
        if int(state_of_charge) < 0 or int(state_of_charge) > 100:
            return False
    except ValueError:
        return False

    return True

def is_valid_target_range_soc(target_range_soc: str) -> bool:
    if target_range_soc is None:
        return False
    try:
        if int(target_range_soc.split(':')[0].strip()) < 0 or int (target_range_soc.split(':')[0].strip()) > 100 or int(target_range_soc.split(':')[1].strip()) < 0 or int (target_range_soc.split(':')[1].strip()) > 100 or int(target_range_soc.split(':')[0].strip()) > int(target_range_soc.split(':')[1].strip()):
            return False
    except Exception:
        return False

    return True

def is_valid_location(location: str) -> bool:
    if location is None:
        return False
    try:
        float(location.split(':')[0].strip())
        float(location.split(':')[1].strip())
    except Exception:
        return False

    return True

def is_valid_mileage(mileage: str) -> bool:
    if mileage is None:
        return False
    if not mileage.isnumeric():
        return False
    try:
        if int(mileage) < 0:
            return False
    except ValueError:
        return False

    return True

def is_valid_last_maintenance_date(last_maintenance_date: str) -> bool:
    if last_maintenance_date is None:
        return False
    try:
        datetime.strptime(last_maintenance_date, "%Y-%m-%d")
    except Exception:
        return False

    return True
