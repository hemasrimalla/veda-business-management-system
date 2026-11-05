# Veda Technology Business & Service Management System

A modular, beginner-friendly Python command-line application that simulates the core operations, service catalog, educational programs, and customer inquiry pipeline of **Veda Technology**—a digital services, cloud, and technical training enterprise.

Built entirely using the **Python Standard Library** (zero third-party dependencies required), this project showcases foundational Python software engineering practices:
- **Object-Oriented Programming (OOP)**: Domain models with encapsulation and serialization (`to_dict` / `from_dict`).
- **Separation of Concerns**: Modular decomposition across models, storage, validators, business managers, filtering, and reporting.
- **Robust Input Validation & Error Handling**: Email and phone regex patterns, date verification, numeric boundary checking, and defensive `try/except` recovery blocks.
- **Graceful Persistence & Auto-Healing**: Atomic JSON persistence with automatic synthetic seed data initialization and corrupted file recovery.
- **Business Intelligence**: KPI metrics calculation, inquiry workflow lifecycle management, pipeline valuation, and text report export.

---

## Table of Contents
1. [Overview & Business Context](#overview--business-context)
2. [Project Architecture & Structure](#project-architecture--structure)
3. [Key Features](#key-features)
4. [Domain Models](#domain-models)
5. [Prerequisites & Getting Started](#prerequisites--getting-started)
6. [Interactive Walkthrough & Usage](#interactive-walkthrough--usage)
7. [Search & Multi-Criteria Filtering](#search--multi-criteria-filtering)
8. [Business Reporting & Analytics](#business-reporting--analytics)
9. [Automated Testing](#automated-testing)
10. [Sample Output](#sample-output)
11. [Future Improvements](#future-improvements)

---

## Overview & Business Context

Veda Technology operates as a multi-vertical technology partner providing:
1. **Client Services**: Enterprise digital services including Custom Web Development, Mobile Engineering, Cloud Infrastructure, AI/LLM Integration, and Cybersecurity Audits.
2. **Talent & Learning Programs**: Professional technology tracks, career bootcamps, and subsidized student internships.
3. **Inquiry & CRM Pipeline**: Managing inbound client and student inquiries through status lifecycles (`New` -> `In Progress` -> `Resolved`) with timestamped audit trails.

This application provides operations staff and executives with a terminal-driven management dashboard to operate these business verticals without requiring external databases or heavy web frameworks.

---

## Project Architecture & Structure

```
veda-business-management-system/
├── .gitignore               # Ignores bytecode, caches, temp files, and virtual environments
├── README.md                # Comprehensive project documentation and user manual
├── main.py                  # Menu-driven entry point and master event loop
├── models.py                # OOP Domain models: Service, Program, Inquiry
├── service_manager.py       # CRUD operations and tabular display for digital services
├── program_manager.py       # Management for training, internship, and tech programs
├── inquiry_manager.py       # Customer inquiry tracking, audit history, and status updates
├── search_filter.py         # Multi-criteria keyword, category, price, and date filters
├── reports.py               # KPI analytics engine, revenue modeling, and text exporter
├── storage.py               # Atomic JSON persistence, seed data generator, and recovery
├── validators.py            # Regex validators (email, phone, dates) and re-prompting helpers
├── test_system.py           # Automated unit test suite verifying all modules
├── generate_sample_run.py   # Simulation harness generating sample output transcripts
├── data/
│   ├── services.json        # Pre-populated digital service catalog records
│   ├── programs.json        # Pre-populated training & internship program records
│   └── inquiries.json       # Pre-populated customer inquiry records with audit trails
└── sample_output/
    ├── business_report.txt  # Exported executive business intelligence report
    └── sample_run.txt       # Full terminal session transcript of the application
```

---

## Key Features

### 1. Digital Service Management (`service_manager.py`)
- View full service catalog in formatted, aligned tables.
- View detailed specifications (ID, Name, Category, Base Price, Status, Description).
- Add new digital services with auto-generated sequential IDs (`SRV-101`, `SRV-102`, ...).
- Update service attributes (supports pressing Enter to retain existing values).
- Delete obsolete services with confirmation prompts.

### 2. Program & Internship Management (`program_manager.py`)
- Manage 3 program tracks: **Training**, **Internship**, and **Technology**.
- Track durations (e.g., `12 Weeks`, `6 Months`), enrollment fees, seat capacities, and statuses (`Open`, `Upcoming`, `Closed`, `Ongoing`).
- View seat capacities and fee structures (free/sponsored tracks supported).
- Add, update, and delete programs with validated inputs.

### 3. Customer Inquiry Lifecycle & Audit History (`inquiry_manager.py`)
- Capture customer name, validated email address, validated phone number, topic of interest, requirements message, and date.
- Associate inquiries directly with active services or open programs, or record custom requirements.
- Progress workflow status: `New` -> `In Progress` -> `Resolved`.
- Append chronological audit notes with timestamps (e.g., proposal sent, scoping call completed).
- View full interaction history for any customer ticket.

### 4. Search & Multi-Criteria Filtering Hub (`search_filter.py`)
- **Services**:
  - Keyword search across ID, name, category, and description.
  - Category filtering (Web Dev, Cloud, Cybersecurity, AI/ML, etc.).
  - Operational status filtering (`Active` vs `Inactive`).
  - Price range boundary filtering (`min_price` to `max_price`).
- **Programs**:
  - Keyword search across ID, title, type, and duration.
  - Track type filtering (`Training`, `Internship`, `Technology`).
  - Status filtering (`Open`, `Upcoming`, `Closed`, `Ongoing`).
  - Fee range filtering.
- **Inquiries**:
  - Keyword search across customer name, email, topic, and message.
  - Status filtering (`New`, `In Progress`, `Resolved`).
  - Date range filtering (`YYYY-MM-DD` start and end boundaries).

### 5. Business Intelligence & Reporting (`reports.py`)
- **Executive Summary**: Service, program, and inquiry inventory counts with resolution rate percentage.
- **Program Distribution**: Seat allocation breakdown by track type and status.
- **Inquiry Pipeline**: Distribution across lifecycle stages (`New`, `In Progress`, `Resolved`).
- **Demand Analysis**: Ranked top 5 most-requested services and program topics.
- **Financial Opportunity Modeling**:
  - Baseline Active Service Catalog Value
  - Open Program Seat Tuition Potential
  - In-Flight Inquiries Pipeline Value
  - Total Estimated Business Valuation
- **Text File Export**: Export executive reports to formatted `.txt` files with timestamps.

### 6. Resilient Storage & Auto-Healing (`storage.py`)
- All records persist to human-readable JSON files in `data/`.
- **Automatic Initialization**: If `data/` or any JSON file is missing, the system automatically creates it and pre-populates 10 realistic synthetic records.
- **Corrupted File Recovery**: If a JSON file is damaged or corrupted, the system detects the syntax error, preserves the damaged file as a timestamped backup (`.corrupted_<timestamp>`), and restores clean default data without crashing.

### 7. Interactive Validation & User Experience (`validators.py`)
- Email validation using RFC-compliant regular expressions.
- International & local phone number validation (7 to 15 digits with optional `+` prefix).
- Strict calendar date format verification (`YYYY-MM-DD`).
- Safe numeric parsers (float price, integer seats) with custom ranges.
- Defensive prompt loops that display helpful error messages and re-prompt rather than crashing.

---

## Domain Models

### `Service`
```python
class Service:
    id: str           # e.g., 'SRV-101'
    name: str         # e.g., 'Custom Web Application Development'
    category: str     # e.g., 'Web Development'
    description: str  # Full scope description
    price: float      # Starting price in USD
    status: str       # 'Active' or 'Inactive'
```

### `Program`
```python
class Program:
    id: str           # e.g., 'PRG-201'
    title: str        # e.g., 'Full-Stack Web Development Bootcamp'
    type: str         # 'Training', 'Internship', or 'Technology'
    duration: str     # e.g., '12 Weeks'
    fee: float        # USD tuition (0.0 for free internships)
    seats: int        # Maximum participant capacity
    status: str       # 'Open', 'Upcoming', 'Closed', or 'Ongoing'
```

### `Inquiry`
```python
class Inquiry:
    id: str           # e.g., 'INQ-301'
    customer_name: str
    email: str
    phone: str
    interest: str     # Target service or program
    message: str      # Customer requirement text
    date: str         # 'YYYY-MM-DD'
    status: str       # 'New', 'In Progress', 'Resolved'
    history: list     # List of dicts: [{"timestamp": "...", "status": "...", "note": "..."}]
```

---

## Prerequisites & Getting Started

### Prerequisites
- Python 3.8 or higher (Tested on Python 3.14).
- No external packages or `pip install` commands needed!

### Running the Application
1. Open a terminal or PowerShell.
2. Navigate to the project directory:
   ```bash
   cd veda-business-management-system
   ```
3. Launch the application:
   ```bash
   python main.py
   ```

---

## Interactive Walkthrough & Usage

Upon launch, you will be greeted by the main navigation menu:

```text
======================================================================
      VEDA TECHNOLOGY BUSINESS & SERVICE MANAGEMENT SYSTEM
            Enterprise Digital Operations & Analytics
======================================================================
[i] Storage ready: 10 services, 10 programs, 10 inquiries loaded.

==================================================
               MAIN NAVIGATION MENU               
==================================================
  1. Digital Service Management
  2. Program & Internship Management
  3. Customer Inquiry Management
  4. Search & Multi-Criteria Filtering
  5. Business Analytics & Reports
  6. System Data Status & Reload
  7. Exit Application
==================================================
Select an option (1-7):
```

### Navigation Tips:
- Enter the number corresponding to your desired menu or submenu.
- Enter `0` in any submenu to return to the previous menu.
- When updating records, press **Enter** without typing to retain the current value.
- To safely interrupt or quit at any time, press `Ctrl+C` or choose option `7`.

---

## Business Reporting & Analytics

Choosing option `5` opens the **Business Analytics & Reports** hub:
- Option `1`: Displays the executive report on screen.
- Option `2`: Exports the report to a formatted text file (default: `sample_output/business_report_<timestamp>.txt`).
- Option `3`: Displays financial valuation metrics (Service Catalog Value, Program Tuition Capacity, and Inquiry Pipeline).
- Option `4`: Displays the most-requested service and training tracks based on inquiry data.

### Sample Business Report Snapshot:
```text
================================================================================
          VEDA TECHNOLOGY BUSINESS & SERVICE MANAGEMENT SYSTEM
                        EXECUTIVE BUSINESS REPORT
================================================================================
 Generated At : 2026-11-05 21:19:47
 Organization : Veda Technology Solutions Inc.
--------------------------------------------------------------------------------

1. EXECUTIVE SUMMARY & INVENTORY
   ----------------------------------------------------------------------
   * Total Digital Services Offered  : 10 (9 Active, 1 Inactive)
   * Total Educational Programs       : 10 (Capacity: 195 seats)
   * Active/Upcoming Seat Capacity    : 163 seats available
   * Total Customer Inquiries Logged  : 10
   * Inquiry Resolution Rate          : 20.0%

2. EDUCATIONAL & TRAINING PROGRAM BREAKDOWN
   ----------------------------------------------------------------------
   Distribution by Track Type:
     - Training        :  4 programs (110 seats total)
     - Internship      :  3 programs ( 30 seats total)
     - Technology      :  3 programs ( 55 seats total)
   Enrollment Status Breakdown:
     - Open            :  5 programs
     - Upcoming        :  3 programs
     - Closed          :  1 programs
     - Ongoing         :  1 programs

3. CUSTOMER INQUIRIES & WORKFLOW PIPELINE
   ----------------------------------------------------------------------
   * New Inquiries (Unassigned/Pending) :  4 (40.0%)
   * In Progress (Under Scoping/Review) :  4 (40.0%)
   * Resolved (Closed or Contracted)    :  2 (20.0%)

4. MOST REQUESTED SERVICES & PROGRAMS
   ----------------------------------------------------------------------
   Rank   Service / Program Topic                        Inquiries
   ---------------------------------------------------------------
   #1     Custom Web Application Development                     1
   #2     Cloud Infrastructure & DevOps Automation               1
   #3     Full-Stack Web Development Bootcamp                    1
   #4     Cybersecurity Audit & Penetration Testing              1
   #5     AI & Machine Learning Model Integration                1

5. REVENUE POTENTIAL & PIPELINE VALUATION
   ----------------------------------------------------------------------
   * Active Service Baseline Catalog Value : $   35,300.00
   * Open Program Tuition Capacity Value   : $  135,450.00
   * Active Inquiries Pipeline Value       : $   22,350.00
   --------------------------------------------------------------
   * Total Estimated Financial Opportunity : $  193,100.00

================================================================================
                       END OF BUSINESS REPORT
================================================================================
```

---

## Automated Testing

An automated unit test suite is provided in `test_system.py` covering:
- Seed data completeness (at least 8-10 records per file)
- Domain model dictionary serialization and deserialization
- Email and phone regex format validation
- Calendar date validation
- Automatic sequential ID generation
- Multi-criteria search and filter operations
- Report calculation formulas and file exporter

To run the test suite:
```bash
python test_system.py
```

Expected output:
```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.063s

OK
```

---

## Sample Output

The project includes pre-generated verified output assets in the `sample_output/` folder:
- **`sample_output/sample_run.txt`**: A complete, end-to-end terminal recording exercising all menu options, adding records, updating statuses, filtering records, and viewing analytics.
- **`sample_output/business_report.txt`**: The exported business intelligence report file.

You can also re-generate the sample run transcript anytime by executing:
```bash
python generate_sample_run.py
```

---

## Future Improvements

While this version provides a resilient command-line business system, future architectural extensions could include:
1. **Relational Database Migration**: Transitioning persistence from flat JSON files to SQLite or PostgreSQL via an ORM (such as SQLAlchemy).
2. **RESTful Web API**: Exposing endpoints using FastAPI or Flask to allow a React or Vue.js frontend to interact with the system.
3. **Role-Based Access Control (RBAC)**: Adding administrative authentication and sales agent roles with distinct permission levels.
4. **Email & SMS Notifications**: Integrating SMTP or Twilio APIs to automatically dispatch confirmation emails upon inquiry submission.
5. **PDF & Spreadsheet Export**: Generating professional PDF invoices and Excel financial sheets (`openpyxl` / `ReportLab`).

---

## License

Developed as part of the Veda Technology management initiative. Free for educational, evaluation, and commercial software training purposes.
