import time
from rich.console import Console
from InquirerPy import inquirer
from super_admin_page import super_admin_page

def login_screen():
    console = Console()

    while True:
        console.clear()

        console.print("[bold blue]==============================[/bold blue]")
        console.print("[bold blue]        Welcome to UMBS        [/bold blue]")
        console.print("[bold blue]==============================[/bold blue]\n")

        # arrow navigation with inquirer
        choice = inquirer.select(
            message="Please select an option:",
            choices=[
                "Login",
                "Forgot Password",
                "Quit"
            ],
            default="Login",
        ).execute()

        if choice == "Login":
            username = inquirer.text(message="Please enter your Username:").execute()
            password = inquirer.secret(message="Please enter your Password:").execute()

            if username == "super_admin" and password == "Admin_123?":
                console.print("[bold green]Login successful![/bold green]")
                super_admin_page()
            else:
                console.print("[bold red]Login failed! Please try again.[/bold red]")
                time.sleep(3)

        elif choice == "Forgot Password":
            # FORGOR
            console.print("[bold yellow]Forgot Password feature is not implemented yet.[/bold yellow]")
            time.sleep(3)

        elif choice == "Quit":
            # BYE
            console.print("[bold cyan]Goodbye![/bold cyan]")
            break

        else:
            # NUH UH Error
            console.print("[bold red]Invalid choice. Please select a valid option.[/bold red]")
            time.sleep(2)
