import sqlite3
import os
from datetime import datetime

from encryptor import Encryptor
from models.user import Role
from models.user import User
from models.log import Log
from models.scooter import Scooter
from models.traveler import Traveler, Gender
import util
from zipfile import ZipFile

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
    def insert_traveler(first_name: str, last_name: str, birthday: str, gender: str, street_name: str, house_number: str, zip_code: str, city: str, email: str, phone_number: str, driving_license_number: str, registration_date: str):
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Travelers(first_name, last_name, birthday, gender, street_name, house_number, zip_code, city, email, phone_number, driving_license_number, registration_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (first_name, last_name, birthday, gender, street_name, house_number, zip_code, city, email, phone_number, driving_license_number, registration_date)
            )
            conn.commit()

    @staticmethod
    def update_traveler(ID: int, first_name: str, last_name: str, birthday: str, gender: str, street_name: str, house_number: str, zip_code: str, city: str, email: str, phone_number: str, driving_license_number: str):
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Travelers
                SET first_name             = ?,
                    last_name              = ?,
                    birthday               = ?,
                    gender                 = ?,
                    street_name            = ?,
                    house_number           = ?,
                    zip_code               = ?,
                    city                   = ?,
                    email                  = ?,
                    phone_number           = ?,
                    driving_license_number = ?
                WHERE ID = ?
                """,
                (first_name, last_name, birthday, gender, street_name, house_number, zip_code, city, email, phone_number, driving_license_number, ID)
            )
            conn.commit()

    @staticmethod
    def get_all_travelers() -> list[Traveler]:
        all_travelers: list[Traveler] = []
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Travelers
                """
            )
            for result in cursor.fetchall():
                all_travelers.append(Traveler(int(result[0]), Encryptor.decrypt(result[1]), Encryptor.decrypt(result[2]), datetime.strptime(Encryptor.decrypt(result[3]), "%Y-%m-%d"), Gender(int(Encryptor.decrypt(result[4]))), Encryptor.decrypt(result[5]), Encryptor.decrypt(result[6]), Encryptor.decrypt(result[7]), Encryptor.decrypt(result[8]), Encryptor.decrypt(result[9]), Encryptor.decrypt(result[10]), Encryptor.decrypt(result[11]), datetime.strptime(Encryptor.decrypt(result[12]), "%Y-%m-%d")))

        return all_travelers

    @staticmethod
    def get_traveler(ID: int) -> Traveler | None:
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Travelers
                    WHERE ID = ?
                """,
                (ID, )
            )
            result = cursor.fetchone()
            if result:
                return Traveler(int(result[0]), Encryptor.decrypt(result[1]), Encryptor.decrypt(result[2]), datetime.strptime(Encryptor.decrypt(result[3]), "%Y-%m-%d"), Gender(int(Encryptor.decrypt(result[4]))), Encryptor.decrypt(result[5]), Encryptor.decrypt(result[6]), Encryptor.decrypt(result[7]), Encryptor.decrypt(result[8]), Encryptor.decrypt(result[9]), Encryptor.decrypt(result[10]), Encryptor.decrypt(result[11]), datetime.strptime(Encryptor.decrypt(result[12]), "%Y-%m-%d"))
            return None

    @staticmethod
    def delete_traveler(ID: int):
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM Travelers
                    WHERE ID = ?
                """,
                (ID, )
            )
            conn.commit()

    @staticmethod
    def create_scooter_table():
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Scooters (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial_number VARCHAR(17) NOT NULL UNIQUE,
                    brand VARCHAR(255) NOT NULL,
                    model VARCHAR(255) NOT NULL,
                    top_speed INT NOT NULL,
                    battery_capacity INT NOT NULL,
                    state_of_charge INT NOT NULL,
                    target_range_soc VARCHAR(255) NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    out_of_service_status INT NOT NULL,
                    mileage INT NOT NULL,
                    last_maintenance_date DATE NOT NULL
                )
                """
            )

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
    def creat_suspicious_logs_table():
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS SuspiciousLogs (
                    log_ID INT NOT NULL
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
    def get_all_service_engineers() -> list[User]:
        all_service_engineers: list[User] = []
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Users
                """
            )
            for result in cursor.fetchall():
                if Role(result[3]) == Role.SERVICE_ENGINEER:
                    all_service_engineers.append(User(int(result[0]), Encryptor.decrypt(result[1]), Role(result[3]), Encryptor.decrypt(result[4]), Encryptor.decrypt(result[5]), datetime.strptime(Encryptor.decrypt(result[6]), "%Y-%m-%d")))

        return all_service_engineers

    @staticmethod
    def get_all_users_dict() -> dict:
        all_users_dict = {}
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT *
                FROM Users
                """
            )
            for result in cursor.fetchall():
                all_users_dict[f"Name: {Encryptor.decrypt(result[4])} {Encryptor.decrypt(result[5])}, Role: {util.role_to_string(Role(result[3]))}, Username: {Encryptor.decrypt(result[1])}, Registration Date: {Encryptor.decrypt(result[6])}"] = result[0]

        return all_users_dict

    @staticmethod
    def get_all_service_engineers_dict() -> dict:
        all_service_engineers_dict = {}
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
                    all_service_engineers_dict[f"Name: {Encryptor.decrypt(result[4])} {Encryptor.decrypt(result[5])}, Role: {util.role_to_string(Role(result[3]))}, Username: {Encryptor.decrypt(result[1])}, Registration Date: {Encryptor.decrypt(result[6])}"] = result[0]

        return all_service_engineers_dict

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
    def insert_log(datetime: str, username: str, description: str, additional_info: str, suspicious: str):
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Logs(datetime, username, description, additional_info, suspicious)
                    VALUES (?, ?, ?, ?, ?)
                """,
                (datetime, username, description, additional_info, suspicious)
            )
            if Encryptor.decrypt(suspicious) == "1":
                log_ID = cursor.lastrowid
                cursor.execute(
                    """
                    INSERT INTO SuspiciousLogs(log_ID)
                        VALUES (?)
                    """,
                    (str(log_ID), )
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
                all_logs.append(Log(int(result[0]), datetime.strptime(Encryptor.decrypt(result[1]), "%Y-%m-%d %H:%M:%S"), Encryptor.decrypt(result[2]), Encryptor.decrypt(result[3]), Encryptor.decrypt(result[4]), int(Encryptor.decrypt(result[5]))))
        return all_logs

    @staticmethod
    def get_all_unread_suspicious_logs():
        all_logs: list[Log] = []
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT Logs.ID, Logs.datetime, Logs.username, Logs.description, Logs.additional_info, Logs.suspicious
                FROM SuspiciousLogs
                    JOIN Logs ON Logs.ID=SuspiciousLogs.log_ID
                """
            )
            for result in cursor.fetchall():
                all_logs.append(Log(int(result[0]), datetime.strptime(Encryptor.decrypt(result[1]), "%Y-%m-%d %H:%M:%S"), Encryptor.decrypt(result[2]), Encryptor.decrypt(result[3]), Encryptor.decrypt(result[4]), int(Encryptor.decrypt(result[5]))))
        return all_logs

    @staticmethod
    def suspicious_logs_count() -> int:
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT COUNT(*) FROM SuspiciousLogs
                """
            )
            return int(cursor.fetchone()[0])

    @staticmethod
    def clear_suspicious_logs():
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM SuspiciousLogs
                """
            )
            conn.commit()

    @staticmethod
    def get_scooter(ID: int) -> Scooter | None:
        for scooter in Database.get_all_scooters():
            if scooter.ID == ID:
                return scooter
        return None

    @staticmethod
    def get_all_scooters() -> list[Scooter]:
        all_scooters: list[Scooter] = []
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Scooters
                """
            )
            for result in cursor.fetchall():
                all_scooters.append(Scooter(int(result[0]), Encryptor.decrypt(result[1]), Encryptor.decrypt(result[2]), Encryptor.decrypt(result[3]), int(Encryptor.decrypt(result[4])), int(Encryptor.decrypt(result[5])), int(Encryptor.decrypt(result[6])), Encryptor.decrypt(result[7]), Encryptor.decrypt(result[8]), int(result[9]), int(Encryptor.decrypt(result[10])), datetime.strptime(Encryptor.decrypt(result[11]), "%Y-%m-%d")))
        return all_scooters

    @staticmethod
    def get_all_scooters_dict() -> dict:
        all_scooters_dict = {}
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Scooters
                """
            )
            for result in cursor.fetchall():
                all_scooters_dict[f"Scooter: {Encryptor.decrypt(result[2])} {Encryptor.decrypt(result[3])}, Serial number: {Encryptor.decrypt(result[1])}"] = result[0]

        return all_scooters_dict

    @staticmethod
    def get_all_travelers_dict() -> dict:
        all_travelers_dict = {}
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM Travelers
                """
            )
            for result in cursor.fetchall():
                all_travelers_dict[f"ID: {result[0]}, Name: {Encryptor.decrypt(result[1])} {Encryptor.decrypt(result[2])}, Email: {Encryptor.decrypt(result[9])}"] = result[0]

        return all_travelers_dict

    @staticmethod
    def serial_number_exist(serial_number: str | None, allowed_serial_number: str | None) -> bool:
        if serial_number is None:
            return False
        for scooter in Database.get_all_scooters():
            if scooter.serial_number == serial_number:
                if allowed_serial_number is None:
                    return True
                else:
                    return scooter.serial_number != allowed_serial_number
        return False

    @staticmethod
    def insert_scooter(serial_number: str, brand: str, model: str, top_speed: str, battery_capacity: str, state_of_charge: str, target_range_soc: str, location: str, out_of_service_status: str, mileage: str, last_maintenance_date: str):
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Scooters(serial_number, brand, model, top_speed, battery_capacity, state_of_charge, target_range_soc, location, out_of_service_status, mileage, last_maintenance_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (serial_number, brand, model, top_speed, battery_capacity, state_of_charge, target_range_soc, location, out_of_service_status, mileage, last_maintenance_date)
            )
            conn.commit()

    @staticmethod
    def delete_scooter(ID: int):
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                DELETE FROM Scooters
                    WHERE ID = ?
                """,
                (ID, )
            )
            conn.commit()

    @staticmethod
    def update_scooter(ID: int, serial_number: str, brand: str, model: str, top_speed: str, battery_capacity: str, state_of_charge: str, target_range_soc: str, location: str, out_of_service_status: str, mileage: str, last_maintenance_date: str):
        with sqlite3.connect(Database.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE Scooters SET serial_number = ?, brand = ?, model = ?, top_speed = ?, battery_capacity = ?, state_of_charge = ?, target_range_soc = ?, location = ?, out_of_service_status = ?, mileage = ?, last_maintenance_date = ?
                    WHERE ID = ?
                """,
                (serial_number, brand, model, top_speed, battery_capacity, state_of_charge, target_range_soc, location, out_of_service_status, mileage, last_maintenance_date, ID)
            )
            conn.commit()

    
    @staticmethod
    def create_backup():
        if not os.path.exists("data/backups"):
            os.makedirs("data/backups")
        plain_name = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        encrypted_plain_name = Encryptor.encrypt(plain_name)

        if os.path.exists(Database.database_file_name):
            with open(Database.database_file_name, "rb") as source:
                with open(os.path.join("data/backups", encrypted_plain_name + ".db"), "wb") as target:
                    target.write(source.read())
                    with ZipFile(os.path.join("data/backups", encrypted_plain_name + ".zip"), "w") as zip:
                        zip.write(os.path.join("data/backups", encrypted_plain_name + ".db"))
            os.remove(os.path.join("data/backups", encrypted_plain_name + ".db"))
            return encrypted_plain_name + ".zip"
        else:
            return None

    @staticmethod
    def get_all_backups() -> list[tuple[str, str]]:
        if not os.path.exists("data/backups"):
            return []
        backups = []
        for filename in os.listdir("data/backups"):
            if filename.endswith(".zip"):
                enc_name = filename[:-4]
                try:
                    plain_name = Encryptor.decrypt(enc_name)
                    backups.append((plain_name, filename))
                except Exception:
                    pass
        backups.sort(key=lambda x: x[0], reverse=True)
        return backups

    @staticmethod
    def delete_backup(encrypted_filename: str) -> bool:
        backup_path = os.path.join("data/backups", encrypted_filename)
        if os.path.exists(backup_path):
            os.remove(backup_path)
            return True
        return False

    @staticmethod
    def restore_backup(encrypted_filename: str) -> bool:
        backup_path = os.path.join("data/backups", encrypted_filename)
        if not os.path.exists(backup_path):
            return False
        current_backup = Database.create_backup()
        try:
            with ZipFile(backup_path, "r") as zip:
                zip.extractall()
                with open(os.path.join("data/backups", encrypted_filename[:-4] + ".db"), "rb") as source:
                    with open(Database.database_file_name, "wb") as target:
                        target.write(source.read())
            os.remove(os.path.join("data/backups", encrypted_filename[:-4] + ".db"))
            return True
        except Exception:
            if current_backup:
                current_backup_path = os.path.join("data/backups", current_backup)
                if os.path.exists(current_backup_path):
                    with ZipFile(current_backup_path, "r") as zip:
                        zip.extractall()
                        with open(os.path.join("data/backups", current_backup[:-4] + ".db"), "rb") as source:
                            with open(Database.database_file_name, "wb") as target:
                                target.write(source.read())
                os.remove(os.path.join("data/backups", current_backup[:-4] + ".db"))
            return False
