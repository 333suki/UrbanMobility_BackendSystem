from datetime import datetime
from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from InquirerPy import inquirer

import scooter_management
import account_management
import backup_management
from database import Database
from encryptor import Encryptor
import state
from state import Menu

def main_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_MAIN:
        console.clear()
        console.print("[bold blue]Super Admin Page[/bold blue]")
        print()

        notification_string = f"Notifications ({Database.suspicious_logs_count()})"
        choice = inquirer.select(
            message = "Please select an option:",
            choices = [
                "Manage Accounts",
                "Manage Scooters",
                "Manage Backups",
                "View Logs",
                notification_string,
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
            console.clear()
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
        elif choice == "Manage Backups":
            state.last_menu_choice = "Manage Backups"
            state.menu_stack.append(Menu.SUPER_ADMIN_MANAGE_BACKUPS)
            backup_management.manage_backups_menu()
        elif choice == "View Logs":
            state.last_menu_choice = "View Logs"
            state.menu_stack.append(Menu.SUPER_ADMIN_VIEW_LOGS)
            view_logs_menu()
        elif choice == notification_string:
            state.last_menu_choice = notification_string
            state.menu_stack.append(Menu.SUPER_ADMIN_VIEW_SUSPICIOUS_LOGS)
            view_suspicious_logs_menu()


def view_logs_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_VIEW_LOGS:
        console.clear()

        table = Table(title="Logs", box=box.ASCII)
        table.add_column("[blue]Date[/blue]")
        table.add_column("[blue]Time[/blue]")
        table.add_column("[blue]Username[/blue]")
        table.add_column("[blue]Description[/blue]")
        table.add_column("[blue]Additional Information[/blue]")
        table.add_column("[blue]Suspicious[/blue]")

        for log in Database.get_all_logs():
            table.add_row(log.datetime.strftime("%Y-%m-%d"), log.datetime.strftime("%H:%M:%S"), log.username, log.description, log.additional_info, "[red]Yes[/red]" if log.suspicious else "[green]No[/green]")
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

def view_suspicious_logs_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_VIEW_SUSPICIOUS_LOGS:
        console.clear()

        table = Table(title="Notifications", box=box.ASCII)
        table.add_column("[blue]Date[/blue]")
        table.add_column("[blue]Time[/blue]")
        table.add_column("[blue]Username[/blue]")
        table.add_column("[blue]Description[/blue]")
        table.add_column("[blue]Additional Information[/blue]")
        table.add_column("[blue]Suspicious[/blue]")

        for log in Database.get_all_unread_suspicious_logs():
            table.add_row(log.datetime.strftime("%Y-%m-%d"), log.datetime.strftime("%H:%M:%S"), log.username, log.description, log.additional_info, "[red]Yes[/red]" if log.suspicious else "[green]No[/green]")
        console.print(table)
        print()

        choice = inquirer.select(
            message="Please select an option:",
            choices=[
                "Clear Notifications",
                "Back"
            ],
            default="Back",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return

        confirm_choice = inquirer.select(
            message="Do you really want to clear all notifications",
            choices=[
                "Yes",
                "No"
            ],
            default="Yes"
        ).execute()

        if confirm_choice == "Yes":
            Database.clear_suspicious_logs()
            console.print("[bold green]Notification Cleared[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
        else:
            console.print("[bold green]Deletion Canceled[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
        input()
        state.menu_stack.pop()
        return
