from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from InquirerPy import inquirer

import state
from state import Menu
from database import Database
import util

def print_logged_in_user(console):
    if state.current_user:
        role_str = util.role_to_string(state.current_user.role)
        console.print(f"[green]Logged in as:[/green] {state.current_user.username} ({role_str})")
        print()

def manage_scooters_menu():
    console = Console()
    while state.menu_stack[-1] == Menu.SUPER_ADMIN_MANAGE_SCOOTERS:
        console.clear()
        print_logged_in_user(console)
        choice = inquirer.select(
            message="Scooter Management:",
            choices=[
                "List Scooters",
                "Create Scooter",
                "Update Scooter",
                "Delete Scooter",
                "Back"
            ],
            default="List Scooters",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return
        elif choice == "List Scooters":
        
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_LIST_SCOOTERS)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_LIST_SCOOTERS)
            else:
                state.menu_stack.append(Menu.SERVICE_ENGINEER_LIST_SCOOTERS)
            list_scooters_menu()
        elif choice == "Create Scooter":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_CREATE_SCOOTER)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_CREATE_SCOOTER)
            else:
                state.menu_stack.append(Menu.SERVICE_ENGINEER_CREATE_SCOOTER)
            create_scooter_menu()
        elif choice == "Update Scooter":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_UPDATE_SCOOTER)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_UPDATE_SCOOTER)
            else:
                state.menu_stack.append(Menu.SERVICE_ENGINEER_UPDATE_SCOOTER)
            update_scooter_menu()
        elif choice == "Delete Scooter":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_DELETE_SCOOTER)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_DELETE_SCOOTER)
            else:
                state.menu_stack.append(Menu.SERVICE_ENGINEER_DELETE_SCOOTER)
            delete_scooter_menu()

def list_scooters_menu():
    console = Console()
    # Check for all possible roles
    while (
        (state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_LIST_SCOOTERS) or
        (state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_LIST_SCOOTERS)
    ):
        console.clear()
        print_logged_in_user(console)
        table = Table(title="Scooters", box=box.ASCII)
        table.add_column("ID")
        table.add_column("Brand")
        table.add_column("Model")
        table.add_column("Top Speed")
        table.add_column("Battery Capacity")
        table.add_column("State of Charge")
        table.add_column("Target Range SOC")
        table.add_column("Location")
        table.add_column("Out of Service")
        table.add_column("Mileage")
        table.add_column("Last Maintenance")
        for scooter in Database.list_scooters():
            table.add_row(
                scooter["ID"], scooter["brand"], scooter["model"], str(scooter["top_speed"]),
                str(scooter["battery_capacity"]), str(scooter["state_of_charge"]),
                scooter["target_range_soc"], scooter["location"], str(scooter["out_of_service_status"]),
                str(scooter["mileage"]), scooter["last_maintenance_date"]
            )
        console.print(table)
        print()
        choice = inquirer.select(
            message="Please select an option:",
            choices=["Back"],
            default="Back",
        ).execute()
        if choice == "Back":
            state.menu_stack.pop()
            return

def create_scooter_menu():
    console = Console()
    # Check for all possible roles
    while (
        (state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_CREATE_SCOOTER) or
        (state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_CREATE_SCOOTER)
    ):
        console.clear()
        print_logged_in_user(console)
        console.print("[bold blue]Create Scooter[/bold blue]")
        print()
        ID = Prompt.ask("[cyan]Scooter ID[/cyan]", console=console)
        brand = Prompt.ask("[cyan]Brand[/cyan]", console=console)
        model = Prompt.ask("[cyan]Model[/cyan]", console=console)
        top_speed = int(Prompt.ask("[cyan]Top Speed[/cyan]", console=console))
        battery_capacity = int(Prompt.ask("[cyan]Battery Capacity[/cyan]", console=console))
        state_of_charge = int(Prompt.ask("[cyan]State of Charge[/cyan]", console=console))
        target_range_soc = Prompt.ask("[cyan]Target Range SOC[/cyan]", console=console)
        location = Prompt.ask("[cyan]Location[/cyan]", console=console)
        out_of_service_status = int(Prompt.ask("[cyan]Out of Service Status (0=No, 1=Yes)[/cyan]", console=console))
        mileage = int(Prompt.ask("[cyan]Mileage[/cyan]", console=console))
        last_maintenance_date = Prompt.ask("[cyan]Last Maintenance Date (YYYY-MM-DD)[/cyan]", console=console)
        Database.insert_scooter(ID, brand, model, top_speed, battery_capacity, state_of_charge,
                                target_range_soc, location, out_of_service_status, mileage, last_maintenance_date)
        console.print("[bold green]Scooter Created[/bold green]")
        console.print("[bright_black]Press enter to continue[/bright_black]")
        input()
        state.menu_stack.pop()
        return

def update_scooter_menu():
    console = Console()
    while (
        (state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_UPDATE_SCOOTER) or
        (state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_UPDATE_SCOOTER)
    ):
        console.clear()
        print_logged_in_user(console)
        scooters = Database.list_scooters()
        if not scooters:
            console.print("[bold red]No scooters found.[/bold red]")
            input("Press enter to continue...")
            state.menu_stack.pop()
            return
        scooter_dict = {f"{s['ID']} ({s['brand']} {s['model']})": s for s in scooters}
        scooter_choices = list(scooter_dict.keys())
        scooter_choices.append("Back")
        choice = inquirer.select(
            message="Select Scooter to update:",
            choices=scooter_choices,
        ).execute()
        if choice == "Back":
            state.menu_stack.pop()
            return
        scooter = scooter_dict[choice]
        brand = Prompt.ask("[cyan]Brand[/cyan]", default=scooter["brand"], console=console)
        model = Prompt.ask("[cyan]Model[/cyan]", default=scooter["model"], console=console)
        top_speed = int(Prompt.ask("[cyan]Top Speed[/cyan]", default=str(scooter["top_speed"]), console=console))
        battery_capacity = int(Prompt.ask("[cyan]Battery Capacity[/cyan]", default=str(scooter["battery_capacity"]), console=console))
        state_of_charge = int(Prompt.ask("[cyan]State of Charge[/cyan]", default=str(scooter["state_of_charge"]), console=console))
        target_range_soc = Prompt.ask("[cyan]Target Range SOC[/cyan]", default=scooter["target_range_soc"], console=console)
        location = Prompt.ask("[cyan]Location[/cyan]", default=scooter["location"], console=console)
        out_of_service_status = int(Prompt.ask("[cyan]Out of Service Status (0=No, 1=Yes)[/cyan]", default=str(scooter["out_of_service_status"]), console=console))
        mileage = int(Prompt.ask("[cyan]Mileage[/cyan]", default=str(scooter["mileage"]), console=console))
        last_maintenance_date = Prompt.ask("[cyan]Last Maintenance Date (YYYY-MM-DD)[/cyan]", default=scooter["last_maintenance_date"], console=console)
        Database.update_scooter(
            scooter["ID"], brand, model, top_speed, battery_capacity, state_of_charge,
            target_range_soc, location, out_of_service_status, mileage, last_maintenance_date
        )
        console.print("[bold green]Scooter Updated[/bold green]")
        console.print("[bright_black]Press enter to continue[/bright_black]")
        input()
        state.menu_stack.pop()
        return

def delete_scooter_menu():
    console = Console()
    while (
        (state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_DELETE_SCOOTER) or
        (state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_DELETE_SCOOTER)
    ):
        console.clear()
        print_logged_in_user(console)
        scooters = Database.list_scooters()
        if not scooters:
            console.print("[bold red]No scooters found.[/bold red]")
            input("Press enter to continue...")
            state.menu_stack.pop()
            return
        scooter_dict = {f"{s['ID']} ({s['brand']} {s['model']})": s for s in scooters}
        scooter_choices = list(scooter_dict.keys())
        scooter_choices.append("Back")
        choice = inquirer.select(
            message="Select Scooter to delete:",
            choices=scooter_choices,
        ).execute()
        if choice == "Back":
            state.menu_stack.pop()
            return
        confirm = inquirer.select(
            message=f"Are you sure you want to delete scooter {choice}?",
            choices=["Yes", "No"],
            default="No"
        ).execute()
        if confirm == "Yes":
            Database.delete_scooter(scooter_dict[choice]["ID"])
            console.print("[bold green]Scooter Deleted[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
            input()
        state.menu_stack.pop()
        return