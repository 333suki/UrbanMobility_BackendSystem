from rich.console import Console
from InquirerPy import inquirer
import time

def super_admin_menu():
    console = Console()
    while True:
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
            time.sleep(3)

        elif choice == "Manage Users":
            console.print("[bold yellow]Manage Users feature is not implemented yet.[/bold yellow]")
            time.sleep(3)

        elif choice == "Logout":
            console.print("[bold cyan]Logging out...[/bold cyan]")
            time.sleep(2)
            break
