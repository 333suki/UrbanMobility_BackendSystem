from datetime import datetime
from rich import box
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from InquirerPy import inquirer

import scooter_management
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
        console.print("[bold blue]System Admin Page[/bold blue]")
        console.print(f"[bold blue]Welcome {state.current_user.username}![/bold blue]")
        print()

        choice = inquirer.select(
            message = "Please select an option:",
            choices = [
                "List Users",
                "Manage Scooters",
                "Create Service Engineer",
                "Update Service Engineer",
                "Delete Service Engineer",
                "Reset Service Engineer Password",
                "Update My Profile",
                "Delete My Account",
                "View Logs",
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
            state.menu_stack.append(Menu.SYSTEM_ADMIN_LIST_ACCOUNTS)
            list_users_menu()
        elif choice == "Manage Scooters":
            state.last_menu_choice = "Manage Scooters"
            state.menu_stack.append(Menu.SYSTEM_ADMIN_MANAGE_SCOOTERS)
            scooter_management.manage_scooters_menu()
        elif choice == "Create Service Engineer":
            state.last_menu_choice = "Create Service Engineer"
            state.menu_stack.append(Menu.SYSTEM_ADMIN_CREATE_ACCOUNT)
            create_account_menu()
        elif choice == "Update Service Engineer":
            state.last_menu_choice = "Update Service Engineer"
            state.menu_stack.append(Menu.SYSTEM_ADMIN_UPDATE_ACCOUNT)
            update_account_menu()
        elif choice == "View Logs":
            state.last_menu_choice = "View Logs"
            state.menu_stack.append(Menu.SYSTEM_ADMIN_VIEW_LOGS)
            view_logs_menu()
        elif choice == "Delete Service Engineer":
            state.last_menu_choice = "Delete Service Engineer"
            state.menu_stack.append(Menu.SYSTEM_ADMIN_DELETE_ACCOUNT)
            delete_account_menu()
        
def list_users_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SYSTEM_ADMIN_LIST_ACCOUNTS:
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

def create_account_menu():
    console = Console()
    role: Role | None = Role.SERVICE_ENGINEER
    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    while state.menu_stack[-1] == Menu.SYSTEM_ADMIN_CREATE_ACCOUNT:
        console.clear()
        console.print("[bold blue]Create Account[/bold blue]")
        print()

        console.print("[cyan]Role:[/cyan]       ", end="")
        if role is not None:
            console.print(f"[white]{util.role_to_string(role)}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

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
                "Edit Credentials",
                "Create",
                "Back"
            ],
            default="Edit Credentials",
        ).execute()
        if choice == "Back":
            state.menu_stack.pop()
            return
        elif choice == "Edit Credentials":
            new_username: str = Prompt.ask(
                f"[cyan]Username[/cyan] [bright_black](Empty to keep {util.parse_string(username)})[/bright_black]",
                console=console)
            if new_username:
                username = new_username
            new_password: str = Prompt.ask(
                f"[cyan]Password[/cyan] [bright_black](Empty to keep {util.parse_string(password)})[/bright_black]",
                console=console)
            if new_password:
                password = new_password
            new_first_name: str = Prompt.ask(
                f"[cyan]First name[/cyan] [bright_black](Empty to keep {util.parse_string(first_name)})[/bright_black]",
                console=console)
            if new_first_name:
                first_name = new_first_name
            new_last_name: str = Prompt.ask(
                f"[cyan]Last name[/cyan] [bright_black](Empty to keep {util.parse_string(last_name)})[/bright_black]",
                console=console)
            if new_last_name:
                last_name = new_last_name
        elif choice == "Create":
            is_valid: bool = True
            if Database.username_exist(username, None):
                console.print(f"[bold red]Invalid username:[/bold red]   [white]{util.parse_string(username)}[/white] [bright_black]Username already exists[/bright_black]")
                is_valid = False
            if not util.is_valid_username(username):
                console.print(f"[bold red]Invalid username:[/bold red]   [white]{util.parse_string(username)}[/white]")
                is_valid = False
            if not util.is_valid_password(password):
                console.print(f"[bold red]Invalid password:[/bold red]   [white]{util.parse_string(password)}[/white]")
                is_valid = False
            if not util.is_valid_first_name(first_name):
                console.print(
                    f"[bold red]Invalid first name:[/bold red] [white]{util.parse_string(first_name)}[/white]")
                is_valid = False
            if not util.is_valid_last_name(last_name):
                console.print(f"[bold red]Invalid last name:[/bold red]  [white]{util.parse_string(last_name)}[/white]")
                is_valid = False

            if not is_valid:
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
            else:
                Database.insert_user(Encryptor.encrypt(username), str(abs(hash(password))), role, Encryptor.encrypt(first_name), Encryptor.encrypt(last_name), Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d")))
                console.print(f"[bold green]{util.role_to_string(role)} Created[/bold green]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
                state.menu_stack.pop()
                return

def update_account_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SYSTEM_ADMIN_UPDATE_ACCOUNT:
        console.clear()
        console.print("[bold blue]Update Account[/bold blue]")
        print()
        all_engineers_dict = Database.get_all_service_engineers_dict()
        all_engineers_strings = list(all_engineers_dict.keys())
        all_engineers_strings.append("Back")
        choice = inquirer.select(
            message="Select Account to update:",
            choices=all_engineers_strings,
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return

        id_to_edit = all_engineers_dict[choice]
        user: User = Database.get_user(id_to_edit)

        role: Role | None = user.role
        username: str | None = user.username
        password: str | None = None
        first_name: str | None = user.first_name
        last_name: str | None = user.last_name

        while True:
            console.clear()
            console.print("[bold blue]Update Account[/bold blue]")
            print()

            console.print("[cyan]Role:[/cyan]       ", end="")
            if role is not None:
                console.print(f"[white]{util.role_to_string(role)}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Username:[/cyan]   ", end="")
            if username is not None:
                console.print(f"[white]{username}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Password:[/cyan]   ", end="")
            if password is not None:
                console.print(f"[white]{password}[/white]")
            else:
                console.print("[bright_black]Hidden[/bright_black]")

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
                    "Edit Credentials",
                    "Update",
                    "Back"
                ],
                default="Edit Credentials",
            ).execute()

            if choice == "Back":
                break
            elif choice == "Edit Credentials":
                new_role = inquirer.select(
                    message="Role",
                    choices=[
                        "System Administrator",
                        "Service Engineer"
                    ],
                    default=util.role_to_string(role) if role else "System Administrator",
                ).execute()
                role = util.string_to_role(new_role)
                new_username: str = Prompt.ask(f"[cyan]Username[/cyan] [bright_black](Empty to keep {util.parse_string(username)})[/bright_black]", console=console)
                if new_username:
                    username = new_username
                if password:
                    new_password: str = Prompt.ask(f"[cyan]Password[/cyan] [bright_black](Empty to keep {util.parse_string(password)})[/bright_black]", console=console)
                else:
                    new_password: str = Prompt.ask(f"[cyan]Password[/cyan] [bright_black](Empty to keep the same)", console=console)
                if new_password:
                    password = new_password
                new_first_name: str = Prompt.ask(f"[cyan]First name[/cyan] [bright_black](Empty to keep {util.parse_string(first_name)})[/bright_black]", console=console)
                if new_first_name:
                    first_name = new_first_name
                new_last_name: str = Prompt.ask(f"[cyan]Last name[/cyan] [bright_black](Empty to keep {util.parse_string(last_name)})[/bright_black]", console=console)
                if new_last_name:
                    last_name = new_last_name
            elif choice == "Update":
                is_valid: bool = True
                if Database.username_exist(username, user.username):
                    console.print(f"[bold red]Invalid username:[/bold red]   [white]{util.parse_string(username)}[/white] [bright_black]Username already exists[/bright_black]")
                    is_valid = False
                if not util.is_valid_username(username):
                    console.print(f"[bold red]Invalid username:[/bold red]   [white]{util.parse_string(username)}[/white]")
                    is_valid = False
                if password is not None and not util.is_valid_password(password):
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
                    if password:
                        Database.update_user_with_password(user.ID, Encryptor.encrypt(username), str(abs(hash(password))), role, Encryptor.encrypt(first_name), Encryptor.encrypt(last_name))
                    else:
                        Database.update_user(user.ID, Encryptor.encrypt(username), role, Encryptor.encrypt(first_name), Encryptor.encrypt(last_name))
                    console.print(f"[bold green]User Updated[/bold green]")
                    console.print("[bright_black]Press enter to continue[/bright_black]")
                    input()
                    state.menu_stack.pop()
                    return

def delete_account_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SYSTEM_ADMIN_DELETE_ACCOUNT:
        console.clear()
        console.print("[bold blue]Delete Account[/bold blue]")
        print()
        all_engineers_dict = Database.get_all_service_engineers_dict()
        all_engineers_strings = list(all_engineers_dict.keys())
        all_engineers_strings.append("Back")
        choice = inquirer.select(
            message="Select Account to delete:",
            choices=all_engineers_strings,
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return

        confirm_choice = inquirer.select(
            message="Do you really want to delete this User",
            choices=[
                "Yes",
                "No"
            ],
            default="Yes"
        ).execute()

        if confirm_choice == "Yes":
            Database.delete_user(all_engineers_dict[choice])
            console.print("[bold green]User Deleted[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
        else:
            console.print("[bold green]Deletion Canceled[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
        input()
        state.menu_stack.pop()
        return

def view_logs_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SYSTEM_ADMIN_VIEW_LOGS:
        console.clear()

        table = Table(title="Logs", box=box.ASCII)
        table.add_column("ID")
        table.add_column("Date")
        table.add_column("Time")
        table.add_column("Username")
        table.add_column("Description")
        table.add_column("Additional Information")
        table.add_column("Suspicious")

        for log in Database.get_all_logs():
            table.add_row(str(log.ID), log.datetime.strftime("%Y-%m-%d"), log.datetime.strftime("%H:%M:%S"), log.username, log.description, log.additional_info, "Yes" if log.suspicious else "No")
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
