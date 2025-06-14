from datetime import datetime
from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from InquirerPy import inquirer

from database import Database
from encryptor import Encryptor
import state
from state import Menu
from models.user import Role, User
import util

def main_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SYSTEM_ADMIN_MAIN:
        console.clear()
        console.print("[bold blue]==============================[/bold blue]")
        console.print("[bold blue]       System Admin Page       [/bold blue]")
        console.print("[bold blue]==============================[/bold blue]\n")

        choice = inquirer.select(
            message = "Please select an option:",
            choices = [
                "List Users",
                "Create Service Engineer",
                "Update Service Engineer",
                "Delete Service Engineer",
                "Reset Service Engineer Password",
                "Update My Profile",
                "Delete My Account",
                "Logout"
            ],
            default = state.last_menu_choice,
        ).execute()

        if choice == "Logout":
            state.current_user = None
            console.print("[bold cyan]Logged out[/bold cyan]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
            input()
            state.menu_stack.pop()
            return
        elif choice == "List Users":
            state.last_menu_choice = "List Users"
            state.menu_stack.append(Menu.SYSTEM_ADMIN_LIST_USERS)
            list_users_menu()
            return
        
def list_users_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SYSTEM_ADMIN_LIST_USERS:
        console.clear()

        table = Table(title="Users", box=box.ASCII)
        table.add_column("ID")
        table.add_column("Username")
        table.add_column("Role")
        table.add_column("First Name")
        table.add_column("Last Name")
        table.add_column("Registration Date")
        for user in Database.get_all_users():
            table.add_row(str(user.ID), user.username, util.role_to_string(user.role), user.first_name, user.last_name, user.registration_date.strftime("%Y-%m-%d"))
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
