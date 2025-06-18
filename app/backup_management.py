from datetime import datetime
from rich import box
from rich.console import Console
from rich.table import Table
from InquirerPy import inquirer

from database import Database
from encryptor import Encryptor
import state
from state import Menu

def manage_backups_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_MANAGE_BACKUPS or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_MANAGE_BACKUPS:
        console.clear()
        
        if state.menu_stack[-1] == Menu.SUPER_ADMIN_MANAGE_BACKUPS:
            console.print("[bold blue]Super Admin - Backup Management[/bold blue]")
        else:
            console.print("[bold blue]System Admin - Backup Management[/bold blue]")
        print()

        # Get available choices based on role
        choices = ["List Backups", "Create Backup", "Restore Backup"]
        
        # Only Super Admin can delete backups
        if state.menu_stack[-1] == Menu.SUPER_ADMIN_MANAGE_BACKUPS:
            choices.append("Delete Backup")
        
        choices.append("Back")

        choice = inquirer.select(
            message="Please select an option:",
            choices=choices,
            default="Back",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return
        elif choice == "List Backups":
            if state.menu_stack[-1] == Menu.SUPER_ADMIN_MANAGE_BACKUPS:
                state.menu_stack.append(Menu.SUPER_ADMIN_LIST_BACKUPS)
            else:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_LIST_BACKUPS)
            list_backups_menu()
        elif choice == "Create Backup":
            if state.menu_stack[-1] == Menu.SUPER_ADMIN_MANAGE_BACKUPS:
                state.menu_stack.append(Menu.SUPER_ADMIN_CREATE_BACKUP)
            else:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_CREATE_BACKUP)
            create_backup_menu()
        elif choice == "Restore Backup":
            if state.menu_stack[-1] == Menu.SUPER_ADMIN_MANAGE_BACKUPS:
                state.menu_stack.append(Menu.SUPER_ADMIN_RESTORE_BACKUP)
            else:
                state.menu_stack.append(Menu.SYSTEM_ADMIN_RESTORE_BACKUP)
            restore_backup_menu()
        elif choice == "Delete Backup":
            state.menu_stack.append(Menu.SUPER_ADMIN_DELETE_BACKUP)
            delete_backup_menu()

def list_backups_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_LIST_BACKUPS or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_LIST_BACKUPS:
        console.clear()
        
        if state.menu_stack[-1] == Menu.SUPER_ADMIN_LIST_BACKUPS:
            console.print("[bold blue]Super Admin - Backup List[/bold blue]")
        else:
            console.print("[bold blue]System Admin - Backup List[/bold blue]")
        print()

        backups = Database.get_all_backups()  # list of (readable, encrypted)
        
        if not backups:
            console.print("[yellow]No backups found.[/yellow]")
        else:
            table = Table(title="Database Backups", box=box.ASCII)
            table.add_column("[blue]Backup Filename[/blue]")
            table.add_column("[blue]Created Date[/blue]")
            table.add_column("[blue]Created Time[/blue]")

            for readable, _ in backups:
                # parse date/time from readable name
                timestamp_str = readable.replace("backup_", "").replace(".db", "")
                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
                    date_str = timestamp.strftime("%Y-%m-%d")
                    time_str = timestamp.strftime("%H:%M:%S")
                except ValueError:
                    date_str = "Unknown"
                    time_str = "Unknown"
                table.add_row(readable, date_str, time_str)
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

def create_backup_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_CREATE_BACKUP or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_CREATE_BACKUP:
        console.clear()
        
        if state.menu_stack[-1] == Menu.SUPER_ADMIN_CREATE_BACKUP:
            console.print("[bold blue]Super Admin - Create Backup[/bold blue]")
        else:
            console.print("[bold blue]System Admin - Create Backup[/bold blue]")
        print()

        console.print("This will create a backup of the current database.")
        print()

        choice = inquirer.select(
            message="Do you want to create a backup?",
            choices=["Yes", "No"],
            default="No",
        ).execute()

        if choice == "No":
            state.menu_stack.pop()
            return

        # backup maken
        backup_filename = Database.create_backup()
        
        if backup_filename:
            # log backup
            Database.insert_log(
                Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                Encryptor.encrypt(state.current_user.username),
                Encryptor.encrypt("Database Backup Created"),
                Encryptor.encrypt(f"Backup file: {backup_filename}"),
                Encryptor.encrypt("0")
            )
            
            console.print(f"[bold green]Backup created successfully![/bold green]")
            console.print(f"[green]Backup file: {backup_filename}[/green]")
        else:
            console.print("[bold red]Failed to create backup![/bold red]")
            console.print("[red]Database file not found.[/red]")

        console.print("[bright_black]Press enter to continue[/bright_black]")
        input()
        state.menu_stack.pop()
        return

def delete_backup_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_DELETE_BACKUP:
        console.clear()
        console.print("[bold blue]Super Admin - Delete Backup[/bold blue]")
        print()

        backups = Database.get_all_backups()  # list of (readable, encrypted)
        
        if not backups:
            console.print("[yellow]No backups found.[/yellow]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
            input()
            state.menu_stack.pop()
            return

        backup_choices = [f"{readable}" for readable, _ in backups]
        backup_choices.append("Back")

        choice = inquirer.select(
            message="Select a backup to delete:",
            choices=backup_choices,
            default="Back",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return

        # find encrypted name
        selected = next((enc for read, enc in backups if read == choice), None)
        if not selected:
            console.print("[red]Backup not found.[/red]")
            input()
            state.menu_stack.pop()
            return

        confirm_choice = inquirer.select(
            message=f"Do you really want to delete '{choice}'?",
            choices=["Yes", "No"],
            default="No",
        ).execute()

        if confirm_choice == "Yes":
            if Database.delete_backup(selected):
                Database.insert_log(
                    Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    Encryptor.encrypt(state.current_user.username),
                    Encryptor.encrypt("Database Backup Deleted"),
                    Encryptor.encrypt(f"Backup file: {choice}"),
                    Encryptor.encrypt("0")
                )
                console.print(f"[bold green]Backup '{choice}' deleted![/bold green]")
            else:
                console.print(f"[bold red]Failed to delete backup '{choice}'![/bold red]")
        else:
            console.print("[bold green]Deletion canceled.[/bold green]")

        console.print("[bright_black]Press enter to continue[/bright_black]")
        input()
        state.menu_stack.pop()
        return

def restore_backup_menu():
    console = Console()

    while state.menu_stack[-1] == Menu.SUPER_ADMIN_RESTORE_BACKUP or state.menu_stack[-1] == Menu.SYSTEM_ADMIN_RESTORE_BACKUP:
        console.clear()
        
        if state.menu_stack[-1] == Menu.SUPER_ADMIN_RESTORE_BACKUP:
            console.print("[bold blue]Super Admin - Restore Backup[/bold blue]")
        else:
            console.print("[bold blue]System Admin - Restore Backup[/bold blue]")
        print()

        console.print("[bold red]WARNING: This will overwrite the current database![/bold red]")
        console.print("[yellow]A backup of the current database will be made before restoring.[/yellow]")
        print()

        backups = Database.get_all_backups()  # list of (readable, encrypted)
        
        if not backups:
            console.print("[yellow]No backups found.[/yellow]")
            console.print("[bright_black]Press enter to continue[/bright_black]")
            input()
            state.menu_stack.pop()
            return

        backup_choices = [f"{readable}" for readable, _ in backups]
        backup_choices.append("Back")

        choice = inquirer.select(
            message="Select a backup to restore:",
            choices=backup_choices,
            default="Back",
        ).execute()

        if choice == "Back":
            state.menu_stack.pop()
            return

        # find encrypted name
        selected = next((enc for read, enc in backups if read == choice), None)
        if not selected:
            console.print("[red]Backup not found.[/red]")
            input()
            state.menu_stack.pop()
            return

        console.print(f"[bold red]Do you really want to restore '{choice}'?[/bold red]")
        console.print("[red]This will overwrite the current database![/red]")
        confirm_choice = inquirer.select(
            message="Proceed with restore?",
            choices=["Yes", "No"],
            default="No",
        ).execute()

        if confirm_choice == "Yes":
            if Database.restore_backup(selected):
                Database.insert_log(
                    Encryptor.encrypt(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    Encryptor.encrypt(state.current_user.username),
                    Encryptor.encrypt("Database Backup Restored"),
                    Encryptor.encrypt(f"Backup file: {choice}"),
                    Encryptor.encrypt("0")
                )
                console.print(f"[bold green]Backup '{choice}' restored![/bold green]")
                console.print("[green]The application will now restart to load the restored database.[/green]")
            else:
                console.print(f"[bold red]Failed to restore backup '{choice}'![/bold red]")
                console.print("[red]The current database has been preserved.[/red]")
        else:
            console.print("[bold green]Restoration canceled.[/bold green]")

        console.print("[bright_black]Press enter to continue[/bright_black]")
        input()
        state.menu_stack.pop()
        return 