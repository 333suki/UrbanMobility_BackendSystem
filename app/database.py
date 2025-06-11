import sqlite3
import os

class Database:
    def __init__(self, database_file_name: str):
        os.makedirs(os.path.dirname(database_file_name), exist_ok=True)
        self.database_file_name = database_file_name
        self.create_users_table()
        self.create_travelers_table()
        self.create_scooter_table()

    def create_users_table(self):
        with sqlite3.connect(self.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Users (
                    ID INT NOT NULL UNIQUE,
                    user_name VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role INT NOT NULL,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    registration_date DATE NOT NULL,
                    PRIMARY KEY (ID)
                )
                """
            )

    def create_travelers_table(self):
        with sqlite3.connect(self.database_file_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS Travelers (
                    ID INT NOT NULL UNIQUE,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    birthday DATE NOT NULL,
                    gender INT NOT NULL,
                    street_name VARCHAR(255) NOT NULL,
                    house_number VARCHAR(255) NOT NULL,
                    zip_code CHAR(6) NOT NULL,
                    city VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    mobile_nr CHAR(15) NOT NULL,
                    driving_license_nr VARCHAR(9) NOT NULL,
                    registration_date DATE NOT NULL,
                    PRIMARY KEY (ID)
                )
            """
            )

    def create_scooter_table(self):
        with sqlite3.connect(self.database_file_name) as conn:
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