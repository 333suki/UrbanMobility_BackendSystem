import sqlite3
import os
from datetime import datetime

from encryptor import Encryptor
from models.user import Role
from models.user import User
import util

class Database:
    def __init__(self, database_file_name: str):
        os.makedirs(os.path.dirname(database_file_name), exist_ok=True)
        self.database_file_name = database_file_name
        self.connection: sqlite3.Connection | None = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.database_file_name)
        self.create_users_table()
        self.create_travelers_table()
        self.create_scooter_table()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

    def create_users_table(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Users (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role INT NOT NULL,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    registration_date DATE NOT NULL
            )
                """
            )

    def create_travelers_table(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Travelers (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    birthday DATE NOT NULL,
                    gender INT NOT NULL,
                    street_name VARCHAR(255) NOT NULL,
                    house_number VARCHAR(255) NOT NULL,
                    zip_code CHAR(6) NOT NULL,
                    city VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    phone_number CHAR(15) NOT NULL,
                    driving_license_number VARCHAR(9) NOT NULL,
                    registration_date DATE NOT NULL
                )
                """
            )

    def create_scooter_table(self):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Scooters (
                    ID VARCHAR(17) NOT NULL UNIQUE,
                    brand VARCHAR(255) NOT NULL,
                    model VARCHAR(255) NOT NULL,
                    top_speed INT NOT NULL,
                    battery_capacity INT NOT NULL,
                    state_of_charge INT NOT NULL,
                    target_range_soc VARCHAR(255) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    out_of_service_status INT NOT NULL,
                    mileage INT NOT NULL,
                    last_maintenance_date DATE NOT NULL,
                    PRIMARY KEY(ID)
                )
                """
            )

    def insert_user(self, username: str, password: str, role: Role, first_name: str, last_name: str, registration_date: str | None):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Users(username, password, role, first_name, last_name, registration_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                (username, password, role.value, first_name, last_name, registration_date)
            )
            conn.commit()

    # With password
    def update_user(self, ID: int, username: str, password: str, role: Role, first_name: str, last_name: str):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Users
                    SET username = ?, password = ?, role = ?, first_name = ?, last_name = ?
                    WHERE ID = ?
                """,
                (username, password, role.value, first_name, last_name, ID)
            )
            conn.commit()

    # Without password
    def update_user(self, ID: int, username: str, role: Role, first_name: str, last_name: str):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Users
                    SET username = ?, role = ?, first_name = ?, last_name = ?
                    WHERE ID = ?
                """,
                (username,role.value, first_name, last_name, ID)
            )
            conn.commit()

    def delete_user(self, ID: int):
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM Users
                    WHERE ID = ?
                """,
                (ID, )
            )
            conn.commit()

    def get_user(self, ID: int) -> User | None:
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Users
                    WHERE ID = ?
                """,
                (ID, )
            )
            result = cursor.fetchone()
            if result:
                return User(int(result[0]), Encryptor.decrypt(result[1]), Role(result[3]), Encryptor.decrypt(result[4]), Encryptor.decrypt(result[5]), datetime.strptime(Encryptor.decrypt(result[6]), "%Y-%m-%d"))
            return None


    def get_all_users(self) -> list[User]:
        all_users: list[User] = []
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Users
                """
            )
            for result in cursor.fetchall():
                all_users.append(User(int(result[0]), Encryptor.decrypt(result[1]), Role(result[3]), Encryptor.decrypt(result[4]), Encryptor.decrypt(result[5]), datetime.strptime(Encryptor.decrypt(result[6]), "%Y-%m-%d")))

        return all_users

    def get_all_users_dict(self) -> dict:
        all_system_users_dict = {}
        with self.connection as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT *
                FROM Users
                """
            )
            for result in cursor.fetchall():
                all_system_users_dict[f"Name: {Encryptor.decrypt(result[4])} {Encryptor.decrypt(result[5])}, Role: {util.role_to_string(Role(result[3]))}, Username: {Encryptor.decrypt(result[1])}, Registration Date: {Encryptor.decrypt(result[6])}"] = result[0]

        return all_system_users_dict


    def username_already_exist(self, username: str, allowed_username: str | None) -> bool:
        for user in self.get_all_users():
            if user.username == username:
                if allowed_username is None:
                    return True
                else:
                    return user.username != allowed_username
        return False
