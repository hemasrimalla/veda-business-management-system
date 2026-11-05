"""
main.py
-------
Entry point for the Veda Technology Business & Service Management System.

A modular, menu-driven CLI application simulating the business operations,
service offerings, training and internship programs, and customer inquiry
lifecycle of Veda Technology.

Run:
    python main.py
"""

import sys
import os

# Ensure local modules can be imported directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import storage
from service_manager import service_menu
from program_manager import program_menu
from inquiry_manager import inquiry_menu
from search_filter import search_filter_menu
from reports import reports_menu
from validators import prompt_confirm


def print_banner() -> None:
    """Print the startup branding banner."""
    print("\n" + "=" * 70)
    print("      VEDA TECHNOLOGY BUSINESS & SERVICE MANAGEMENT SYSTEM")
    print("            Enterprise Digital Operations & Analytics")
    print("=" * 70)
    print(" Welcome! Manage services, programs, inquiries, search, and reports.")
    print("=" * 70)


def display_system_status(services, programs, inquiries) -> None:
    """Display real-time record counts and data persistence paths."""
    print("\n" + "=" * 60)
    print(" SYSTEM STORAGE & DATA STATUS".center(60))
    print("=" * 60)
    print(f"  Storage Directory : {storage.DATA_DIR}")
    print(f"  Services Loaded   : {len(services)} records (File: services.json)")
    print(f"  Programs Loaded   : {len(programs)} records (File: programs.json)")
    print(f"  Inquiries Loaded  : {len(inquiries)} records (File: inquiries.json)")
    print("-" * 60)

    if prompt_confirm("Do you want to re-load datasets from disk?", default_yes=False):
        services.clear()
        services.extend(storage.load_services())
        programs.clear()
        programs.extend(storage.load_programs())
        inquiries.clear()
        inquiries.extend(storage.load_inquiries())
        print("  [OK] Datasets successfully reloaded from disk.")


def main() -> None:
    """Main program execution loop."""
    print_banner()

    # Step 1: Initialize storage and ensure seed files exist
    storage.initialize_storage()

    # Step 2: Load current datasets into in-memory object collections
    services = storage.load_services()
    programs = storage.load_programs()
    inquiries = storage.load_inquiries()

    print(f"[i] Storage ready: {len(services)} services, {len(programs)} programs, {len(inquiries)} inquiries loaded.\n")

    # Step 3: Main application loop
    while True:
        try:
            print("\n" + "=" * 50)
            print(" MAIN NAVIGATION MENU".center(50))
            print("=" * 50)
            print("  1. Digital Service Management")
            print("  2. Program & Internship Management")
            print("  3. Customer Inquiry Management")
            print("  4. Search & Multi-Criteria Filtering")
            print("  5. Business Analytics & Reports")
            print("  6. System Data Status & Reload")
            print("  7. Exit Application")
            print("=" * 50)

            choice = input("Select an option (1-7): ").strip()

            if choice == "1":
                service_menu(services)
            elif choice == "2":
                program_menu(programs)
            elif choice == "3":
                inquiry_menu(inquiries, services, programs)
            elif choice == "4":
                search_filter_menu(services, programs, inquiries)
            elif choice == "5":
                reports_menu(services, programs, inquiries)
            elif choice == "6":
                display_system_status(services, programs, inquiries)
            elif choice == "7":
                print("\n" + "=" * 60)
                print(" Thank you for using Veda Technology Management System!")
                print(" Have a productive day ahead. Goodbye.")
                print("=" * 60 + "\n")
                break
            else:
                print("  [!] Invalid choice. Please enter a number between 1 and 7.")

        except (KeyboardInterrupt, EOFError):
            print("\n\n[!] Session interrupted by user. Exiting cleanly. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n[!] Unexpected Error: {e}")
            print("    Returning to main menu safely...\n")


if __name__ == "__main__":
    main()
