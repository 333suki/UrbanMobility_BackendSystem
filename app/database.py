import sqlite3
import os
from datetime import datetime

from encryptor import Encryptor
from models.user import Role
from models.user import User
from models.log import Log
import util

class Database:
    database_file_name: str | None = None

    @staticmethod
    def set_database_file_name(database_file_name: str):
        os.makedirs(os.path.dirname(database_file_name), exist_ok=True)
        Database.database_file_name = database_file_name

    @staticmethod
    def create_users_table():
        with sqlite3.connect(Database.database_file_name) as conn:
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

    @staticmethod
    def create_travelers_table():
        with sqlite3.connect(Database.database_file_name) as conn:
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

    @staticmethod
    def create_scooter_table():
        with sqlite3.connect(Database.database_file_name) as conn:
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

    @staticmethod
    def insert_user(username: str, password: str, role: Role, first_name: str, last_name: str, registration_date: str | None):
        with sqlite3.connect(Database.database_file_name) as conn:
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
    @staticmethod
    def update_user_with_password(ID: int, username: str, password: str, role: Role, first_name: str, last_name: str):
        with sqlite3.connect(Database.database_file_name) as conn:
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
    @staticmethod
    def update_user(ID: int, username: str, role: Role, first_name: str, last_name: str):
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Users
                    SET username = ?, role = ?, first_name = ?, last_name = ?
                    WHERE ID = ?
                """,
                (username, role.value, first_name, last_name, ID)
            )
            conn.commit()

    @staticmethod
    def delete_user(ID: int):
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM Users
                    WHERE ID = ?
                """,
                (ID, )
            )
            conn.commit()

    @staticmethod
    def get_user(ID: int) -> User | None:
        with sqlite3.connect(Database.database_file_name) as conn:
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


    @staticmethod
    def get_user_by_username(username: str) -> User | None:
        for user in Database.get_all_users():
            if user.username.lower() == username.lower():
                return user
        return None


    @staticmethod
    def get_all_users() -> list[User]:
        all_users: list[User] = []
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Users
                """
            )
            for result in cursor.fetchall():
                all_users.append(User(int(result[0]), Encryptor.decrypt(result[1]), Role(result[3]), Encryptor.decrypt(result[4]), Encryptor.decrypt(result[5]), datetime.strptime(Encryptor.decrypt(result[6]), "%Y-%m-%d")))

        return all_users

    @staticmethod
    def get_all_users_dict() -> dict:
        all_system_users_dict = {}
        with sqlite3.connect(Database.database_file_name) as conn:
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

    @staticmethod
    def get_all_engineers_dict() -> dict:
        all_engineers_dict = {}
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT *
                FROM Users
                """
            )
            for result in cursor.fetchall():
                if Role (result[3]) == Role.SERVICE_ENGINEER:
                    all_engineers_dict[f"Name: {Encryptor.decrypt(result[4])} {Encryptor.decrypt(result[5])}, Role: {util.role_to_string(Role(result[3]))}, Username: {Encryptor.decrypt(result[1])}, Registration Date: {Encryptor.decrypt(result[6])}"] = result[0]

        return all_engineers_dict


    @staticmethod
    def username_exist(username: str | None, allowed_username: str | None) -> bool:
        if username is None:
            return False
        for user in Database.get_all_users():
            if user.username.lower() == username.lower():
                if allowed_username is None:
                    return True
                else:
                    return user.username != allowed_username
        return False

    @staticmethod
    def validate(username: str, password: str) -> bool:
        for user in Database.get_all_users():
            if user.username.lower() == username.lower():
                with sqlite3.connect(Database.database_file_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        SELECT *
                        FROM Users
                            WHERE ID = ? AND password = ?
                        """,
                        (user.ID, Encryptor.get_hash(password))
                    )
                    result = cursor.fetchone()
                    if result:
                        return True
                    return False
        return False

    @staticmethod
    def create_logs_table():
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Logs (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime DATE NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    description VARCHAR(255) NOT NULL,
                    additional_info VARCHAR(255),
                    suspicious INT NOT NULL
                )
                """
            )

    @staticmethod
    def insert_log(datetime: str, username: str, description: str, additional_info: str, suspicious: int):
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Logs(datetime, username, description, additional_info, suspicious)
                    VALUES (?, ?, ?, ?, ?)
                """,
                (datetime, username, description, additional_info, suspicious)
            )
            conn.commit()

    @staticmethod
    def get_all_logs():
        all_logs: list[Log] = []
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Logs
                """
            )
            for result in cursor.fetchall():
                all_logs.append(Log(int(result[0]), datetime.strptime(Encryptor.decrypt(result[1]), "%Y-%m-%d %H:%M:%S"), Encryptor.decrypt(result[2]), Encryptor.decrypt(result[3]), Encryptor.decrypt(result[4]), int(result[5])))
        return all_logs