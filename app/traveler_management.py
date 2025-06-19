from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich import box
from InquirerPy import inquirer
from datetime import datetime

import state
from models.traveler import Traveler
from encryptor import Encryptor
from state import Menu
from database import Database
import util

def manage_travelers_menu():
    console = Console()
    while state.menu_stack[-1] == Menu.SUPER_ADMIN_MANAGE_TRAVELERS or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_MANAGE_TRAVELERS:
        console.clear()
        choice = inquirer.select(
            message="Traveler Management:",
            choices=[
                "List Travelers",
                "Search Traveler",
                "Create Traveler",
                "Update Traveler",
                "Delete Traveler",
                "Back"
            ],
            default="List Travelers",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return
        elif choice == "List Travelers":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_LIST_TRAVELERS)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_LIST_TRAVELERS)
            list_travelers_menu()
        elif choice == "Search Traveler":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_SEARCH_TRAVELER)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_SEARCH_TRAVELER)
            search_travelers_menu()
        elif choice == "Create Traveler":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_CREATE_TRAVELER)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_CREATE_TRAVELER)
            create_traveler_menu()
        elif choice == "Update Traveler":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_UPDATE_TRAVELER)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_UPDATE_TRAVELER)
            update_traveler_menu()
        elif choice == "Delete Traveler":
            if state.current_user.role == util.Role.SUPER_ADMIN:
                state.menu_stack.append(Menu.SUPER_ADMIN_DELETE_TRAVELER)
            elif state.current_user.role == util.Role.SYSTEM_ADMIN:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_DELETE_TRAVELER)
            delete_traveler_menu()


def list_travelers_menu():
    console = Console()
    while state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_LIST_TRAVELERS or state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_LIST_TRAVELERS:
        console.clear()
        table = Table(title="Travelers", box=box.ASCII)
        table.add_column("[blue]ID[/blue]")
        table.add_column("[blue]First Name[/blue]")
        table.add_column("[blue]Last Name[/blue]")
        table.add_column("[blue]Birthday[/blue]")
        table.add_column("[blue]Gender[/blue]")
        table.add_column("[blue]Street Name[/blue]")
        table.add_column("[blue]House Number[/blue]")
        table.add_column("[blue]Zip Code[/blue]")
        table.add_column("[blue]City[/blue]")
        table.add_column("[blue]Email[/blue]")
        table.add_column("[blue]Phone Number[/blue]")
        table.add_column("[blue]Driving License Number[/blue]")
        table.add_column("[blue]Registration Date[/blue]")
        for traveler in Database.get_all_travelers():
            table.add_row(str(traveler.ID), traveler.first_name, traveler.last_name, traveler.birthday.strftime("%Y-%m-%d"), util.gender_to_string(traveler.gender), traveler.street_name, traveler.house_number, traveler.zip_code, traveler.city, traveler.email, traveler.phone_number, traveler.driving_license_number, traveler.registration_date.strftime("%Y-%m-%d"))
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

def search_travelers_menu():
    console = Console()
    while state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_SEARCH_TRAVELER or state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_SEARCH_TRAVELER:
        console.clear()
        search_term = Prompt.ask("[cyan]Search term[/cyan]", console=console)
        table = Table(title="Travelers", box=box.ASCII)
        table.add_column("[blue]ID[/blue]")
        table.add_column("[blue]First Name[/blue]")
        table.add_column("[blue]Last Name[/blue]")
        table.add_column("[blue]Birthday[/blue]")
        table.add_column("[blue]Gender[/blue]")
        table.add_column("[blue]Street Name[/blue]")
        table.add_column("[blue]House Number[/blue]")
        table.add_column("[blue]Zip Code[/blue]")
        table.add_column("[blue]City[/blue]")
        table.add_column("[blue]Email[/blue]")
        table.add_column("[blue]Phone Number[/blue]")
        table.add_column("[blue]Driving License Number[/blue]")
        table.add_column("[blue]Registration Date[/blue]")
        for traveler in Database.get_all_travelers():
            if search_term in traveler.first_name or search_term in traveler.last_name or search_term in str(traveler.ID):
                table.add_row(str(traveler.ID), traveler.first_name, traveler.last_name, traveler.birthday.strftime("%Y-%m-%d"), util.gender_to_string(traveler.gender), traveler.street_name, traveler.house_number, traveler.zip_code, traveler.city, traveler.email, f"+31 6{traveler.phone_number}", traveler.driving_license_number, traveler.registration_date.strftime("%Y-%m-%d"))
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

def create_traveler_menu():
    console = Console()
    first_name: str | None = None
    last_name: str | None = None
    birthday: str | None = None
    gender: str | None = None
    street_name: str | None = None
    house_number: str | None = None
    zip_code: str | None = None
    city: str | None = None
    email: str | None = None
    phone_number: str | None = None
    driving_license_number: str | None = None

    while state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_CREATE_TRAVELER or state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_CREATE_TRAVELER:
        console.clear()
        console.print("[bold blue]Create Traveler[/bold blue]")
        print()

        console.print("[cyan]First Name:[/cyan]             ", end="")
        if first_name is not None:
            console.print(f"[white]{first_name}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Last Name:[/cyan]              ", end="")
        if last_name is not None:
            console.print(f"[white]{last_name}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Birthday:[/cyan]               ", end="")
        if birthday is not None:
            console.print(f"[white]{birthday}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Gender:[/cyan]                 ", end="")
        if gender is not None:
            console.print(f"[white]{gender}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Street Name:[/cyan]            ", end="")
        if street_name is not None:
            console.print(f"[white]{street_name}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]House Number:[/cyan]           ", end="")
        if house_number is not None:
            console.print(f"[white]{house_number}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Zip Code:[/cyan]               ", end="")
        if zip_code is not None:
            console.print(f"[white]{zip_code}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]City:[/cyan]                   ", end="")
        if city is not None:
            console.print(f"[white]{city}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Email:[/cyan]                  ", end="")
        if email is not None:
            console.print(f"[white]{email}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Phone Number:[/cyan] +31 6     ", end="")
        if phone_number is not None:
            console.print(f"[white]{phone_number}[/white]")
        else:
            console.print("[bright_black]None[/bright_black]")

        console.print("[cyan]Driving License Number:[/cyan] ", end="")
        if driving_license_number is not None:
            console.print(f"[white]{driving_license_number}[/white]")
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
            new_first_name: str = Prompt.ask(f"[cyan]First Name[/cyan] [bright_black](Empty to keep {first_name})[/bright_black]", console=console)
            if new_first_name:
                first_name = new_first_name
            new_last_name: str = Prompt.ask(f"[cyan]Last Name[/cyan] [bright_black](Empty to keep {last_name})[/bright_black]", console=console)
            if new_last_name:
                last_name = new_last_name
            new_birthday: str = Prompt.ask(f"[cyan]Birthday (YYYY-MM-DD)[/cyan] [bright_black](Empty to keep {birthday})[/bright_black]", console=console)
            if new_birthday:
                birthday = new_birthday
            gender = inquirer.select(
                message="Gender:",
                choices=[
                    "Male",
                    "Female",
                    "Other"
                ],
                default=gender if gender else "Male",
            ).execute()
            new_street_name: str = Prompt.ask(f"[cyan]Street Name[/cyan] [bright_black](Empty to keep {street_name})[/bright_black]", console=console)
            if new_street_name:
                street_name = new_street_name
            new_house_number: str = Prompt.ask(f"[cyan]House Number[/cyan] [bright_black](Empty to keep {house_number})[/bright_black]", console=console)
            if new_house_number:
                house_number = new_house_number
            new_zip_code: str = Prompt.ask(f"[cyan]Zip Code (DDDDXX)[/cyan] [bright_black](Empty to keep {zip_code})[/bright_black]", console=console)
            if new_zip_code:
                zip_code = new_zip_code
            city = inquirer.select(
                message="City:",
                choices=[
                    "Rotterdam",
                    "Amsterdam",
                    "Den Haag",
                    "Utrecht",
                    "Maastricht",
                    "Nijmegen",
                    "Eindhoven",
                    "Breda",
                    "Zwolle",
                    "Groningen",
                ],
                default=city if city else "Rotterdam",
            ).execute()
            new_email: str = Prompt.ask(f"[cyan]Email[/cyan] [bright_black](Empty to keep {email})[/bright_black]", console=console)
            if new_email:
                email = new_email
            new_phone_number: str = Prompt.ask(f"[cyan]Phone Number (DDDDDDDD)[/cyan] [bright_black](Empty to keep {phone_number})[/bright_black]", console=console)
            if new_phone_number:
                phone_number = new_phone_number
            new_driving_license_number: str = Prompt.ask(f"[cyan]Driving License Number (XXDDDDDDD/XDDDDDDDD)[/cyan] [bright_black](Empty to keep {driving_license_number})[/bright_black]", console=console)
            if new_driving_license_number:
                driving_license_number = new_driving_license_number
        elif choice == "Create":
            is_valid: bool = True
            if not util.is_valid_first_name(first_name):
                console.print(f"[bold red]Invalid First Name:[/bold red]             [white]{util.parse_string(first_name)}[/white]")
                is_valid = False
            if not util.is_valid_last_name(last_name):
                console.print(f"[bold red]Invalid Last Name:[/bold red]              [white]{util.parse_string(last_name)}[/white]")
                is_valid = False
            if not util.is_valid_date(birthday):
                console.print(f"[bold red]Invalid Birthday:[/bold red]               [white]{util.parse_string(birthday)}[/white]")
                is_valid = False
            if not util.is_valid_street_name(street_name):
                console.print(f"[bold red]Invalid Street Name:[/bold red]            [white]{util.parse_string(street_name)}[/white]")
                is_valid = False
            if not util.is_valid_house_number(house_number):
                console.print(f"[bold red]Invalid House Number:[/bold red]           [white]{util.parse_string(house_number)}[/white]")
                is_valid = False
            if not util.is_valid_zip_code(zip_code):
                console.print(f"[bold red]Invalid Zip Code:[/bold red]               [white]{util.parse_string(zip_code)}[/white]")
                is_valid = False
            if not util.is_valid_email(email):
                console.print(f"[bold red]Invalid Email:[/bold red]                  [white]{util.parse_string(email)}[/white]")
                is_valid = False
            if not util.is_valid_phone_number(phone_number):
                console.print(f"[bold red]Invalid Phone Number:[/bold red]           [white]{util.parse_string(phone_number)}[/white]")
                is_valid = False
            if not util.is_valid_driving_license_number(driving_license_number):
                console.print(f"[bold red]Invalid Driving License Number:[/bold red] [white]{util.parse_string(driving_license_number)}[/white]")
                is_valid = False

            if not is_valid:
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
            else:
                Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                    Encryptor.encrypt(state.current_user.username),
                                    Encryptor.encrypt("Traveler created"), Encryptor.encrypt(f"Traveler with name \"{first_name} {last_name}\" created"),
                                    Encryptor.encrypt("0"))
                Database.insert_traveler(Encryptor.encrypt(first_name), Encryptor.encrypt(last_name), Encryptor.encrypt(birthday), Encryptor.encrypt(util.gender_string_to_db_string(gender)), Encryptor.encrypt(street_name), Encryptor.encrypt(house_number), Encryptor.encrypt(zip_code), Encryptor.encrypt(city), Encryptor.encrypt(email) , Encryptor.encrypt(phone_number), Encryptor.encrypt(driving_license_number), Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d")))
                console.print(f"[bold green]Traveler Created[/bold green]")
                console.print("[bright_black]Press enter to continue[/bright_black]")
                input()
                state.menu_stack.pop()
                return

def update_traveler_menu():
    console = Console()

    while state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_UPDATE_TRAVELER or state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_UPDATE_TRAVELER:
        console.clear()
        console.print("[bold blue]Update Traveler[/bold blue]")
        print()
        all_travelers_dict = Database.get_all_travelers_dict()
        all_travelers_strings = list(all_travelers_dict.keys())
        all_travelers_strings.append("Back")
        choice = inquirer.select(
            message="Select Traveler to update:",
            choices=all_travelers_strings,
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return

        id_to_edit = all_travelers_dict[choice]
        traveler: Traveler = Database.get_traveler(id_to_edit)

        first_name: str | None = traveler.first_name
        last_name: str | None = traveler.last_name
        birthday: str | None = traveler.birthday.strftime("%Y-%d-%m")
        gender: str | None = util.gender_to_string(traveler.gender)
        street_name: str | None = traveler.street_name
        house_number: str | None = traveler.house_number
        zip_code: str | None = traveler.zip_code
        city: str | None = traveler.city
        email: str | None = traveler.email
        phone_number: str | None = traveler.phone_number
        driving_license_number: str | None = traveler.driving_license_number

        while True:
            console.clear()
            console.print("[bold blue]Update Scooter[/bold blue]")
            print()

            console.print("[cyan]First Name:[/cyan]             ", end="")
            if first_name is not None:
                console.print(f"[white]{first_name}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Last Name:[/cyan]              ", end="")
            if last_name is not None:
                console.print(f"[white]{last_name}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Birthday:[/cyan]               ", end="")
            if birthday is not None:
                console.print(f"[white]{birthday}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Gender:[/cyan]                 ", end="")
            if gender is not None:
                console.print(f"[white]{gender}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Street Name:[/cyan]            ", end="")
            if street_name is not None:
                console.print(f"[white]{street_name}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]House Number:[/cyan]           ", end="")
            if house_number is not None:
                console.print(f"[white]{house_number}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Zip Code:[/cyan]               ", end="")
            if zip_code is not None:
                console.print(f"[white]{zip_code}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]City:[/cyan]                   ", end="")
            if city is not None:
                console.print(f"[white]{city}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Email:[/cyan]                  ", end="")
            if email is not None:
                console.print(f"[white]{email}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Phone Number:[/cyan] +31 6     ", end="")
            if phone_number is not None:
                console.print(f"[white]{phone_number}[/white]")
            else:
                console.print("[bright_black]None[/bright_black]")

            console.print("[cyan]Driving License Number:[/cyan] ", end="")
            if driving_license_number is not None:
                console.print(f"[white]{driving_license_number}[/white]")
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
                new_first_name: str = Prompt.ask(f"[cyan]First Name[/cyan] [bright_black](Empty to keep {first_name})[/bright_black]", console=console)
                if new_first_name:
                    first_name = new_first_name
                new_last_name: str = Prompt.ask(
                    f"[cyan]Last Name[/cyan] [bright_black](Empty to keep {last_name})[/bright_black]", console=console)
                if new_last_name:
                    last_name = new_last_name
                new_birthday: str = Prompt.ask(
                    f"[cyan]Birthday (YYYY-MM-DD)[/cyan] [bright_black](Empty to keep {birthday})[/bright_black]",
                    console=console)
                if new_birthday:
                    birthday = new_birthday
                gender = inquirer.select(
                    message="Gender:",
                    choices=[
                        "Male",
                        "Female",
                        "Other"
                    ],
                    default=gender if gender else "Male",
                ).execute()
                new_street_name: str = Prompt.ask(
                    f"[cyan]Street Name[/cyan] [bright_black](Empty to keep {street_name})[/bright_black]",
                    console=console)
                if new_street_name:
                    street_name = new_street_name
                new_house_number: str = Prompt.ask(
                    f"[cyan]House Number[/cyan] [bright_black](Empty to keep {house_number})[/bright_black]",
                    console=console)
                if new_house_number:
                    house_number = new_house_number
                new_zip_code: str = Prompt.ask(
                    f"[cyan]Zip Code (DDDDXX)[/cyan] [bright_black](Empty to keep {zip_code})[/bright_black]",
                    console=console)
                if new_zip_code:
                    zip_code = new_zip_code
                city = inquirer.select(
                    message="City:",
                    choices=[
                        "Rotterdam",
                        "Amsterdam",
                        "Den Haag",
                        "Utrecht",
                        "Maastricht",
                        "Nijmegen",
                        "Eindhoven",
                        "Breda",
                        "Zwolle",
                        "Groningen",
                    ],
                    default=city if city else "Rotterdam",
                ).execute()
                new_email: str = Prompt.ask(f"[cyan]Email[/cyan] [bright_black](Empty to keep {email})[/bright_black]", console=console)
                if new_email:
                    email = new_email
                new_phone_number: str = Prompt.ask(
                    f"[cyan]Phone Number (DDDDDDDD)[/cyan] [bright_black](Empty to keep {phone_number})[/bright_black]",
                    console=console)
                if new_phone_number:
                    phone_number = new_phone_number
                new_driving_license_number: str = Prompt.ask(
                    f"[cyan]Driving License Number (XXDDDDDDD/XDDDDDDDD)[/cyan] [bright_black](Empty to keep {driving_license_number})[/bright_black]",
                    console=console)
                if new_driving_license_number:
                    driving_license_number = new_driving_license_number
            elif choice == "Update":
                is_valid: bool = True
                if not util.is_valid_first_name(first_name):
                    console.print(f"[bold red]Invalid First Name:[/bold red]             [white]{util.parse_string(first_name)}[/white]")
                    is_valid = False
                if not util.is_valid_last_name(last_name):
                    console.print(f"[bold red]Invalid Last Name:[/bold red]              [white]{util.parse_string(last_name)}[/white]")
                    is_valid = False
                if not util.is_valid_date(birthday):
                    console.print(f"[bold red]Invalid Birthday:[/bold red]               [white]{util.parse_string(birthday)}[/white]")
                    is_valid = False
                if not util.is_valid_street_name(street_name):
                    console.print(f"[bold red]Invalid Street Name:[/bold red]            [white]{util.parse_string(street_name)}[/white]")
                    is_valid = False
                if not util.is_valid_house_number(house_number):
                    console.print(f"[bold red]Invalid House Number:[/bold red]           [white]{util.parse_string(house_number)}[/white]")
                    is_valid = False
                if not util.is_valid_zip_code(zip_code):
                    console.print(f"[bold red]Invalid Zip Code:[/bold red]               [white]{util.parse_string(zip_code)}[/white]")
                    is_valid = False
                if not util.is_valid_email(email):
                    console.print(f"[bold red]Invalid Email:[/bold red]                  [white]{util.parse_string(email)}[/white]")
                    is_valid = False
                if not util.is_valid_phone_number(phone_number):
                    console.print(f"[bold red]Invalid Phone Number:[/bold red]           [white]{util.parse_string(phone_number)}[/white]")
                    is_valid = False
                if not util.is_valid_driving_license_number(driving_license_number):
                    console.print(f"[bold red]Invalid Driving License Number:[/bold red] [white]{util.parse_string(driving_license_number)}[/white]")
                    is_valid = False

                if not is_valid:
                    console.print("[bright_black]Press enter to continue[/bright_black]")
                    input()
                else:
                    Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                        Encryptor.encrypt(state.current_user.username),
                                        Encryptor.encrypt("Traveler updated"),
                                        Encryptor.encrypt(f"Traveler with name \"{first_name} {last_name}\" updated, (old name: \"{traveler.first_name} {traveler.last_name}\")"),
                                        Encryptor.encrypt("0"))
                    Database.update_traveler(traveler.ID, Encryptor.encrypt(first_name), Encryptor.encrypt(last_name), Encryptor.encrypt(birthday), Encryptor.encrypt(util.gender_string_to_db_string(gender)), Encryptor.encrypt(street_name), Encryptor.encrypt(house_number), Encryptor.encrypt(zip_code), Encryptor.encrypt(city), Encryptor.encrypt(email), Encryptor.encrypt(phone_number), Encryptor.encrypt(driving_license_number))
                    console.print(f"[bold green]Traveler Updated[/bold green]")
                    console.print("[bright_black]Press enter to continue[/bright_black]")
                    input()
                    state.menu_stack.pop()
                    return

def delete_traveler_menu():
    console = Console()
    while state.current_user.role == util.Role.SUPER_ADMIN and state.menu_stack[-1] == Menu.SUPER_ADMIN_DELETE_TRAVELER or state.current_user.role == util.Role.SYSTEM_ADMIN and state.menu_stack[-1] == Menu.SYSTEM_ADMIN_DELETE_TRAVELER:
        console.clear()
        console.print("[bold blue]Delete Traveler[/bold blue]")
        print()

        all_travelers_dict = Database.get_all_travelers_dict()
        all_travelers_strings = list(all_travelers_dict.keys())
        all_travelers_strings.append("Back")
        choice = inquirer.select(
            message="Select Traveler to delete:",
            choices=all_travelers_strings,
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return

        confirm_choice = inquirer.select(
            message="Do you really want to kill this Traveler",
            choices=[
                "Yes",
                "No"
            ],
            default="Yes"
        ).execute()

        if confirm_choice == "Yes":
            traveler: Traveler = Database.get_traveler(int(all_travelers_dict[choice]))
            Database.insert_log(Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                Encryptor.encrypt(state.current_user.username),
                                Encryptor.encrypt("Traveler deleted"),
                                Encryptor.encrypt(f"Traveler with name \"{traveler.first_name} {traveler.last_name}\" deleted"),
                                Encryptor.encrypt("0"))
            Database.delete_traveler(all_travelers_dict[choice])
            console.print("[bold green]Traveler Deleted[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
        else:
            console.print("[bold green]Deletion Canceled[/bold green]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
        input()
        state.menu_stack.pop()
        return
