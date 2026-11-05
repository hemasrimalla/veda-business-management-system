"""
search_filter.py
----------------
Search and multi-criteria filtering module for Veda Technology
Business & Service Management System.

Capabilities:
- Services: search by keyword, filter by category, status, and price range.
- Programs: search by keyword, filter by type (Training/Internship/Technology),
  status, and fee range.
- Inquiries: search by keyword, filter by status, and filter by date range.
"""

from typing import List, Optional
from datetime import datetime
from models import Service, Program, Inquiry
from service_manager import display_services_table
from program_manager import display_programs_table
from inquiry_manager import display_inquiries_table
from validators import (
    prompt_input,
    prompt_float,
    prompt_choice,
    validate_date_format,
    validate_non_empty,
)


# =========================================================================
# Pure Filtering Functions for Services
# =========================================================================

def search_services(services: List[Service], keyword: str) -> List[Service]:
    """Search services across id, name, category, and description."""
    kw = keyword.strip().lower()
    if not kw:
        return list(services)
    return [
        s for s in services
        if kw in s.id.lower()
        or kw in s.name.lower()
        or kw in s.category.lower()
        or kw in s.description.lower()
    ]


def filter_services_by_category(services: List[Service], category: str) -> List[Service]:
    """Filter services by category (case-insensitive substring or exact)."""
    cat = category.strip().lower()
    return [s for s in services if cat in s.category.lower()]


def filter_services_by_status(services: List[Service], status: str) -> List[Service]:
    """Filter services by operational status ('Active' or 'Inactive')."""
    st = status.strip().lower()
    return [s for s in services if s.status.lower() == st]


def filter_services_by_price_range(
    services: List[Service],
    min_price: float = 0.0,
    max_price: Optional[float] = None,
) -> List[Service]:
    """Filter services within a specified price boundary."""
    results = []
    for s in services:
        if s.price >= min_price:
            if max_price is None or s.price <= max_price:
                results.append(s)
    return results


# =========================================================================
# Pure Filtering Functions for Programs
# =========================================================================

def search_programs(programs: List[Program], keyword: str) -> List[Program]:
    """Search programs by keyword in id, title, type, duration."""
    kw = keyword.strip().lower()
    if not kw:
        return list(programs)
    return [
        p for p in programs
        if kw in p.id.lower()
        or kw in p.title.lower()
        or kw in p.type.lower()
        or kw in p.duration.lower()
    ]


def filter_programs_by_type(programs: List[Program], prog_type: str) -> List[Program]:
    """Filter programs by track type ('Training', 'Internship', 'Technology')."""
    pt = prog_type.strip().lower()
    return [p for p in programs if p.type.lower() == pt]


def filter_programs_by_status(programs: List[Program], status: str) -> List[Program]:
    """Filter programs by enrollment status ('Open', 'Upcoming', 'Closed', 'Ongoing')."""
    st = status.strip().lower()
    return [p for p in programs if p.status.lower() == st]


def filter_programs_by_fee_range(
    programs: List[Program],
    min_fee: float = 0.0,
    max_fee: Optional[float] = None,
) -> List[Program]:
    """Filter programs within an enrollment fee boundary."""
    results = []
    for p in programs:
        if p.fee >= min_fee:
            if max_fee is None or p.fee <= max_fee:
                results.append(p)
    return results


# =========================================================================
# Pure Filtering Functions for Inquiries
# =========================================================================

def search_inquiries(inquiries: List[Inquiry], keyword: str) -> List[Inquiry]:
    """Search inquiries by keyword in id, customer_name, email, interest, message."""
    kw = keyword.strip().lower()
    if not kw:
        return list(inquiries)
    return [
        i for i in inquiries
        if kw in i.id.lower()
        or kw in i.customer_name.lower()
        or kw in i.email.lower()
        or kw in i.phone.lower()
        or kw in i.interest.lower()
        or kw in i.message.lower()
    ]


def filter_inquiries_by_status(inquiries: List[Inquiry], status: str) -> List[Inquiry]:
    """Filter inquiries by status ('New', 'In Progress', 'Resolved')."""
    st = status.strip().lower()
    return [i for i in inquiries if i.status.lower() == st]


def filter_inquiries_by_date_range(
    inquiries: List[Inquiry],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[Inquiry]:
    """Filter inquiries within a chronological date range (YYYY-MM-DD)."""
    results = []
    start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
    end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None

    for inq in inquiries:
        try:
            # Handle timestamps with hours/minutes or pure date
            inq_date_part = inq.date.split()[0]
            inq_dt = datetime.strptime(inq_date_part, "%Y-%m-%d")
            if start_dt and inq_dt < start_dt:
                continue
            if end_dt and inq_dt > end_dt:
                continue
            results.append(inq)
        except ValueError:
            results.append(inq)
    return results


# =========================================================================
# Interactive Search & Filter Submenus
# =========================================================================

def handle_service_search_filter(services: List[Service]) -> None:
    """Submenu for searching and filtering services."""
    while True:
        print("\n--- Search & Filter Digital Services ---")
        print("  1. Search by Keyword (Name, Category, Description)")
        print("  2. Filter by Category")
        print("  3. Filter by Status (Active / Inactive)")
        print("  4. Filter by Price Range")
        print("  0. Back to Search Menu")

        choice = input("Select an option (0-4): ").strip()
        if choice == "1":
            kw = prompt_input("Enter search keyword", validator_fn=validate_non_empty)
            res = search_services(services, kw)
            display_services_table(res, title=f"Services Matching '{kw}'")
        elif choice == "2":
            cats = sorted(list(set(s.category for s in services)))
            cat = prompt_choice("Select Category to Filter:", cats)
            res = filter_services_by_category(services, cat)
            display_services_table(res, title=f"Services in Category: {cat}")
        elif choice == "3":
            st = prompt_choice("Select Status to Filter:", ["Active", "Inactive"])
            res = filter_services_by_status(services, st)
            display_services_table(res, title=f"{st.capitalize()} Services")
        elif choice == "4":
            min_p = prompt_float("Minimum Price ($)", min_val=0.0, default=0.0)
            max_p = prompt_float("Maximum Price ($)", min_val=min_p, default=10000.0)
            res = filter_services_by_price_range(services, min_p, max_p)
            display_services_table(res, title=f"Services Priced Between ${min_p:,.2f} and ${max_p:,.2f}")
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice. Enter 0-4.")


def handle_program_search_filter(programs: List[Program]) -> None:
    """Submenu for searching and filtering programs."""
    while True:
        print("\n--- Search & Filter Programs & Internships ---")
        print("  1. Search by Keyword (Title, Duration)")
        print("  2. Filter by Track Type (Training / Internship / Technology)")
        print("  3. Filter by Status (Open / Upcoming / Closed / Ongoing)")
        print("  4. Filter by Enrollment Fee Range")
        print("  0. Back to Search Menu")

        choice = input("Select an option (0-4): ").strip()
        if choice == "1":
            kw = prompt_input("Enter search keyword", validator_fn=validate_non_empty)
            res = search_programs(programs, kw)
            display_programs_table(res, title=f"Programs Matching '{kw}'")
        elif choice == "2":
            pt = prompt_choice("Select Program Type:", ["Training", "Internship", "Technology"])
            res = filter_programs_by_type(programs, pt)
            display_programs_table(res, title=f"{pt} Programs")
        elif choice == "3":
            st = prompt_choice("Select Enrollment Status:", ["Open", "Upcoming", "Closed", "Ongoing"])
            res = filter_programs_by_status(programs, st)
            display_programs_table(res, title=f"{st} Programs")
        elif choice == "4":
            min_f = prompt_float("Minimum Fee ($)", min_val=0.0, default=0.0)
            max_f = prompt_float("Maximum Fee ($)", min_val=min_f, default=2000.0)
            res = filter_programs_by_fee_range(programs, min_f, max_f)
            display_programs_table(res, title=f"Programs with Fee Between ${min_f:,.2f} and ${max_f:,.2f}")
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice. Enter 0-4.")


def handle_inquiry_search_filter(inquiries: List[Inquiry]) -> None:
    """Submenu for searching and filtering inquiries."""
    while True:
        print("\n--- Search & Filter Customer Inquiries ---")
        print("  1. Search by Keyword (Name, Email, Interest, Message)")
        print("  2. Filter by Status (New / In Progress / Resolved)")
        print("  3. Filter by Date Range (YYYY-MM-DD)")
        print("  0. Back to Search Menu")

        choice = input("Select an option (0-3): ").strip()
        if choice == "1":
            kw = prompt_input("Enter search keyword", validator_fn=validate_non_empty)
            res = search_inquiries(inquiries, kw)
            display_inquiries_table(res, title=f"Inquiries Matching '{kw}'")
        elif choice == "2":
            st = prompt_choice("Select Status to Filter:", ["New", "In Progress", "Resolved"])
            res = filter_inquiries_by_status(inquiries, st)
            display_inquiries_table(res, title=f"Inquiries with Status '{st}'")
        elif choice == "3":
            start_d = prompt_input(
                "Enter Start Date (YYYY-MM-DD, or leave blank)",
                allow_blank=True,
                validator_fn=lambda d: not d or validate_date_format(d),
                error_message="Invalid date format. Use YYYY-MM-DD.",
            )
            end_d = prompt_input(
                "Enter End Date (YYYY-MM-DD, or leave blank)",
                allow_blank=True,
                validator_fn=lambda d: not d or validate_date_format(d),
                error_message="Invalid date format. Use YYYY-MM-DD.",
            )
            res = filter_inquiries_by_date_range(inquiries, start_d or None, end_d or None)
            lbl = f"Inquiries ({start_d or 'Earliest'} to {end_d or 'Latest'})"
            display_inquiries_table(res, title=lbl)
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice. Enter 0-3.")


def search_filter_menu(
    services: List[Service],
    programs: List[Program],
    inquiries: List[Inquiry],
) -> None:
    """Master search & filtering hub menu loop."""
    while True:
        print("\n" + "=" * 50)
        print(" SEARCH & FILTER HUB".center(50))
        print("=" * 50)
        print("  1. Search & Filter Digital Services")
        print("  2. Search & Filter Programs & Internships")
        print("  3. Search & Filter Customer Inquiries")
        print("  0. Back to Main Menu")
        print("-" * 50)

        choice = input("Select an option (0-3): ").strip()
        if choice == "1":
            handle_service_search_filter(services)
        elif choice == "2":
            handle_program_search_filter(programs)
        elif choice == "3":
            handle_inquiry_search_filter(inquiries)
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice. Enter 0-3.")
