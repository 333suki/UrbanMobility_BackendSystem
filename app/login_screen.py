import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

def login_screen():
    console = Console()

    while True:
        # clear console
        console.clear()

        # title
        console.print(Panel("[bold blue]UMBS[/bold blue]", expand=False,))

        # prompt user and passwrd
        username = Prompt.ask("[bold green]Please enter your Username[/bold green]")
        password = Prompt.ask("[bold green]Please enter your Password[/bold green]", password=True)

        # Sim login
        if username == "super_admin" and password == "Admin_123?":
            console.print("[bold green]Login successful![/bold green]")
            break
        else:
            console.print("[bold red]Login failed! Please try again.[/bold red]")
            time.sleep(2)  # 3s 


