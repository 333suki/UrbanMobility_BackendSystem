from rich.console import Console
from InquirerPy import inquirer
from datetime import datetime

from database import Database
from models.user import Role
from models.user import User
from encryptor import Encryptor
import super_admin_menu
import system_admin_menu
import state
from state import Menu

# TODO: Change back
SUPER_ADMIN_USERNAME: str = "a"
SUPER_ADMIN_PASSWORD: str = "a"
SUSPICIOUS_LOGIN_COUNT = 2

def login_screen():
    login_count: int = 0
    state.last_menu_choice = "List Users"
    console = Console()

    while state.menu_stack[-1] == Menu.LOGIN:
        console.clear()
        console.print("[bold blue]==============================[/bold blue]")
        console.print("[bold blue]        Welcome to UMBS        [/bold blue]")
        console.print("[bold blue]==============================[/bold blue]\n")

        choice = inquirer.select(
            message = "Please select an option:",
            choices = [
                "Login",
                "Quit"
            ],
            default = "Login",
        ).execute()

        if choice == "Quit":
            console.print("[bold cyan]Goodbye![/bold cyan]")
            state.menu_stack.pop()
            break
        elif choice == "Login":
            username = inquirer.text(message="Username:").execute()
            password = inquirer.secret(message="Password:").execute()
            login_count += 1
            if username == SUPER_ADMIN_USERNAME and password == SUPER_ADMIN_PASSWORD:
                if login_count > SUSPICIOUS_LOGIN_COUNT:
                    Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), Encryptor.encrypt(username), Encryptor.encrypt("Super Administrator Login"), Encryptor.encrypt(f"Login after multiple wrong attempts"), Encryptor.encrypt("1"))
                else:
                    Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), Encryptor.encrypt(username), Encryptor.encrypt("Super Administrator Login"), Encryptor.encrypt(""), Encryptor.encrypt("0"))
                state.current_user = User(0, SUPER_ADMIN_USERNAME, Role.SUPER_ADMIN, None, None, None)
                state.menu_stack.append(Menu.SUPER_ADMIN_MAIN)
                super_admin_menu.main_menu()
                login_count = 0
            elif Database.validate(username, password):
                state.current_user = Database.get_user_by_username(username)
                if state.current_user.role == Role.SERVICE_ENGINEER:
                    if login_count > SUSPICIOUS_LOGIN_COUNT:
                        Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),Encryptor.encrypt(username), Encryptor.encrypt("Service Engineer Login"), Encryptor.encrypt(f"Login after multiple wrong attempts"), Encryptor.encrypt("1"))
                    else:
                        Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), Encryptor.encrypt(username), Encryptor.encrypt("Service Engineer Login"), Encryptor.encrypt(f""), Encryptor.encrypt("0"))
                    console.print("[bold green]Service Engineer login success[/bold green]")
                    console.print("[bright_black]Press enter to continue[/bright_black]")
                    input()
                    state.menu_stack.append(Menu.SERVICE_ENGINEER_MAIN)
                    from scooter_management import service_engineer_main_menu
                    service_engineer_main_menu()
                    login_count = 0
                elif state.current_user.role == Role.SYSTEM_ADMIN:
                    if login_count > SUSPICIOUS_LOGIN_COUNT:
                        Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), Encryptor.encrypt(username), Encryptor.encrypt("System Administrator Login"), Encryptor.encrypt(f"Login after multiple wrong attempts"), Encryptor.encrypt("1"))
                    else:
                        Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), Encryptor.encrypt(username), Encryptor.encrypt("System Administrator Login"), Encryptor.encrypt(f""), Encryptor.encrypt("0"))
                    state.menu_stack.append(Menu.SYSTEM_ADMIN_MAIN)
                    system_admin_menu.main_menu()
                    login_count = 0
            else:
                if login_count > SUSPICIOUS_LOGIN_COUNT:
                    Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), Encryptor.encrypt(username), Encryptor.encrypt("Unsuccessful login"), Encryptor.encrypt(""), Encryptor.encrypt("1"))
                else:
                    Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), Encryptor.encrypt(username), Encryptor.encrypt("Unsuccessful Login"), Encryptor.encrypt(""), Encryptor.encrypt("0"))
                console.print("[bold red]Login failed! Please try again.[/bold red]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
