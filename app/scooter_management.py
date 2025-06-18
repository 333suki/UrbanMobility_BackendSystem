from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from InquirerPy import inquirer
from datetime import datetime

import state
from encryptor import Encryptor
from state import Menu
from database import Database
from models.scooter import Scooter
import util

def manage_scooters_menu():
    console = Console()
    while state.menu_stack[-1] == Menu.SUPER_ADMIN_MANAGE_SCOOTERS or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_MANAGE_SCOOTERS:
        console.clear()
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
    while state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_LIST_SCOOTERS or state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_LIST_SCOOTERS:
        console.clear()
        table = Table(title="Scooters", box=box.ASCII)
        table.add_column("[blue]ID[/blue]")
        table.add_column("[blue]Serial Number[/blue]")
        table.add_column("[blue]Brand[/blue]")
        table.add_column("[blue]Model[/blue]")
        table.add_column("[blue]Top Speed (km/h)[/blue]")
        table.add_column("[blue]Battery Capacity (Wh)[/blue]")
        table.add_column("[blue]State of Charge (%)[/blue]")
        table.add_column("[blue]Target Range SOC(%:%)[/blue]")
        table.add_column("[blue]Location (lon:lat)[/blue]")
        table.add_column("[blue]Out of Service[/blue]")
        table.add_column("[blue]Mileage[/blue]")
        table.add_column("[blue]Last Maintenance Date[/blue]")
        for scooter in Database.get_all_scooters():
            table.add_row(str(scooter.ID), scooter.serial_number, scooter.brand, scooter.model, str(scooter.top_speed), str(scooter.battery_capacity), str(scooter.state_of_charge), f"{scooter.target_rance_soc[0]}:{scooter.target_rance_soc[1]}", scooter.location, "Yes" if scooter.out_of_service_status == "1" else "No", str(scooter.mileage), scooter.last_maintenance_date.strftime("%Y-%m-%d"))
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
    serial_number: str | None = None
    brand: str | None = None
    model: str | None = None
    top_speed: str | None = None
    battery_capacity: str | None = None
    state_of_charge: str | None = None
    target_range_soc: str | None = None
    location: str | None = None
    out_of_service_status: str | None = None
    mileage: str | None = None
    last_maintenance_date: str | None = None

    while state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_CREATE_SCOOTER or state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_CREATE_SCOOTER:
        console.clear()
        console.print("[bold blue]Create Scooter[/bold blue]")
        print()

        console.print("[cyan]Serial Number:[/cyan]                ", end="")
        if serial_number is not None:
            console.print(f"[white]{serial_number}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Brand:[/cyan]                        ", end="")
        if brand is not None:
            console.print(f"[white]{brand}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Model:[/cyan]                        ", end="")
        if model is not None:
            console.print(f"[white]{model}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Top speed (km/h):[/cyan]             ", end="")
        if top_speed is not None:
            console.print(f"[white]{top_speed}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Battery Capacity (Wh):[/cyan]        ", end="")
        if battery_capacity is not None:
            console.print(f"[white]{battery_capacity}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]State of Charge (%):[/cyan]          ", end="")
        if state_of_charge is not None:
            console.print(f"[white]{state_of_charge}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Target Range State of Charge:[/cyan] ", end="")
        if target_range_soc is not None:
            console.print(f"[white]{target_range_soc}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Location (lon:lat):[/cyan]           ", end="")
        if location is not None:
            console.print(f"[white]{location}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Out of Service Status:[/cyan]        ", end="")
        if out_of_service_status is not None:
            console.print(f"[white]{out_of_service_status}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Mileage (km):[/cyan]                 ", end="")
        if mileage is not None:
            console.print(f"[white]{mileage}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Last Maintenance Date:[/cyan]        ", end="")
        if last_maintenance_date is not None:
            console.print(f"[white]{last_maintenance_date}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        print()
        choice = inquirer.select(
            message="Please select an option:",
            choices=[
                "Edit Credentials",
                "Create",
                "Back"
            ],
            default="Edit Credentials",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return
        elif choice == "Edit Credentials":
            new_serial_number: str = Prompt.ask(f"[cyan]Serial Number[/cyan] [bright_black](Empty to keep {serial_number})[/bright_black]", console=console)
            if new_serial_number:
                serial_number = new_serial_number
            new_brand: str = Prompt.ask(f"[cyan]Brand[/cyan] [bright_black](Empty to keep {brand})[/bright_black]", console=console)
            if new_brand:
                brand = new_brand
            new_model: str = Prompt.ask(f"[cyan]Model[/cyan] [bright_black](Empty to keep {model})[/bright_black]", console=console)
            if new_model:
                model = new_model
            new_top_speed: str = Prompt.ask(f"[cyan]Top Speed (km/h)[/cyan] [bright_black](Empty to keep {top_speed})[/bright_black]", console=console)
            if new_top_speed:
                top_speed = new_top_speed
            new_battery_capacity: str = Prompt.ask(f"[cyan]Battery Capacity (Wh)[/cyan] [bright_black](Empty to keep {battery_capacity})[/bright_black]", console=console)
            if new_battery_capacity:
                battery_capacity = new_battery_capacity
            new_state_of_charge: str = Prompt.ask(f"[cyan]State of Charge (Percentage)[/cyan] [bright_black](Empty to keep {state_of_charge})[/bright_black]", console=console)
            if new_state_of_charge:
                state_of_charge = new_state_of_charge
            new_target_range_soc: str = Prompt.ask(f"[cyan]Target Range SoC (two percentages, seperated by \':\')[/cyan] [bright_black](Empty to keep {target_range_soc})[/bright_black]", console=console)
            if new_target_range_soc:
                target_range_soc = new_target_range_soc
            new_location: str = Prompt.ask(f"[cyan]Location (longitude & latitude, seperated by \':\')[/cyan] [bright_black](Empty to keep {location})[/bright_black]", console=console).replace(',', '.')
            if new_location:
                location = new_location
            out_of_service_status = inquirer.select(
                message="Out of Service Status:",
                choices=[
                    "Yes",
                    "No"
                ],
                default=out_of_service_status if out_of_service_status else "No",
            ).execute()
            new_mileage: str = Prompt.ask(f"[cyan]Mileage (km)[/cyan] [bright_black](Empty to keep {mileage})[/bright_black]", console=console)
            if new_mileage:
                mileage = new_mileage
            new_last_maintenance_date: str = Prompt.ask(f"[cyan]Last Maintenance Date (YYYY-MM-DD)[/cyan] [bright_black](Empty to keep {last_maintenance_date})[/bright_black]", console=console)
            if new_last_maintenance_date:
                last_maintenance_date = new_last_maintenance_date
        elif choice == "Create":
            is_valid: bool = True
            if Database.serial_number_exist(serial_number, None):
                console.print(f"[bold red]Invalid Serial Number:[/bold red]                [white]{util.parse_string(serial_number)}[/white] [bright_black]Serial number already exists[/bright_black]")
                is_valid = False
            if not util.is_valid_serial_number(serial_number):
                console.print(f"[bold red]Invalid Serial Number:[/bold red]                [white]{util.parse_string(serial_number)}[/white]")
                is_valid = False
            if not util.is_valid_scooter_brand(brand):
                console.print(f"[bold red]Invalid Brand:[/bold red]                        [white]{util.parse_string(brand)}[/white]")
                is_valid = False
            if not util.is_valid_scooter_model(model):
                console.print(f"[bold red]Invalid Model:[/bold red]                        [white]{util.parse_string(model)}[/white]")
                is_valid = False
            if not util.is_valid_top_speed(top_speed):
                console.print(f"[bold red]Invalid Top Speed:[/bold red]                    [white]{util.parse_string(top_speed)}[/white]")
                is_valid = False
            if not util.is_valid_battery_capacity(battery_capacity):
                console.print(f"[bold red]Invalid Battery Capacity:[/bold red]             [white]{util.parse_string(battery_capacity)}[/white]")
                is_valid = False
            if not util.is_valid_state_of_charge(state_of_charge):
                console.print(f"[bold red]Invalid State of Charge:[/bold red]              [white]{util.parse_string(state_of_charge)}[/white]")
                is_valid = False
            if not util.is_valid_target_range_soc(target_range_soc):
                console.print(f"[bold red]Invalid Target Range State of Charge:[/bold red] [white]{util.parse_string(target_range_soc)}[/white]")
                is_valid = False
            if not util.is_valid_location(location):
                console.print(f"[bold red]Invalid Location:[/bold red]                     [white]{util.parse_string(location)}[/white]")
                is_valid = False
            if not util.is_valid_mileage(mileage):
                console.print(f"[bold red]Invalid Mileage:[/bold red]                      [white]{util.parse_string(mileage)}[/white]")
                is_valid = False
            if not util.is_valid_last_maintenance_date(last_maintenance_date):
                console.print(f"[bold red]Invalid Last Maintenance Date:[/bold red]        [white]{util.parse_string(last_maintenance_date)}[/white]")
                is_valid = False

            if not is_valid:
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
            else:
                Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                    Encryptor.encrypt(state.current_user.username),
                                    Encryptor.encrypt("Scooter created"), Encryptor.encrypt(f"Scooter with serial number \"{serial_number}\" created"),
                                    Encryptor.encrypt("0"))
                Database.insert_scooter(Encryptor.encrypt(serial_number), Encryptor.encrypt(brand),Encryptor.encrypt(model), Encryptor.encrypt(top_speed), Encryptor.encrypt(battery_capacity), Encryptor.encrypt(state_of_charge), Encryptor.encrypt(target_range_soc), Encryptor.encrypt(location), "0" if out_of_service_status == "No" else "1", Encryptor.encrypt(mileage), Encryptor.encrypt(last_maintenance_date))
                console.print(f"[bold green]Scooter Created[/bold green]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
                state.menu_stack.pop()
                return

def update_scooter_menu():
    console = Console()

    while state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_UPDATE_SCOOTER or state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_UPDATE_SCOOTER:
        console.clear()
        console.print("[bold blue]Update Scooter[/bold blue]")
        print()
        all_scooters_dict = Database.get_all_scooters_dict()
        all_scooters_strings = list(all_scooters_dict.keys())
        all_scooters_strings.append("Back")
        choice = inquirer.select(
            message="Select Scooter to update:",
            choices=all_scooters_strings,
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return

        id_to_edit = all_scooters_dict[choice]
        scooter: Scooter = Database.get_scooter(id_to_edit)
        old_serial_number: str = scooter.serial_number

        serial_number: str | None = scooter.serial_number
        brand: str | None = scooter.brand
        model: str | None = scooter.model
        top_speed: str | None = str(scooter.top_speed)
        battery_capacity: str | None = str(scooter.battery_capacity)
        state_of_charge: str | None = str(scooter.state_of_charge)
        target_range_soc: str | None = f"{scooter.target_rance_soc[0]}:{scooter.target_rance_soc[1]}"
        location: str | None = scooter.location
        out_of_service_status: str | None = "No" if scooter.out_of_service_status == 0 else "Yes"
        mileage: str | None = str(scooter.mileage)
        last_maintenance_date: str | None = scooter.last_maintenance_date.strftime("%Y-%m-%d")

        while True:
            console.clear()
            console.print("[bold blue]Update Scooter[/bold blue]")
            print()

            console.print("[cyan]Serial Number:[/cyan]                ", end="")
            if serial_number is not None:
                console.print(f"[white]{serial_number}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Brand:[/cyan]                        ", end="")
            if brand is not None:
                console.print(f"[white]{brand}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Model:[/cyan]                        ", end="")
            if model is not None:
                console.print(f"[white]{model}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Top speed (km/h):[/cyan]             ", end="")
            if top_speed is not None:
                console.print(f"[white]{top_speed}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Battery Capacity (Wh):[/cyan]        ", end="")
            if battery_capacity is not None:
                console.print(f"[white]{battery_capacity}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]State of Charge (%):[/cyan]          ", end="")
            if state_of_charge is not None:
                console.print(f"[white]{state_of_charge}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Target Range State of Charge:[/cyan] ", end="")
            if target_range_soc is not None:
                console.print(f"[white]{target_range_soc}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Location (lon:lat):[/cyan]           ", end="")
            if location is not None:
                console.print(f"[white]{location}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Out of Service Status:[/cyan]        ", end="")
            if out_of_service_status is not None:
                console.print(f"[white]{out_of_service_status}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Mileage (km):[/cyan]                 ", end="")
            if mileage is not None:
                console.print(f"[white]{mileage}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Last Maintenance Date:[/cyan]        ", end="")
            if last_maintenance_date is not None:
                console.print(f"[white]{last_maintenance_date}[/white]")
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
                new_serial_number: str = Prompt.ask(f"[cyan]Serial Number[/cyan] [bright_black](Empty to keep {serial_number})[/bright_black]", console=console)
                if new_serial_number:
                    serial_number = new_serial_number
                new_brand: str = Prompt.ask(f"[cyan]Brand[/cyan] [bright_black](Empty to keep {brand})[/bright_black]", console=console)
                if new_brand:
                    brand = new_brand
                new_model: str = Prompt.ask(f"[cyan]Model[/cyan] [bright_black](Empty to keep {model})[/bright_black]", console=console)
                if new_model:
                    model = new_model
                new_top_speed: str = Prompt.ask(f"[cyan]Top Speed (km/h)[/cyan] [bright_black](Empty to keep {top_speed})[/bright_black]", console=console)
                if new_top_speed:
                    top_speed = new_top_speed
                new_battery_capacity: str = Prompt.ask(f"[cyan]Battery Capacity (Wh)[/cyan] [bright_black](Empty to keep {battery_capacity})[/bright_black]", console=console)
                if new_battery_capacity:
                    battery_capacity = new_battery_capacity
                new_state_of_charge: str = Prompt.ask(f"[cyan]State of Charge (Percentage)[/cyan] [bright_black](Empty to keep {state_of_charge})[/bright_black]", console=console)
                if new_state_of_charge:
                    state_of_charge = new_state_of_charge
                new_target_range_soc: str = Prompt.ask(f"[cyan]Target Range SoC (two percentages, seperated by \':\')[/cyan] [bright_black](Empty to keep {target_range_soc})[/bright_black]", console=console)
                if new_target_range_soc:
                    target_range_soc = new_target_range_soc
                new_location: str = Prompt.ask(f"[cyan]Location (longitude & latitude, seperated by \':\')[/cyan] [bright_black](Empty to keep {location})[/bright_black]", console=console).replace(',', '.')
                if new_location:
                    location = new_location
                out_of_service_status = inquirer.select(
                    message="Out of Service Status:",
                    choices=[
                        "Yes",
                        "No"
                    ],
                    default=out_of_service_status if out_of_service_status else "No",
                ).execute()
                new_mileage: str = Prompt.ask(
                    f"[cyan]Mileage[/cyan] [bright_black](Empty to keep {mileage})[/bright_black]", console=console)
                if new_mileage:
                    mileage = new_mileage
                new_last_maintenance_date: str = Prompt.ask(
                    f"[cyan]Last Maintenance Date (YYYY-MM-DD)[/cyan] [bright_black](Empty to keep {last_maintenance_date})[/bright_black]",
                    console=console)
                if new_last_maintenance_date:
                    last_maintenance_date = new_last_maintenance_date
            elif choice == "Update":
                is_valid: bool = True
                if Database.serial_number_exist(serial_number, scooter.serial_number):
                    console.print(f"[bold red]Invalid Serial Number:[/bold red]      [white]{util.parse_string(serial_number)}[/white] [bright_black]Serial number already exists[/bright_black]")
                    is_valid = False
                if not util.is_valid_serial_number(serial_number):
                    console.print(
                        f"[bold red]Invalid Serial Number:[/bold red]                [white]{util.parse_string(serial_number)}[/white]")
                    is_valid = False
                if not util.is_valid_scooter_brand(brand):
                    console.print(
                        f"[bold red]Invalid Brand:[/bold red]                        [white]{util.parse_string(brand)}[/white]")
                    is_valid = False
                if not util.is_valid_scooter_model(model):
                    console.print(
                        f"[bold red]Invalid Model:[/bold red]                        [white]{util.parse_string(model)}[/white]")
                    is_valid = False
                if not util.is_valid_top_speed(top_speed):
                    console.print(
                        f"[bold red]Invalid Top Speed:[/bold red]                    [white]{util.parse_string(top_speed)}[/white]")
                    is_valid = False
                if not util.is_valid_battery_capacity(battery_capacity):
                    console.print(
                        f"[bold red]Invalid Battery Capacity:[/bold red]             [white]{util.parse_string(battery_capacity)}[/white]")
                    is_valid = False
                if not util.is_valid_state_of_charge(state_of_charge):
                    console.print(
                        f"[bold red]Invalid State of Charge:[/bold red]              [white]{util.parse_string(state_of_charge)}[/white]")
                    is_valid = False
                if not util.is_valid_target_range_soc(target_range_soc):
                    console.print(
                        f"[bold red]Invalid Target Range State of Charge:[/bold red] [white]{util.parse_string(target_range_soc)}[/white]")
                    is_valid = False
                if not util.is_valid_location(location):
                    console.print(
                        f"[bold red]Invalid Location:[/bold red]                     [white]{util.parse_string(location)}[/white]")
                    is_valid = False
                if not util.is_valid_mileage(mileage):
                    console.print(
                        f"[bold red]Invalid Mileage:[/bold red]                      [white]{util.parse_string(mileage)}[/white]")
                    is_valid = False
                if not util.is_valid_last_maintenance_date(last_maintenance_date):
                    console.print(
                        f"[bold red]Invalid Last Maintenance Date:[/bold red]        [white]{util.parse_string(last_maintenance_date)}[/white]")
                    is_valid = False

                if not is_valid:
                    console.print("[bright_black]Press enter to continue[/bright_black]")
                    input()
                else:
                    Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                        Encryptor.encrypt(state.current_user.username),
                                        Encryptor.encrypt("Scooter updated"),
                                        Encryptor.encrypt(f"Scooter with serial number \"{serial_number}\" updated, (old serial number: \"{old_serial_number}\")"),
                                        Encryptor.encrypt("0"))
                    Database.update_scooter(scooter.ID, Encryptor.encrypt(serial_number), Encryptor.encrypt(brand), Encryptor.encrypt(model), Encryptor.encrypt(top_speed), Encryptor.encrypt(battery_capacity), Encryptor.encrypt(state_of_charge), Encryptor.encrypt(target_range_soc), Encryptor.encrypt(location), "0" if out_of_service_status == "No" else "1", Encryptor.encrypt(mileage), Encryptor.encrypt(last_maintenance_date))
                    console.print(f"[bold green]Scooter Updated[/bold green]")
                    console.print("[bright_black]Press enter to continue[/bright_black]")
                    input()
                    state.menu_stack.pop()
                    return

def delete_scooter_menu():
    console = Console()
    while state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_DELETE_SCOOTER or state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_DELETE_SCOOTER:
        console.clear()
        console.print("[bold blue]Delete Scooter[/bold blue]")
        print()

        all_scooters_dict = Database.get_all_scooters_dict()
        all_scooters_strings = list(all_scooters_dict.keys())
        all_scooters_strings.append("Back")
        choice = inquirer.select(
            message="Select Scooter to delete:",
            choices=all_scooters_strings,
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return

        confirm_choice = inquirer.select(
            message="Do you really want to delete this Scooter",
            choices=[
                "Yes",
                "No"
            ],
            default="Yes"
        ).execute()

        if confirm_choice == "Yes":
            scooter: Scooter = Database.get_scooter(int(all_scooters_dict[choice]))
            Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                Encryptor.encrypt(state.current_user.username),
                                Encryptor.encrypt("Scooter deleted"),
                                Encryptor.encrypt(f"Scooter with serial number \"{scooter.serial_number}\" deleted"),
                                Encryptor.encrypt("0"))
            Database.delete_scooter(all_scooters_dict[choice])
            console.print("[bold green]Scooter Deleted[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
        else:
            console.print("[bold green]Deletion Canceled[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
        input()
        state.menu_stack.pop()
        return
