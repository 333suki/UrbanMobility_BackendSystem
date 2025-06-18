from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from InquirerPy import inquirer
from datetime import datetime

import state
from models.user import Role, User
from encryptor import Encryptor
from state import Menu
from database import Database
import util

def manage_accounts_menu():
    console = Console()
    while state.menu_stack[-1] == Menu.SUPER_ADMIN_MANAGE_ACCOUNTS or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_MANAGE_ACCOUNTS:
        console.clear()
        choice = inquirer.select(
            message="Account Management:",
            choices=[
                "List Accounts",
                "Create Account",
                "Update Account",
                "Delete Account",
                "Back"
            ],
            default="List Accounts",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return
        elif choice == "List Accounts":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_LIST_ACCOUNTS)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_LIST_ACCOUNTS)
            list_accounts_menu()
        elif choice == "Create Account":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_CREATE_ACCOUNT)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_CREATE_ACCOUNT)
            create_account_menu()
        elif choice == "Update Account":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_UPDATE_ACCOUNT)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_UPDATE_ACCOUNT)
            update_account_menu()
        elif choice == "Delete Account":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_DELETE_ACCOUNT)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_DELETE_ACCOUNT)
            delete_account_menu()


def list_accounts_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_LIST_ACCOUNTS or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_LIST_ACCOUNTS:
        console.clear()

        table = Table(title="Users", box=box.ASCII)
        table.add_column("ID")
        table.add_column("Username")
        table.add_column("Role")
        table.add_column("First Name")
        table.add_column("Last Name")
        table.add_column("Registration Date")

        # if state.current_user.role == Role.SUPER_ADMIN:
        #     all_users = Database.get_all_users()
        # else:
        #     all_users = Database.get_all_service_engineers()
        all_users = Database.get_all_users()
        for user in all_users:
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
    role: Role | None = None
    username: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_CREATE_ACCOUNT or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_CREATE_ACCOUNT:
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
            if state.current_user.role == Role.SUPER_ADMIN:
                choices = ["System Administrator", "Service Engineer"]
            else:
                choices = ["Service Engineer"]

            new_role = inquirer.select(
                message="Role",
                choices=choices,
                default=util.role_to_string(role) if role else choices[0],
            ).execute()
            role = util.string_to_role(new_role)
            new_username: str = Prompt.ask(f"[cyan]Username[/cyan] [bright_black](Empty to keep {util.parse_string(username)})[/bright_black]", console=console).lower()
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
                Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                    Encryptor.encrypt(state.current_user.username),
                                    Encryptor.encrypt("Account created"), Encryptor.encrypt(f"Account with username \"{username.lower()}\" created"),
                                    Encryptor.encrypt("0"))
                Database.insert_user(Encryptor.encrypt(username.lower()), Encryptor.get_hash(password), role, Encryptor.encrypt(first_name), Encryptor.encrypt(last_name), Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d")))
                console.print(f"[bold green]{util.role_to_string(role)} Created[/bold green]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
                state.menu_stack.pop()
                return


def update_account_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_UPDATE_ACCOUNT or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_UPDATE_ACCOUNT:
        console.clear()
        console.print("[bold blue]Update Account[/bold blue]")
        print()

        if state.current_user.role == Role.SUPER_ADMIN:
            all_users_dict = Database.get_all_users_dict()
        else:
            all_users_dict = Database.get_all_service_engineers_dict()
        all_users_strings = list(all_users_dict.keys())
        all_users_strings.append("Back")
        choice = inquirer.select(
            message="Select Account to update:",
            choices=all_users_strings,
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return

        id_to_edit = all_users_dict[choice]
        user: User = Database.get_user(id_to_edit)
        old_username: str = user.username

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
                if state.current_user.role == Role.SUPER_ADMIN:
                    choices = ["System Administrator", "Service Engineer"]
                else:
                    choices = ["Service Engineer"]

                new_role = inquirer.select(
                    message="Role",
                    choices=choices,
                    default=util.role_to_string(role) if role else choices[0],
                ).execute()
                role = util.string_to_role(new_role)
                new_username: str = Prompt.ask(f"[cyan]Username[/cyan] [bright_black](Empty to keep {util.parse_string(username)})[/bright_black]", console=console).lower()
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
                    Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                        Encryptor.encrypt(state.current_user.username),
                                        Encryptor.encrypt("Account updated"),
                                        Encryptor.encrypt(f"Account with username \"{username.lower()}\" updated, (old username: \"{old_username}\")"),
                                        Encryptor.encrypt("0"))
                    if password:
                        Database.update_user_with_password(user.ID, Encryptor.encrypt(username.lower()), Encryptor.get_hash(password), role, Encryptor.encrypt(first_name), Encryptor.encrypt(last_name))
                    else:
                        Database.update_user(user.ID, Encryptor.encrypt(username.lower()), role, Encryptor.encrypt(first_name), Encryptor.encrypt(last_name))
                    console.print(f"[bold green]Account Updated[/bold green]")
                    console.print("[bright_black]Press enter to continue[/bright_black]")
                    input()
                    state.menu_stack.pop()
                    return


def delete_account_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_DELETE_ACCOUNT or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_DELETE_ACCOUNT:
        console.clear()
        console.print("[bold blue]Delete Account[/bold blue]")
        print()

        if state.current_user.role == Role.SUPER_ADMIN:
            all_users_dict = Database.get_all_users_dict()
        else:
            all_users_dict = Database.get_all_service_engineers_dict()
        all_users_strings = list(all_users_dict.keys())
        all_users_strings.append("Back")
        choice = inquirer.select(
            message="Select Account to delete:",
            choices=all_users_strings,
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
            user: User = Database.get_user(int(all_users_dict[choice]))
            Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                Encryptor.encrypt(state.current_user.username),
                                Encryptor.encrypt("Account deleted"),
                                Encryptor.encrypt(f"Account with username \"{user.username}\" deleted"),
                                Encryptor.encrypt("0"))
            Database.delete_user(all_users_dict[choice])
            console.print("[bold green]Account Deleted[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
        else:
            console.print("[bold green]Deletion Canceled[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
        input()
        state.menu_stack.pop()
        return
