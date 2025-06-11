from rich.console import Console
from InquirerPy import inquirer
import time
import state
from state import Menu

def super_admin_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN:
        console.clear()
        console.print("[bold blue]==============================[/bold blue]")
        console.print("[bold blue]       Super Admin Page       [/bold blue]")
        console.print("[bold blue]==============================[/bold blue]\n")

        choice = inquirer.select(
            message="Please select an option:",
            choices=[
                "View System Logs",
                "Manage Users",
                "Logout"
            ],
            default="View System Logs",
        ).execute()

        if choice == "View System Logs":
            console.print("[bold yellow]System Logs feature is not implemented yet.[/bold yellow]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
            input()

        elif choice == "Manage Users":
            console.print("[bold yellow]Manage Users feature is not implemented yet.[/bold yellow]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
            input()

        elif choice == "Logout":
            state.current_user = None
            state.menu_stack.pop()
            console.print("[bold cyan]Logged out[/bold cyan]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
            input()
            break
