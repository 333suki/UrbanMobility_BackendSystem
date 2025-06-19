from enum import Enum
from datetime import datetime

class Gender(Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2


class Traveler:
    def __init__(self, ID: int, first_name: str, last_name: str, birthday: datetime, gender: Gender, street_name: str, house_number: str, zip_code: str, city: str, email: str, phone_number: str, driving_license_number: str, registration_date: datetime):
        self.ID: int = ID
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.birthday: datetime = birthday
        self.gender: Gender = gender
        self.street_name: str = street_name
        self.house_number: str = house_number
        self.zip_code: str = zip_code
        self.city: str = city
        self.email: str = email
        self.phone_number: str = phone_number
        self.driving_license_number: str = driving_license_number
        self.registration_date: datetime = registration_date
