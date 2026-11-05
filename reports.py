"""
reports.py
----------
Business intelligence and reporting module for Veda Technology
Business & Service Management System.

Calculates key performance indicators (KPIs):
- Inventory of Services and active status ratios
- Program distribution by track type and seat capacity
- Inquiry status metrics and resolution rates
- Most requested services/topics
- Financial revenue potential summary (Service catalog value, program seat revenue)

Allows rendering reports to stdout and exporting to a formatted text file.
"""

import os
from collections import Counter
from datetime import datetime
from typing import List, Dict, Any, Tuple
from models import Service, Program, Inquiry
from validators import prompt_confirm, prompt_input


def calculate_metrics(
    services: List[Service],
    programs: List[Program],
    inquiries: List[Inquiry],
) -> Dict[str, Any]:
    """Calculate operational KPIs and business summaries from the dataset.

    Returns:
        dict: Aggregated dictionary of metrics.
    """
    total_services = len(services)
    active_services = sum(1 for s in services if s.status == "Active")
    inactive_services = total_services - active_services
    active_service_catalog_value = sum(s.price for s in services if s.status == "Active")

    total_programs = len(programs)
    programs_by_type = Counter(p.type for p in programs)
    programs_by_status = Counter(p.status for p in programs)
    total_seats = sum(p.seats for p in programs)
    open_seats = sum(p.seats for p in programs if p.status in ["Open", "Upcoming"])

    # Program potential tuition revenue (seats * fee for open/upcoming programs)
    program_revenue_potential = sum(
        p.seats * p.fee for p in programs if p.status in ["Open", "Upcoming"]
    )

    total_inquiries = len(inquiries)
    inquiries_by_status = Counter(i.status for i in inquiries)
    new_inq = inquiries_by_status.get("New", 0)
    in_prog_inq = inquiries_by_status.get("In Progress", 0)
    resolved_inq = inquiries_by_status.get("Resolved", 0)
    resolution_rate = (resolved_inq / total_inquiries * 100) if total_inquiries > 0 else 0.0

    # Most requested interests / services
    interest_counter = Counter(i.interest for i in inquiries)
    top_interests = interest_counter.most_common(5)

    # Estimate inquiry pipeline revenue:
    # Match active service prices to open inquiries (New or In Progress)
    service_price_map = {s.name.lower(): s.price for s in services}
    program_fee_map = {p.title.lower(): p.fee for p in programs}

    inquiry_pipeline_value = 0.0
    for inq in inquiries:
        if inq.status in ["New", "In Progress"]:
            inq_key = inq.interest.lower()
            if inq_key in service_price_map:
                inquiry_pipeline_value += service_price_map[inq_key]
            elif inq_key in program_fee_map:
                inquiry_pipeline_value += program_fee_map[inq_key]

    return {
        "total_services": total_services,
        "active_services": active_services,
        "inactive_services": inactive_services,
        "active_service_catalog_value": active_service_catalog_value,
        "total_programs": total_programs,
        "programs_by_type": programs_by_type,
        "programs_by_status": programs_by_status,
        "total_seats": total_seats,
        "open_seats": open_seats,
        "program_revenue_potential": program_revenue_potential,
        "total_inquiries": total_inquiries,
        "inquiries_by_status": inquiries_by_status,
        "new_inq": new_inq,
        "in_prog_inq": in_prog_inq,
        "resolved_inq": resolved_inq,
        "resolution_rate": resolution_rate,
        "top_interests": top_interests,
        "inquiry_pipeline_value": inquiry_pipeline_value,
    }


def generate_report_text(
    services: List[Service],
    programs: List[Program],
    inquiries: List[Inquiry],
) -> str:
    """Compile a comprehensive, formatted business performance report string."""
    m = calculate_metrics(services, programs, inquiries)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = []
    lines.append("=" * 80)
    lines.append("          VEDA TECHNOLOGY BUSINESS & SERVICE MANAGEMENT SYSTEM")
    lines.append("                        EXECUTIVE BUSINESS REPORT")
    lines.append("=" * 80)
    lines.append(f" Generated At : {now_str}")
    lines.append(f" Organization : Veda Technology Solutions Inc.")
    lines.append("-" * 80)
    lines.append("")

    # Section 1: Executive KPI Summary
    lines.append("1. EXECUTIVE SUMMARY & INVENTORY")
    lines.append("   " + "-" * 70)
    lines.append(f"   * Total Digital Services Offered  : {m['total_services']} ({m['active_services']} Active, {m['inactive_services']} Inactive)")
    lines.append(f"   * Total Educational Programs       : {m['total_programs']} (Capacity: {m['total_seats']} seats)")
    lines.append(f"   * Active/Upcoming Seat Capacity    : {m['open_seats']} seats available")
    lines.append(f"   * Total Customer Inquiries Logged  : {m['total_inquiries']}")
    lines.append(f"   * Inquiry Resolution Rate          : {m['resolution_rate']:.1f}%")
    lines.append("")

    # Section 2: Program Breakdown
    lines.append("2. EDUCATIONAL & TRAINING PROGRAM BREAKDOWN")
    lines.append("   " + "-" * 70)
    lines.append("   Distribution by Track Type:")
    for track, count in m["programs_by_type"].items():
        seats_in_track = sum(p.seats for p in programs if p.type == track)
        lines.append(f"     - {track:<16}: {count:>2} programs ({seats_in_track:>3} seats total)")
    lines.append("   Enrollment Status Breakdown:")
    for status, count in m["programs_by_status"].items():
        lines.append(f"     - {status:<16}: {count:>2} programs")
    lines.append("")

    # Section 3: Customer Inquiry Distribution
    lines.append("3. CUSTOMER INQUIRIES & WORKFLOW PIPELINE")
    lines.append("   " + "-" * 70)
    lines.append(f"   * New Inquiries (Unassigned/Pending) : {m['new_inq']:>2} ({m['new_inq']/max(m['total_inquiries'],1)*100:4.1f}%)")
    lines.append(f"   * In Progress (Under Scoping/Review) : {m['in_prog_inq']:>2} ({m['in_prog_inq']/max(m['total_inquiries'],1)*100:4.1f}%)")
    lines.append(f"   * Resolved (Closed or Contracted)    : {m['resolved_inq']:>2} ({m['resolved_inq']/max(m['total_inquiries'],1)*100:4.1f}%)")
    lines.append("")

    # Section 4: Demand Analysis
    lines.append("4. MOST REQUESTED SERVICES & PROGRAMS")
    lines.append("   " + "-" * 70)
    if not m["top_interests"]:
        lines.append("   (No inquiry demand records available)")
    else:
        lines.append(f"   {'Rank':<6} {'Service / Program Topic':<45} {'Inquiries':>10}")
        lines.append("   " + "-" * 63)
        for rank, (topic, count) in enumerate(m["top_interests"], 1):
            topic_disp = (topic[:42] + "...") if len(topic) > 45 else topic
            lines.append(f"   #{rank:<5} {topic_disp:<45} {count:>10}")
    lines.append("")

    # Section 5: Revenue & Financial Potential
    lines.append("5. REVENUE POTENTIAL & PIPELINE VALUATION")
    lines.append("   " + "-" * 70)
    lines.append(f"   * Active Service Baseline Catalog Value : ${m['active_service_catalog_value']:>12,.2f}")
    lines.append(f"   * Open Program Tuition Capacity Value   : ${m['program_revenue_potential']:>12,.2f}")
    lines.append(f"   * Active Inquiries Pipeline Value       : ${m['inquiry_pipeline_value']:>12,.2f}")
    total_est = m['active_service_catalog_value'] + m['program_revenue_potential'] + m['inquiry_pipeline_value']
    lines.append(f"   --------------------------------------------------------------")
    lines.append(f"   * Total Estimated Financial Opportunity : ${total_est:>12,.2f}")
    lines.append("")
    lines.append("=" * 80)
    lines.append("                       END OF BUSINESS REPORT")
    lines.append("=" * 80)

    return "\n".join(lines)


def export_report_to_file(
    report_content: str,
    target_path: str,
) -> bool:
    """Save the generated report text to disk."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(target_path)), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        return True
    except Exception as e:
        print(f"[!] Error exporting report to '{target_path}': {e}")
        return False


def reports_menu(
    services: List[Service],
    programs: List[Program],
    inquiries: List[Inquiry],
) -> None:
    """Submenu for viewing and exporting business intelligence reports."""
    while True:
        print("\n" + "=" * 50)
        print(" BUSINESS ANALYTICS & REPORTS".center(50))
        print("=" * 50)
        print("  1. View Executive Business Report (Console)")
        print("  2. Export Executive Report to Text File")
        print("  3. View Revenue Potential Summary")
        print("  4. View Most Requested Services / Topics")
        print("  0. Back to Main Menu")
        print("-" * 50)

        choice = input("Select an option (0-4): ").strip()
        if choice == "1":
            report_text = generate_report_text(services, programs, inquiries)
            print("\n" + report_text)
        elif choice == "2":
            report_text = generate_report_text(services, programs, inquiries)
            default_fn = f"business_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            base_dir = os.path.dirname(os.path.abspath(__file__))
            default_path = os.path.join(base_dir, "sample_output", default_fn)
            export_path = prompt_input(
                f"Enter export file path",
                default=default_path,
            )
            if export_report_to_file(report_text, export_path):
                print(f"\n[OK] Executive report exported successfully to:\n    {export_path}")
        elif choice == "3":
            m = calculate_metrics(services, programs, inquiries)
            print("\n" + "-" * 55)
            print(" REVENUE POTENTIAL SUMMARY".center(55))
            print("-" * 55)
            print(f"  Active Service Catalog Value : ${m['active_service_catalog_value']:>12,.2f}")
            print(f"  Program Tuition Capacity     : ${m['program_revenue_potential']:>12,.2f}")
            print(f"  Unresolved Inquiries Pipeline: ${m['inquiry_pipeline_value']:>12,.2f}")
            total_pot = m['active_service_catalog_value'] + m['program_revenue_potential'] + m['inquiry_pipeline_value']
            print("  " + "-" * 45)
            print(f"  Total Business Value         : ${total_pot:>12,.2f}")
            print("-" * 55)
        elif choice == "4":
            m = calculate_metrics(services, programs, inquiries)
            print("\n" + "-" * 55)
            print(" TOP REQUESTED SERVICES & PROGRAMS".center(55))
            print("-" * 55)
            if not m["top_interests"]:
                print("  No inquiries logged yet.")
            else:
                for idx, (topic, cnt) in enumerate(m["top_interests"], 1):
                    print(f"  {idx}. {topic} ({cnt} inquiries)")
            print("-" * 55)
        elif choice == "0":
            break
        else:
            print("  [!] Invalid choice. Enter 0-4.")
