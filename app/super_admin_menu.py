from rich.console import Console
from InquirerPy import inquirer
import state
from state import Menu
from account_management import manage_accounts_menu
from scooter_management import manage_scooters_menu
import util

def print_logged_in_user(console):
    if state.current_user:
        role_str = util.role_to_string(state.current_user.role)
        console.print(f"[green]Logged in as:[/green] {state.current_user.username} ({role_str})")
        print()

def super_admin_main_menu():
    console = Console()
    while state.menu_stack[-1] == Menu.SUPER_ADMIN_MAIN:
        console.clear()
        print_logged_in_user(console)
        console.print("[bold blue]Super Admin Page[/bold blue]")
        print()
        choice = inquirer.select(
            message="Please select an option:",
            choices=[
                "Manage Accounts",
                "Manage Scooters",
                "Logout"
            ],
            default=state.last_menu_choice,
        ).execute()

        if choice == "Logout":
            state.current_user = None
            console.print("[bold cyan]Logged out[/bold cyan]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
            input()
            state.menu_stack.pop()
            return
        elif choice == "Manage Accounts":
            state.last_menu_choice = "Manage Accounts"
            state.menu_stack.append(Menu.SUPER_ADMIN_MANAGE_ACCOUNTS)
            manage_accounts_menu()
        elif choice == "Manage Scooters":
            state.last_menu_choice = "Manage Scooters"
            state.menu_stack.append(Menu.SUPER_ADMIN_MANAGE_SCOOTERS)
            manage_scooters_menu()