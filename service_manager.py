"""
service_manager.py
------------------
Service management module for Veda Technology Business & Service Management System.

Handles:
- Listing and table formatting for digital services
- Viewing detailed specifications of a service
- Adding a new service with auto-generated ID and validation
- Modifying service attributes (name, category, description, price, status)
- Removing a service with safety confirmation
"""

from typing import List, Optional
from models import Service
from validators import (
    prompt_input,
    prompt_float,
    prompt_choice,
    prompt_confirm,
    validate_non_empty,
)
import storage


def display_services_table(services: List[Service], title: str = "VEDA TECHNOLOGY SERVICES") -> None:
    """Print a clean, tabular view of services.

    Args:
        services (list): List of Service objects to display.
        title (str): Header title for the table.
    """
    if not services:
        print("\n  [i] No services available to display.")
        return

    print("\n" + "=" * 90)
    print(f" {title.upper()} (Total: {len(services)})".center(90))
    print("=" * 90)
    header = f"{'ID':<9} {'Service Name':<34} {'Category':<22} {'Price (USD)':>12} {'Status':^9}"
    print(header)
    print("-" * 90)

    for s in services:
        name_trimmed = (s.name[:31] + "...") if len(s.name) > 34 else s.name
        cat_trimmed = (s.category[:19] + "...") if len(s.category) > 22 else s.category
        price_str = f"${s.price:,.2f}"
        print(f"{s.id:<9} {name_trimmed:<34} {cat_trimmed:<22} {price_str:>12} {s.status:^9}")

    print("=" * 90)


def find_service_by_id(services: List[Service], service_id: str) -> Optional[Service]:
    """Lookup a service by case-insensitive ID match.

    Args:
        services (list): List of Service objects.
        service_id (str): Service identifier.

    Returns:
        Service or None: The matching service if found.
    """
    service_id_clean = service_id.strip().upper()
    for srv in services:
        if srv.id.upper() == service_id_clean:
            return srv
    return None


def view_service_details(services: List[Service]) -> None:
    """Prompt the user for a service ID and show comprehensive details."""
    if not services:
        print("\n  [!] No services found in the system.")
        return

    srv_id = prompt_input("Enter Service ID to view (e.g., SRV-101)").upper()
    srv = find_service_by_id(services, srv_id)

    if not srv:
        print(f"  [!] Error: No service found with ID '{srv_id}'.")
        return

    print("\n" + "-" * 60)
    print(f" SERVICE DETAILS: {srv.id}".center(60))
    print("-" * 60)
    print(f"  Service ID   : {srv.id}")
    print(f"  Name         : {srv.name}")
    print(f"  Category     : {srv.category}")
    print(f"  Price (USD)  : ${srv.price:,.2f}")
    print(f"  Status       : {srv.status}")
    print(f"  Description  :\n    {srv.description}")
    print("-" * 60)


def add_service(services: List[Service]) -> Optional[Service]:
    """Interactive workflow to create and persist a new digital service.

    Args:
        services (list): Current list of services.

    Returns:
        Service: The newly created Service object, or None if aborted.
    """
    print("\n--- Add New Digital Service ---")
    new_id = storage.generate_service_id(services)
    print(f"Generated Service ID: {new_id}")

    name = prompt_input("Enter Service Name", validator_fn=validate_non_empty)

    categories = [
        "Web Development",
        "Mobile App Development",
        "Cloud Services",
        "Data Analytics",
        "AI & Machine Learning",
        "Cybersecurity",
        "Design & Creative",
        "Architecture",
        "Database",
        "Other",
    ]
    category = prompt_choice("Select Service Category:", categories)
    if category == "Other":
        category = prompt_input("Enter Custom Category Name", validator_fn=validate_non_empty)

    description = prompt_input("Enter Service Description", validator_fn=validate_non_empty)
    price = prompt_float("Enter Base Price in USD ($)", min_val=0.0)
    status = prompt_choice("Select Initial Status:", ["Active", "Inactive"], default="Active")

    new_service = Service(
        id=new_id,
        name=name,
        category=category,
        description=description,
        price=price,
        status=status,
    )

    services.append(new_service)
    if storage.save_services(services):
        print(f"\n[OK] Service '{new_service.name}' ({new_service.id}) added successfully!")
        return new_service
    else:
        print("\n[!] Error saving service to storage.")
        return None


def update_service(services: List[Service]) -> bool:
    """Interactive workflow to modify an existing service.

    Allows updating individual fields while keeping existing values by pressing Enter.
    """
    if not services:
        print("\n  [!] No services available to update.")
        return False

    srv_id = prompt_input("Enter Service ID to update (e.g., SRV-101)").upper()
    srv = find_service_by_id(services, srv_id)

    if not srv:
        print(f"  [!] Error: Service '{srv_id}' not found.")
        return False

    print(f"\nUpdating Service: {srv.id} - {srv.name}")
    print("(Press [Enter] to keep current value)\n")

    # Name
    new_name = prompt_input("Service Name", allow_blank=True, default=srv.name)
    srv.name = new_name

    # Category
    print(f"Current Category: {srv.category}")
    if prompt_confirm("Do you want to update category?", default_yes=False):
        categories = [
            "Web Development",
            "Mobile App Development",
            "Cloud Services",
            "Data Analytics",
            "AI & Machine Learning",
            "Cybersecurity",
            "Design & Creative",
            "Architecture",
            "Database",
            "Other",
        ]
        chosen_cat = prompt_choice("Choose New Category:", categories)
        if chosen_cat == "Other":
            chosen_cat = prompt_input("Enter Custom Category Name", validator_fn=validate_non_empty)
        srv.category = chosen_cat

    # Description
    new_desc = prompt_input("Description", allow_blank=True, default=srv.description)
    srv.description = new_desc

    # Price
    new_price = prompt_float("Base Price (USD)", min_val=0.0, default=srv.price)
    srv.price = new_price

    # Status
    new_status = prompt_choice("Operational Status:", ["Active", "Inactive"], default=srv.status)
    srv.status = new_status

    if storage.save_services(services):
        print(f"\n[OK] Service '{srv.id}' updated successfully!")
        return True
    else:
        print("\n[!] Error saving updated service.")
        return False


def delete_service(services: List[Service]) -> bool:
    """Remove a service after explicit user confirmation."""
    if not services:
        print("\n  [!] No services to delete.")
        return False

    srv_id = prompt_input("Enter Service ID to delete (e.g., SRV-101)").upper()
    srv = find_service_by_id(services, srv_id)

    if not srv:
        print(f"  [!] Error: Service '{srv_id}' not found.")
        return False

    confirm = prompt_confirm(
        f"Are you sure you want to permanently delete service '{srv.name}' ({srv.id})?",
        default_yes=False,
    )

    if confirm:
        services.remove(srv)
        if storage.save_services(services):
            print(f"\n[OK] Service '{srv.id}' removed successfully.")
            return True
        else:
            print("\n[!] Error updating storage after deletion.")
            return False
    else:
        print("\nDeletion cancelled.")
        return False


def service_menu(services: List[Service]) -> None:
    """Submenu loop for digital service operations."""
    while True:
        print("\n" + "=" * 50)
        print(" SERVICE MANAGEMENT MENU".center(50))
        print("=" * 50)
        print("  1. View All Services")
        print("  2. View Service Details")
        print("  3. Add New Service")
        print("  4. Update Service")
        print("  5. Delete Service")
        print("  0. Back to Main Menu")
        print("-" * 50)

        choice = input("Select an option (0-5): ").strip()
        if choice == "1":
            display_services_table(services)
        elif choice == "2":
            view_service_details(services)
        elif choice == "3":
            add_service(services)
        elif choice == "4":
            update_service(services)
        elif choice == "5":
            delete_service(services)
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice. Please enter a number between 0 and 5.")
