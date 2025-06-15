from rich.console import Console
from InquirerPy import inquirer

from database import Database
from models.user import Role
from models.user import User
import super_admin_menu
import system_admin_menu
import state
from state import Menu

# TODO: Change back
SUPER_ADMIN_USERNAME: str = "a"
SUPER_ADMIN_PASSWORD: str = "a"

def login_screen():
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
            if username == SUPER_ADMIN_USERNAME and password == SUPER_ADMIN_PASSWORD:
                state.current_user = User(0, SUPER_ADMIN_USERNAME, Role.SUPER_ADMIN, None, None, None)
                state.menu_stack.append(Menu.SUPER_ADMIN_MAIN)
                super_admin_menu.super_admin_main_menu()
            elif Database.validate(username, password):
                state.current_user = Database.get_user_by_username(username)
                if state.current_user.role == Role.SERVICE_ENGINEER:
                    console.print("[bold green]Service Engineer login success[/bold green]")
                    console.print("[bright_black]Press enter to continue[/bright_black]")
                    input()
                    # state.menu_stack.append(Menu.SERVICE_ENGINEER_MAIN)
                    # service_engineer_menu.main_menu()
                elif state.current_user.role == Role.SYSTEM_ADMIN:
                    state.menu_stack.append(Menu.SYSTEM_ADMIN_MAIN)
                    system_admin_menu.system_admin_main_menu()
            else:
                console.print("[bold red]Login failed! Please try again.[/bold red]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
