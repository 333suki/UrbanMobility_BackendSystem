from rich.console import Console
from InquirerPy import inquirer
from super_admin_menu import super_admin_menu
from models.user import Role
from models.user import User
from state import Menu
import state

def login_screen():
    console = Console()

    while state.menu_stack[-1] == Menu.LOGIN:
        console.clear()
        console.print("[bold blue]==============================[/bold blue]")
        console.print("[bold blue]        Welcome to UMBS        [/bold blue]")
        console.print("[bold blue]==============================[/bold blue]\n")

        choice = inquirer.select(
            message="Please select an option:",
            choices=[
                "Login",
                "Quit"
            ],
            default="Login",
        ).execute()

        if choice == "Login":
            username = inquirer.text(message="Username:").execute()
            password = inquirer.secret(message="Password:").execute()

            if username == "super_admin" and password == "Admin_123?":
                console.print("[bold green]Login successful![/bold green]")
                state.current_user = User(0, "super_admin", Role.SUPER_ADMIN, None, None, None)
                state.menu_stack.append(Menu.SUPER_ADMIN)
                super_admin_menu()
            else:
                console.print("[bold red]Login failed! Please try again.[/bold red]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()

        elif choice == "Quit":
            console.print("[bold cyan]Goodbye![/bold cyan]")
            break
