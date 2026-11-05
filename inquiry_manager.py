"""
inquiry_manager.py
------------------
Customer and service inquiry management module for Veda Technology.

Handles:
- Logging prospective client inquiries with email and phone validation
- Tabular display of inquiries
- Deep inspection of inquiry requirements and chronological audit history
- Updating inquiry progress (New -> In Progress -> Resolved) with agent notes
- Removing inquiry records with confirmation
"""

from typing import List, Optional
from datetime import datetime
from models import Inquiry, Service, Program
from validators import (
    prompt_input,
    prompt_choice,
    prompt_confirm,
    validate_email,
    validate_phone,
    validate_non_empty,
    validate_date_format,
)
import storage


def display_inquiries_table(inquiries: List[Inquiry], title: str = "CUSTOMER & SERVICE INQUIRIES") -> None:
    """Print tabular listing of inquiries."""
    if not inquiries:
        print("\n  [i] No inquiries found.")
        return

    print("\n" + "=" * 98)
    print(f" {title.upper()} (Total: {len(inquiries)})".center(98))
    print("=" * 98)
    header = f"{'ID':<9} {'Customer Name':<20} {'Email':<25} {'Interest / Subject':<22} {'Date':<11} {'Status':^9}"
    print(header)
    print("-" * 98)

    for inq in inquiries:
        name_trimmed = (inq.customer_name[:17] + "...") if len(inq.customer_name) > 20 else inq.customer_name
        email_trimmed = (inq.email[:22] + "...") if len(inq.email) > 25 else inq.email
        interest_trimmed = (inq.interest[:19] + "...") if len(inq.interest) > 22 else inq.interest
        print(f"{inq.id:<9} {name_trimmed:<20} {email_trimmed:<25} {interest_trimmed:<22} {inq.date:<11} {inq.status:^9}")

    print("=" * 98)


def find_inquiry_by_id(inquiries: List[Inquiry], inquiry_id: str) -> Optional[Inquiry]:
    """Find an inquiry by case-insensitive ID."""
    clean_id = inquiry_id.strip().upper()
    for inq in inquiries:
        if inq.id.upper() == clean_id:
            return inq
    return None


def view_inquiry_details(inquiries: List[Inquiry]) -> None:
    """Display comprehensive inquiry information along with chronological history log."""
    if not inquiries:
        print("\n  [!] No inquiries available.")
        return

    inq_id = prompt_input("Enter Inquiry ID to view (e.g., INQ-301)").upper()
    inq = find_inquiry_by_id(inquiries, inq_id)

    if not inq:
        print(f"  [!] Error: No inquiry found with ID '{inq_id}'.")
        return

    print("\n" + "=" * 65)
    print(f" INQUIRY DETAILS: {inq.id}".center(65))
    print("=" * 65)
    print(f"  Inquiry ID     : {inq.id}")
    print(f"  Customer Name  : {inq.customer_name}")
    print(f"  Email Address  : {inq.email}")
    print(f"  Phone Number   : {inq.phone}")
    print(f"  Date Received  : {inq.date}")
    print(f"  Interest Target: {inq.interest}")
    print(f"  Current Status : {inq.status}")
    print(f"  Customer Query :\n    {inq.message}")
    print("-" * 65)
    print("  STATUS AUDIT & PROGRESS HISTORY:")
    if not inq.history:
        print("    (No history logged)")
    else:
        for idx, entry in enumerate(inq.history, 1):
            ts = entry.get("timestamp", "N/A")
            st = entry.get("status", "N/A")
            nt = entry.get("note", "")
            print(f"    [{idx}] {ts} | Status: {st:<11} | Note: {nt}")
    print("=" * 65)


def add_inquiry(
    inquiries: List[Inquiry],
    services: List[Service],
    programs: List[Program],
) -> Optional[Inquiry]:
    """Interactive workflow to record a new customer inquiry."""
    print("\n--- Record New Customer Inquiry ---")
    new_id = storage.generate_inquiry_id(inquiries)
    print(f"Generated Inquiry ID: {new_id}")

    name = prompt_input("Enter Customer Name", validator_fn=validate_non_empty)

    email = prompt_input(
        "Enter Customer Email Address",
        validator_fn=validate_email,
        error_message="Invalid email format (e.g., name@domain.com).",
    )

    phone = prompt_input(
        "Enter Customer Phone Number",
        validator_fn=validate_phone,
        error_message="Invalid phone format. Please enter 7 to 15 digits (e.g., +1-5551234567 or 9876543210).",
    )

    # Let user select from existing services/programs or type a custom topic
    print("\nSelect Interest Topic:")
    print("  1. Select from Active Services")
    print("  2. Select from Open Programs")
    print("  3. Enter Custom Requirement / Subject")
    mode = prompt_choice("Choose option:", ["Active Services", "Open Programs", "Custom Topic"])

    interest = ""
    if mode == "Active Services":
        active_services = [s.name for s in services if s.status == "Active"]
        if active_services:
            interest = prompt_choice("Select Service:", active_services)
        else:
            interest = prompt_input("No active services found. Enter service name", validator_fn=validate_non_empty)
    elif mode == "Open Programs":
        open_progs = [p.title for p in programs if p.status in ["Open", "Upcoming"]]
        if open_progs:
            interest = prompt_choice("Select Program:", open_progs)
        else:
            interest = prompt_input("No open programs found. Enter program title", validator_fn=validate_non_empty)
    else:
        interest = prompt_input("Enter Subject / Area of Interest", validator_fn=validate_non_empty)

    message = prompt_input("Enter Inquiry Message / Customer Requirements", validator_fn=validate_non_empty)

    # Date defaults to today's date
    today_str = datetime.now().strftime("%Y-%m-%d")
    date_val = prompt_input(
        f"Inquiry Date (YYYY-MM-DD)",
        validator_fn=validate_date_format,
        error_message="Date must be in valid YYYY-MM-DD format.",
        default=today_str,
    )

    status = prompt_choice("Initial Status:", ["New", "In Progress", "Resolved"], default="New")

    new_inquiry = Inquiry(
        id=new_id,
        customer_name=name,
        email=email,
        phone=phone,
        interest=interest,
        message=message,
        date=date_val,
        status=status,
    )

    inquiries.append(new_inquiry)
    if storage.save_inquiries(inquiries):
        print(f"\n[OK] Inquiry '{new_inquiry.id}' from '{new_inquiry.customer_name}' logged successfully!")
        return new_inquiry
    else:
        print("\n[!] Error saving inquiry to storage.")
        return None


def update_inquiry_status(inquiries: List[Inquiry]) -> bool:
    """Update inquiry workflow status and record notes in audit history."""
    if not inquiries:
        print("\n  [!] No inquiries available to update.")
        return False

    inq_id = prompt_input("Enter Inquiry ID to update (e.g., INQ-301)").upper()
    inq = find_inquiry_by_id(inquiries, inq_id)

    if not inq:
        print(f"  [!] Error: Inquiry '{inq_id}' not found.")
        return False

    print(f"\nInquiry Found: {inq.id} - {inq.customer_name} ({inq.interest})")
    print(f"Current Status: {inq.status}")

    new_status = prompt_choice(
        "Select New Status:",
        ["New", "In Progress", "Resolved"],
        default=inq.status,
    )

    note = prompt_input(
        "Enter Activity / Follow-Up Note",
        allow_blank=True,
        default=f"Status set to {new_status}",
    )

    inq.add_status_update(new_status, note)

    if storage.save_inquiries(inquiries):
        print(f"\n[OK] Inquiry '{inq.id}' status updated to '{new_status}' with audit note.")
        return True
    else:
        print("\n[!] Error saving updated inquiry status.")
        return False


def delete_inquiry(inquiries: List[Inquiry]) -> bool:
    """Delete an inquiry record after confirmation."""
    if not inquiries:
        print("\n  [!] No inquiries to delete.")
        return False

    inq_id = prompt_input("Enter Inquiry ID to delete (e.g., INQ-301)").upper()
    inq = find_inquiry_by_id(inquiries, inq_id)

    if not inq:
        print(f"  [!] Error: Inquiry '{inq_id}' not found.")
        return False

    confirm = prompt_confirm(
        f"Are you sure you want to permanently delete inquiry '{inq.id}' from '{inq.customer_name}'?",
        default_yes=False,
    )

    if confirm:
        inquiries.remove(inq)
        if storage.save_inquiries(inquiries):
            print(f"\n[OK] Inquiry '{inq.id}' deleted successfully.")
            return True
        else:
            print("\n[!] Error updating storage after inquiry deletion.")
            return False
    else:
        print("\nDeletion cancelled.")
        return False


def inquiry_menu(
    inquiries: List[Inquiry],
    services: List[Service],
    programs: List[Program],
) -> None:
    """Submenu loop for customer inquiries."""
    while True:
        print("\n" + "=" * 50)
        print(" CUSTOMER INQUIRY MANAGEMENT MENU".center(50))
        print("=" * 50)
        print("  1. View All Inquiries")
        print("  2. View Inquiry Details & History")
        print("  3. Record New Inquiry")
        print("  4. Update Inquiry Status & Add Note")
        print("  5. Delete Inquiry")
        print("  0. Back to Main Menu")
        print("-" * 50)

        choice = input("Select an option (0-5): ").strip()
        if choice == "1":
            display_inquiries_table(inquiries)
        elif choice == "2":
            view_inquiry_details(inquiries)
        elif choice == "3":
            add_inquiry(inquiries, services, programs)
        elif choice == "4":
            update_inquiry_status(inquiries)
        elif choice == "5":
            delete_inquiry(inquiries)
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice. Please enter a number between 0 and 5.")
