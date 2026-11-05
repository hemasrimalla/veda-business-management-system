"""
program_manager.py
------------------
Program management module for Veda Technology Business & Service Management System.

Handles:
- Listing and table formatting for Training, Internship, and Technology programs
- Viewing full course/program details (seats, duration, fee, status)
- Adding new programs with auto-generated IDs and validation
- Modifying program details (title, type, duration, fee, seats, status)
- Removing programs with safety confirmation
"""

from typing import List, Optional
from models import Program
from validators import (
    prompt_input,
    prompt_float,
    prompt_int,
    prompt_choice,
    prompt_confirm,
    validate_non_empty,
)
import storage


def display_programs_table(programs: List[Program], title: str = "VEDA PROGRAMS & COURSES") -> None:
    """Print a clean, tabular view of programs.

    Args:
        programs (list): List of Program objects.
        title (str): Header title for the table.
    """
    if not programs:
        print("\n  [i] No programs available to display.")
        return

    print("\n" + "=" * 96)
    print(f" {title.upper()} (Total: {len(programs)})".center(96))
    print("=" * 96)
    header = f"{'ID':<9} {'Program Title':<42} {'Type':<13} {'Duration':<11} {'Fee (USD)':>10} {'Seats':^7} {'Status':^9}"
    print(header)
    print("-" * 96)

    for p in programs:
        title_trimmed = (p.title[:39] + "...") if len(p.title) > 42 else p.title
        fee_str = "Free" if p.fee == 0 else f"${p.fee:,.2f}"
        print(f"{p.id:<9} {title_trimmed:<42} {p.type:<13} {p.duration:<11} {fee_str:>10} {p.seats:^7} {p.status:^9}")

    print("=" * 96)


def find_program_by_id(programs: List[Program], program_id: str) -> Optional[Program]:
    """Lookup a program by case-insensitive ID match."""
    program_id_clean = program_id.strip().upper()
    for prg in programs:
        if prg.id.upper() == program_id_clean:
            return prg
    return None


def view_program_details(programs: List[Program]) -> None:
    """Prompt for a program ID and display all fields clearly."""
    if not programs:
        print("\n  [!] No programs found in the system.")
        return

    prg_id = prompt_input("Enter Program ID to view (e.g., PRG-201)").upper()
    prg = find_program_by_id(programs, prg_id)

    if not prg:
        print(f"  [!] Error: No program found with ID '{prg_id}'.")
        return

    fee_display = f"${prg.fee:,.2f}" if prg.fee > 0 else "Free / Sponsored Internship"
    print("\n" + "-" * 60)
    print(f" PROGRAM DETAILS: {prg.id}".center(60))
    print("-" * 60)
    print(f"  Program ID   : {prg.id}")
    print(f"  Title        : {prg.title}")
    print(f"  Track Type   : {prg.type}")
    print(f"  Duration     : {prg.duration}")
    print(f"  Fee (USD)    : {fee_display}")
    print(f"  Capacity     : {prg.seats} seats")
    print(f"  Status       : {prg.status}")
    print("-" * 60)


def add_program(programs: List[Program]) -> Optional[Program]:
    """Interactive workflow to create and persist a new program or internship track."""
    print("\n--- Add New Program / Internship Track ---")
    new_id = storage.generate_program_id(programs)
    print(f"Generated Program ID: {new_id}")

    title = prompt_input("Enter Program Title", validator_fn=validate_non_empty)
    prog_type = prompt_choice("Select Program Type:", ["Training", "Internship", "Technology"])
    duration = prompt_input("Enter Duration (e.g., '12 Weeks', '6 Months')", validator_fn=validate_non_empty)

    # Fee (Internships can default to 0)
    default_fee = 0.0 if prog_type == "Internship" else 500.0
    fee = prompt_float(f"Enter Enrollment Fee in USD ($) (Enter 0 for free/stipend)", min_val=0.0, default=default_fee)

    seats = prompt_int("Enter Maximum Seat Capacity", min_val=1, default=25)
    status = prompt_choice("Select Initial Status:", ["Open", "Upcoming", "Closed", "Ongoing"], default="Open")

    new_prog = Program(
        id=new_id,
        title=title,
        type=prog_type,
        duration=duration,
        fee=fee,
        seats=seats,
        status=status,
    )

    programs.append(new_prog)
    if storage.save_programs(programs):
        print(f"\n[OK] Program '{new_prog.title}' ({new_prog.id}) added successfully!")
        return new_prog
    else:
        print("\n[!] Error saving program to storage.")
        return None


def update_program(programs: List[Program]) -> bool:
    """Interactive workflow to update an existing program."""
    if not programs:
        print("\n  [!] No programs available to update.")
        return False

    prg_id = prompt_input("Enter Program ID to update (e.g., PRG-201)").upper()
    prg = find_program_by_id(programs, prg_id)

    if not prg:
        print(f"  [!] Error: Program '{prg_id}' not found.")
        return False

    print(f"\nUpdating Program: {prg.id} - {prg.title}")
    print("(Press [Enter] to keep current value)\n")

    # Title
    new_title = prompt_input("Program Title", allow_blank=True, default=prg.title)
    prg.title = new_title

    # Type
    print(f"Current Type: {prg.type}")
    if prompt_confirm("Do you want to update track type?", default_yes=False):
        prg.type = prompt_choice("Select Track Type:", ["Training", "Internship", "Technology"], default=prg.type)

    # Duration
    new_dur = prompt_input("Duration", allow_blank=True, default=prg.duration)
    prg.duration = new_dur

    # Fee
    new_fee = prompt_float("Fee (USD)", min_val=0.0, default=prg.fee)
    prg.fee = new_fee

    # Seats
    new_seats = prompt_int("Seat Capacity", min_val=1, default=prg.seats)
    prg.seats = new_seats

    # Status
    prg.status = prompt_choice("Enrollment Status:", ["Open", "Upcoming", "Closed", "Ongoing"], default=prg.status)

    if storage.save_programs(programs):
        print(f"\n[OK] Program '{prg.id}' updated successfully!")
        return True
    else:
        print("\n[!] Error saving updated program.")
        return False


def delete_program(programs: List[Program]) -> bool:
    """Remove a program after confirmation."""
    if not programs:
        print("\n  [!] No programs to delete.")
        return False

    prg_id = prompt_input("Enter Program ID to delete (e.g., PRG-201)").upper()
    prg = find_program_by_id(programs, prg_id)

    if not prg:
        print(f"  [!] Error: Program '{prg_id}' not found.")
        return False

    confirm = prompt_confirm(
        f"Are you sure you want to permanently delete program '{prg.title}' ({prg.id})?",
        default_yes=False,
    )

    if confirm:
        programs.remove(prg)
        if storage.save_programs(programs):
            print(f"\n[OK] Program '{prg.id}' removed successfully.")
            return True
        else:
            print("\n[!] Error updating storage after deletion.")
            return False
    else:
        print("\nDeletion cancelled.")
        return False


def program_menu(programs: List[Program]) -> None:
    """Submenu loop for program management."""
    while True:
        print("\n" + "=" * 50)
        print(" PROGRAM & INTERNSHIP MANAGEMENT MENU".center(50))
        print("=" * 50)
        print("  1. View All Programs")
        print("  2. View Program Details")
        print("  3. Add New Program / Track")
        print("  4. Update Program")
        print("  5. Delete Program")
        print("  0. Back to Main Menu")
        print("-" * 50)

        choice = input("Select an option (0-5): ").strip()
        if choice == "1":
            display_programs_table(programs)
        elif choice == "2":
            view_program_details(programs)
        elif choice == "3":
            add_program(programs)
        elif choice == "4":
            update_program(programs)
        elif choice == "5":
            delete_program(programs)
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice. Please enter a number between 0 and 5.")
