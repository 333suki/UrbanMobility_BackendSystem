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
from models.user import Role
import util


def main_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_MAIN:
        console.clear()
        console.print("[bold blue]==============================[/bold blue]")
        console.print("[bold blue]       Super Admin Page       [/bold blue]")
        console.print("[bold blue]==============================[/bold blue]\n")

        choice = inquirer.select(
            message = "Please select an option:",
            choices = [
                "List Users",
                "Create System Administrator",
                "Delete System Administrator",
                "Create Service Engineer",
                "Delete Service Engineer",
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
            state.menu_stack.append(Menu.SUPER_ADMIN_LIST_USERS)
            list_users_menu()
        elif choice == "Create System Administrator":
            state.last_menu_choice = "Create System Administrator"
            state.menu_stack.append(Menu.SUPER_ADMIN_CREATE_SYSTEM_ADMIN)
            create_system_admin_menu()
        elif choice == "Delete System Administrator":
            state.last_menu_choice = "Delete System Administrator"
            state.menu_stack.append(Menu.SUPER_ADMIN_DELETE_SYSTEM_ADMIN)
            delete_system_admin_menu()
        elif choice == "Create Service Engineer":
            state.last_menu_choice = "Create Service Engineer"
            state.menu_stack.append(Menu.SUPER_ADMIN_CREATE_SERVICE_ENGINEER)
            create_service_engineer_menu()
        elif choice == "Delete Service Engineer":
            state.last_menu_choice = "Delete Service Engineer"
            state.menu_stack.append(Menu.SUPER_ADMIN_DELETE_SERVICE_ENGINEER)
            delete_service_engineer_menu()


def create_system_admin_menu():
    console = Console()
    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_CREATE_SYSTEM_ADMIN:
        console.clear()
        console.print("[bold blue]Create System Administrator[/bold blue]")
        print()

        console.print("[cyan]Username:[/cyan]   ", end="")
        if username is not None:
            console.print(f"[white]{username}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Password:[/cyan]   ", end="")
        if password is not None:
            console.print(f"[white]{password}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]First name:[/cyan] ", end="")
        if first_name is not None:
            console.print(f"[white]{first_name}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Last name:[/cyan]  ", end="")
        if last_name is not None:
            console.print(f"[white]{last_name}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        print()
        choice = inquirer.select(
            message = "Please select an option:",
            choices = [
                "Edit credentials",
                "Create",
                "Back"
            ],
            default = "Edit credentials",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return
        elif choice == "Edit credentials":
            new_username: str = Prompt.ask(f"[cyan]Username[/cyan] [bright_black](Empty to keep {util.parse_string(username)})[/bright_black]", console=console)
            if new_username:
                username = new_username
            new_password: str = Prompt.ask(f"[cyan]Password[/cyan] [bright_black](Empty to keep {util.parse_string(password)})[/bright_black]", console=console)
            if new_password:
                password = new_password
            new_first_name: str = Prompt.ask(f"[cyan]First name[/cyan] [bright_black](Empty to keep {util.parse_string(first_name)})[/bright_black]", console=console)
            if new_first_name:
                first_name = new_first_name
            new_last_name: str = Prompt.ask(f"[cyan]Last name[/cyan] [bright_black](Empty to keep {util.parse_string(last_name)})[/bright_black]", console=console)
            if new_last_name:
                last_name = new_last_name
        elif choice == "Create":
            is_valid: bool = True
            if not util.is_valid_username(username):
                console.print(f"[bold red]Invalid username:[/bold red]   [white]{util.parse_string(username)}[/white]")
                is_valid = False
            if not util.is_valid_password(password):
                console.print(f"[bold red]Invalid password:[/bold red]   [white]{util.parse_string(password)}[/white]")
                is_valid = False
            if not util.is_valid_first_name(first_name):
                console.print(f"[bold red]Invalid first name:[/bold red] [white]{util.parse_string(first_name)}[/white]")
                is_valid = False
            if not util.is_valid_last_name(last_name):
                console.print(f"[bold red]Invalid last name:[/bold red]  [white]{util.parse_string(last_name)}[/white]")
                is_valid = False

            if not is_valid:
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
            else:
                with Database("data/database.db") as db:
                    db.insert_user(Encryptor.encrypt(username), str(abs(hash(password))), Role.SYSTEM_ADMIN, Encryptor.encrypt(first_name), Encryptor.encrypt(last_name), Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d")))
                console.print("[bold green]System Administrator Created[/bold green]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
                state.menu_stack.pop()
                return


def delete_system_admin_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_DELETE_SYSTEM_ADMIN:
        console.clear()
        console.print("[bold blue]Delete System Administrator[/bold blue]")
        print()
        with Database("data/database.db") as db:
            all_system_admins_dict = db.get_all_system_admins_dict()
            all_system_admins_strings = list(all_system_admins_dict.keys())
            all_system_admins_strings.append("Back")
            choice = inquirer.select(
                message = "Select User to delete:",
                choices = all_system_admins_strings,
            ).execute()

            if choice == "Back":
                state.menu_stack.pop()
                return

            confirm_choice = inquirer.select(
                message = "Do you really want to delete this System Administrator",
                choices = [
                    "Yes",
                    "No"
                ],
                default = "Yes"
            ).execute()

            if confirm_choice == "Yes":
                db.delete_user(all_system_admins_dict[choice])
                console.print("[bold green]System Administrator Deleted[/bold green]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
            else:
                console.print("[bold green]Deletion Canceled[/bold green]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
            input()
            state.menu_stack.pop()
            return


def create_service_engineer_menu():
    console = Console()
    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_CREATE_SERVICE_ENGINEER:
        console.clear()
        console.print("[bold blue]Create Service Engineer[/bold blue]")
        print()

        console.print("[cyan]Username:[/cyan]   ", end="")
        if username is not None:
            console.print(f"[white]{username}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Password:[/cyan]   ", end="")
        if password is not None:
            console.print(f"[white]{password}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]First name:[/cyan] ", end="")
        if first_name is not None:
            console.print(f"[white]{first_name}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Last name:[/cyan]  ", end="")
        if last_name is not None:
            console.print(f"[white]{last_name}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        print()
        choice = inquirer.select(
            message="Please select an option:",
            choices=[
                "Edit credentials",
                "Create",
                "Back"
            ],
            default="Edit credentials",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return
        elif choice == "Edit credentials":
            new_username: str = Prompt.ask(f"[cyan]Username[/cyan] [bright_black](Empty to keep {util.parse_string(username)})[/bright_black]", console=console)
            if new_username:
                username = new_username
            new_password: str = Prompt.ask(f"[cyan]Password[/cyan] [bright_black](Empty to keep {util.parse_string(password)})[/bright_black]", console=console)
            if new_password:
                password = new_password
            new_first_name: str = Prompt.ask(f"[cyan]First name[/cyan] [bright_black](Empty to keep {util.parse_string(first_name)})[/bright_black]", console=console)
            if new_first_name:
                first_name = new_first_name
            new_last_name: str = Prompt.ask(f"[cyan]Last name[/cyan] [bright_black](Empty to keep {util.parse_string(last_name)})[/bright_black]", console=console)
            if new_last_name:
                last_name = new_last_name
        elif choice == "Create":
            is_valid: bool = True
            if not util.is_valid_username(username):
                console.print(f"[bold red]Invalid username:[/bold red]   [white]{util.parse_string(username)}[/white]")
                is_valid = False
            if not util.is_valid_password(password):
                console.print(f"[bold red]Invalid password:[/bold red]   [white]{util.parse_string(password)}[/white]")
                is_valid = False
            if not util.is_valid_first_name(first_name):
                console.print(f"[bold red]Invalid first name:[/bold red] [white]{util.parse_string(first_name)}[/white]")
                is_valid = False
            if not util.is_valid_last_name(last_name):
                console.print(f"[bold red]Invalid last name:[/bold red]  [white]{util.parse_string(last_name)}[/white]")
                is_valid = False

            if not is_valid:
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
            else:
                with Database("data/database.db") as db:
                    db.insert_user(Encryptor.encrypt(username), str(abs(hash(password))), Role.SERVICE_ENGINEER, Encryptor.encrypt(first_name), Encryptor.encrypt(last_name), Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d")))
                console.print("[bold green]Service Engineer Created[/bold green]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
                state.menu_stack.pop()
                return


def delete_service_engineer_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_DELETE_SERVICE_ENGINEER:
        console.clear()
        console.print("[bold blue]Delete Service Engineer[/bold blue]")
        print()

        with Database("data/database.db") as db:
            all_service_engineers_dict = db.get_all_service_engineers_dict()
            all_service_engineers_strings = list(all_service_engineers_dict.keys())
            all_service_engineers_strings.append("Back")
            choice = inquirer.select(
                message = "Select User to delete:",
                choices = all_service_engineers_strings,
            ).execute()

            if choice == "Back":
                state.menu_stack.pop()
                return

            confirm_choice = inquirer.select(
                message = "Do you really want to delete this Service Engineer",
                choices = [
                    "Yes",
                    "No"
                ],
                default = "Yes"
            ).execute()

            if confirm_choice == "Yes":
                db.delete_user(all_service_engineers_dict[choice])
                console.print("[bold green]Service Engineer Deleted[/bold green]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
            else:
                console.print("[bold green]Deletion Canceled[/bold green]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
            input()
            state.menu_stack.pop()
            return


def list_users_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_LIST_USERS:
        console.clear()

        table = Table(title="Users", box=box.ASCII)
        table.add_column("ID")
        table.add_column("Username")
        table.add_column("Role")
        table.add_column("First Name")
        table.add_column("Last Name")
        table.add_column("Registration Date")
        with Database("data/database.db") as db:
            for user in db.get_all_users():
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
