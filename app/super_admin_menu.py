from datetime import datetime
from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from InquirerPy import inquirer

import scooter_management
import account_management
from database import Database
from encryptor import Encryptor
import state
from state import Menu
from models.user import Role, User
import util


def main_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_MAIN:
        console.clear()
        console.print("[bold blue]Super Admin Page[/bold blue]")
        print()

        choice = inquirer.select(
            message = "Please select an option:",
            choices = [
                "Manage Accounts",
                "Manage Scooters",
                "View Logs",
                "Logout"
            ],
            default = state.last_menu_choice,
        ).execute()

        if choice == "Logout":
            Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                Encryptor.encrypt(state.current_user.username),
                                Encryptor.encrypt("Super Administrator Logout"), Encryptor.encrypt(f""),
                                Encryptor.encrypt("0"))
            state.current_user = None
            console.print("[bold cyan]Logged out[/bold cyan]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
            input()
            state.menu_stack.pop()
            return
        elif choice == "Manage Accounts":
            state.last_menu_choice = "Manage Accounts"
            state.menu_stack.append(Menu.SUPER_ADMIN_MANAGE_ACCOUNTS)
            account_management.manage_accounts_menu()
        elif choice == "Manage Scooters":
            state.last_menu_choice = "Manage Scooters"
            state.menu_stack.append(Menu.SUPER_ADMIN_MANAGE_SCOOTERS)
            scooter_management.manage_scooters_menu()
        elif choice == "View Logs":
            state.last_menu_choice = "View Logs"
            state.menu_stack.append(Menu.SUPER_ADMIN_VIEW_LOGS)
            view_logs_menu()


def view_logs_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_VIEW_LOGS:
        console.clear()

        table = Table(title="Logs", box=box.ASCII)
        table.add_column("Date")
        table.add_column("Time")
        table.add_column("Username")
        table.add_column("Description")
        table.add_column("Additional Information")
        table.add_column("Suspicious")

        for log in Database.get_all_logs():
            table.add_row(log.datetime.strftime("%Y-%m-%d"), log.datetime.strftime("%H:%M:%S"), log.username, log.description, log.additional_info, "Yes" if log.suspicious else "No")
        console.print(table)
        print()

        choice = inquirer.select(
            message="Please select an option:",
            choices=[
                "Back"
            ],
            default="Back",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return
