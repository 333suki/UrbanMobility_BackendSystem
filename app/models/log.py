from datetime import datetime

class Log:
    def __init__(self, ID: int, datetime: datetime, username: str, description: str, additional_info: str, suspicious: int):
        self.ID: int = ID
        self.datetime: datetime = datetime
        self.username: str = username
        self.description: str = description
        self.additional_info: str | None = additional_info
        self.suspicious: int = suspicious