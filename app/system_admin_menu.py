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


