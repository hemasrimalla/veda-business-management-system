"""
storage.py
----------
JSON persistence and seed data initialization module for Veda Technology
Business & Service Management System.

Features:
- Safe loading and atomic saving of JSON datasets.
- Automatic creation of data directory and seed datasets if files are missing.
- Graceful recovery from corrupted files (creates a timestamped backup and re-initializes).
- ID generation helpers for Services, Programs, and Inquiries.
"""

import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any
from models import Service, Program, Inquiry

# Directory and file path definitions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

SERVICES_FILE = os.path.join(DATA_DIR, "services.json")
PROGRAMS_FILE = os.path.join(DATA_DIR, "programs.json")
INQUIRIES_FILE = os.path.join(DATA_DIR, "inquiries.json")


# -------------------------------------------------------------------------
# Synthetic Seed Data (Realistic Technology Business Records)
# -------------------------------------------------------------------------

SEED_SERVICES = [
    {
        "id": "SRV-101",
        "name": "Custom Web Application Development",
        "category": "Web Development",
        "description": "End-to-end full-stack web applications using modern React, Python FastAPI, and PostgreSQL.",
        "price": 3500.0,
        "status": "Active",
    },
    {
        "id": "SRV-102",
        "name": "Cross-Platform Mobile App Development",
        "category": "Mobile App Development",
        "description": "High-performance iOS and Android mobile apps built using Flutter and React Native.",
        "price": 4200.0,
        "status": "Active",
    },
    {
        "id": "SRV-103",
        "name": "Cloud Infrastructure & DevOps Automation",
        "category": "Cloud Services",
        "description": "Scalable cloud architectures on AWS/GCP with Terraform, Docker, and CI/CD pipelines.",
        "price": 2800.0,
        "status": "Active",
    },
    {
        "id": "SRV-104",
        "name": "Enterprise Data Analytics & BI Dashboards",
        "category": "Data Analytics",
        "description": "Data pipelines, ETL workflows, and interactive executive reporting dashboards.",
        "price": 3100.0,
        "status": "Active",
    },
    {
        "id": "SRV-105",
        "name": "AI & Machine Learning Model Integration",
        "category": "AI & Machine Learning",
        "description": "Custom LLM integrations, document retrieval agents, and predictive machine learning models.",
        "price": 5000.0,
        "status": "Active",
    },
    {
        "id": "SRV-106",
        "name": "Cybersecurity Audit & Penetration Testing",
        "category": "Cybersecurity",
        "description": "Vulnerability assessments, code audits, and infrastructure compliance hardening.",
        "price": 3800.0,
        "status": "Active",
    },
    {
        "id": "SRV-107",
        "name": "UI/UX Experience Design & Prototyping",
        "category": "Design & Creative",
        "description": "User research, wireframing, high-fidelity interactive Figma prototypes, and design systems.",
        "price": 2200.0,
        "status": "Active",
    },
    {
        "id": "SRV-108",
        "name": "API Design & Microservices Refactoring",
        "category": "Architecture",
        "description": "Decomposing legacy monoliths into resilient, decoupled RESTful and gRPC microservices.",
        "price": 4500.0,
        "status": "Active",
    },
    {
        "id": "SRV-109",
        "name": "Managed Database Optimization & Tuning",
        "category": "Database",
        "description": "Query performance profiling, indexing strategies, replication setup, and failover clustering.",
        "price": 1900.0,
        "status": "Inactive",
    },
    {
        "id": "SRV-110",
        "name": "Legacy System Migration & Modernization",
        "category": "Cloud Services",
        "description": "Seamless migration of on-premise systems to modern, scalable containerized cloud stacks.",
        "price": 6200.0,
        "status": "Active",
    },
]

SEED_PROGRAMS = [
    {
        "id": "PRG-201",
        "title": "Full-Stack Web Development Bootcamp",
        "type": "Training",
        "duration": "12 Weeks",
        "fee": 850.0,
        "seats": 35,
        "status": "Open",
    },
    {
        "id": "PRG-202",
        "title": "Data Science & Machine Learning Accelerator",
        "type": "Training",
        "duration": "10 Weeks",
        "fee": 950.0,
        "seats": 25,
        "status": "Open",
    },
    {
        "id": "PRG-203",
        "title": "Cloud Architecture & DevOps Professional",
        "type": "Training",
        "duration": "8 Weeks",
        "fee": 790.0,
        "seats": 30,
        "status": "Upcoming",
    },
    {
        "id": "PRG-204",
        "title": "Cybersecurity Defense & Ethical Hacking",
        "type": "Training",
        "duration": "8 Weeks",
        "fee": 820.0,
        "seats": 20,
        "status": "Open",
    },
    {
        "id": "PRG-205",
        "title": "Software Development Engineering (SDE) Intern",
        "type": "Internship",
        "duration": "6 Months",
        "fee": 0.0,
        "seats": 12,
        "status": "Open",
    },
    {
        "id": "PRG-206",
        "title": "AI & Deep Learning Research Intern",
        "type": "Internship",
        "duration": "3 Months",
        "fee": 0.0,
        "seats": 8,
        "status": "Upcoming",
    },
    {
        "id": "PRG-207",
        "title": "UI/UX Product Design Internship",
        "type": "Internship",
        "duration": "4 Months",
        "fee": 0.0,
        "seats": 10,
        "status": "Closed",
    },
    {
        "id": "PRG-208",
        "title": "Enterprise Kubernetes & Microservices Immersion",
        "type": "Technology",
        "duration": "6 Weeks",
        "fee": 1200.0,
        "seats": 18,
        "status": "Open",
    },
    {
        "id": "PRG-209",
        "title": "Generative AI Application Engineering",
        "type": "Technology",
        "duration": "4 Weeks",
        "fee": 1100.0,
        "seats": 22,
        "status": "Ongoing",
    },
    {
        "id": "PRG-210",
        "title": "Distributed Systems & High-Load Architecture",
        "type": "Technology",
        "duration": "5 Weeks",
        "fee": 1350.0,
        "seats": 15,
        "status": "Upcoming",
    },
]

SEED_INQUIRIES = [
    {
        "id": "INQ-301",
        "customer_name": "Aarav Sharma",
        "email": "aarav.sharma@techcorp.in",
        "phone": "+91-9876543210",
        "interest": "Custom Web Application Development",
        "message": "We need a custom B2B SaaS portal with client onboarding and billing integration.",
        "date": "2026-10-15",
        "status": "Resolved",
        "history": [
            {"timestamp": "2026-10-15 10:30", "status": "New", "note": "Inquiry recorded from web portal."},
            {"timestamp": "2026-10-16 14:00", "status": "In Progress", "note": "Requirement scoping call completed."},
            {"timestamp": "2026-10-20 16:45", "status": "Resolved", "note": "Contract signed and handed to delivery team."}
        ],
    },
    {
        "id": "INQ-302",
        "customer_name": "Priya Patel",
        "email": "priya.patel@innovate.org",
        "phone": "+91-9123456780",
        "interest": "Cloud Infrastructure & DevOps Automation",
        "message": "Looking to migrate our AWS infrastructure to Terraform with automated CI/CD.",
        "date": "2026-10-22",
        "status": "In Progress",
        "history": [
            {"timestamp": "2026-10-22 11:15", "status": "New", "note": "Inquiry received via partner referral."},
            {"timestamp": "2026-10-24 09:30", "status": "In Progress", "note": "Shared cloud architectural assessment proposal."}
        ],
    },
    {
        "id": "INQ-303",
        "customer_name": "Rohit Verma",
        "email": "rohit.verma@gmail.com",
        "phone": "+91-9811223344",
        "interest": "Full-Stack Web Development Bootcamp",
        "message": "Inquiring about weekend cohort schedule and payment installment plans.",
        "date": "2026-10-28",
        "status": "New",
        "history": [
            {"timestamp": "2026-10-28 17:20", "status": "New", "note": "Applicant submitted online course inquiry."}
        ],
    },
    {
        "id": "INQ-304",
        "customer_name": "Ananya Iyer",
        "email": "ananya.iyer@fintechsol.com",
        "phone": "+91-9988776655",
        "interest": "Cybersecurity Audit & Penetration Testing",
        "message": "Require urgent ISO 27001 vulnerability audit and web app penetration testing.",
        "date": "2026-11-01",
        "status": "In Progress",
        "history": [
            {"timestamp": "2026-11-01 13:40", "status": "New", "note": "Inbound corporate audit inquiry."},
            {"timestamp": "2026-11-02 11:00", "status": "In Progress", "note": "NDA signed; testing environment access being provisioned."}
        ],
    },
    {
        "id": "INQ-305",
        "customer_name": "David Miller",
        "email": "david.miller@apexglobal.com",
        "phone": "+1-4155552671",
        "interest": "AI & Machine Learning Model Integration",
        "message": "Interested in deploying internal document retrieval LLMs with role-based access control.",
        "date": "2026-11-02",
        "status": "New",
        "history": [
            {"timestamp": "2026-11-02 09:10", "status": "New", "note": "Inquiry submitted by CTO office."}
        ],
    },
    {
        "id": "INQ-306",
        "customer_name": "Meera Nair",
        "email": "meera.nair@student.edu",
        "phone": "+91-9744112233",
        "interest": "Software Development Engineering (SDE) Intern",
        "message": "Applying for the 6-month SDE internship. Final year CS undergraduate with React/Django experience.",
        "date": "2026-11-03",
        "status": "New",
        "history": [
            {"timestamp": "2026-11-03 14:15", "status": "New", "note": "Resume and GitHub portfolio received."}
        ],
    },
    {
        "id": "INQ-307",
        "customer_name": "Vikram Malhotra",
        "email": "vikram.m@retailx.io",
        "phone": "+91-9833445566",
        "interest": "Enterprise Data Analytics & BI Dashboards",
        "message": "Need help integrating our Shopify, warehouse, and CRM data into a centralized Snowflake & PowerBI setup.",
        "date": "2026-11-03",
        "status": "In Progress",
        "history": [
            {"timestamp": "2026-11-03 16:50", "status": "New", "note": "Retail analytics inquiry created."},
            {"timestamp": "2026-11-04 15:30", "status": "In Progress", "note": "Data schema review meeting conducted."}
        ],
    },
    {
        "id": "INQ-308",
        "customer_name": "Sophie Zhang",
        "email": "sophie.zhang@designlab.ca",
        "phone": "+1-6045558912",
        "interest": "UI/UX Experience Design & Prototyping",
        "message": "Looking for a complete redesign of our mobile health tracking application in Figma.",
        "date": "2026-11-04",
        "status": "New",
        "history": [
            {"timestamp": "2026-11-04 18:05", "status": "New", "note": "Client design brief received."}
        ],
    },
    {
        "id": "INQ-309",
        "customer_name": "Arjun Rao",
        "email": "arjun.rao@startupnexus.com",
        "phone": "+91-9900112233",
        "interest": "Generative AI Application Engineering",
        "message": "Can our engineering team of 5 enroll as a corporate batch? Seeking group discount details.",
        "date": "2026-11-04",
        "status": "In Progress",
        "history": [
            {"timestamp": "2026-11-04 19:40", "status": "New", "note": "Corporate batch discount requested."},
            {"timestamp": "2026-11-05 10:15", "status": "In Progress", "note": "Corporate quotation delivered to HR."}
        ],
    },
    {
        "id": "INQ-310",
        "customer_name": "Sneha Kulkarni",
        "email": "sneha.k@academix.in",
        "phone": "+91-9655443322",
        "interest": "Data Science & Machine Learning Accelerator",
        "message": "Would like to review the syllabus regarding deep learning and PyTorch modules.",
        "date": "2026-11-05",
        "status": "Resolved",
        "history": [
            {"timestamp": "2026-11-05 08:30", "status": "New", "note": "Curriculum inquiry registered."},
            {"timestamp": "2026-11-05 12:00", "status": "Resolved", "note": "Detailed syllabus sent; student enrolled in upcoming batch."}
        ],
    },
]


# -------------------------------------------------------------------------
# Storage Functions & Graceful Recovery
# -------------------------------------------------------------------------

def ensure_data_directory() -> None:
    """Ensure that the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_raw_json(filepath: str, default_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Safely read and parse a JSON file.

    If file does not exist, writes the default_data and returns it.
    If the file is empty or corrupted, creates a backup and resets with default_data.
    """
    ensure_data_directory()
    if not os.path.exists(filepath):
        _save_raw_json(filepath, default_data)
        return default_data

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                # File is empty; write default data
                _save_raw_json(filepath, default_data)
                return default_data
            data = json.loads(content)
            if not isinstance(data, list):
                raise ValueError("JSON root element must be a list.")
            return data
    except (json.JSONDecodeError, ValueError) as err:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{filepath}.corrupted_{timestamp}"
        try:
            shutil.copyfile(filepath, backup_path)
            print(f"\n[!] Warning: Corrupted data detected in '{filepath}'.")
            print(f"    Backup preserved at: '{backup_path}'.")
            print("    Restoring defaults to maintain system integrity...")
        except Exception:
            pass
        _save_raw_json(filepath, default_data)
        return default_data


def _save_raw_json(filepath: str, data: List[Dict[str, Any]]) -> bool:
    """Atomically write Python data structure to a formatted JSON file."""
    ensure_data_directory()
    temp_path = f"{filepath}.tmp"
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        # Atomic replace
        os.replace(temp_path, filepath)
        return True
    except Exception as e:
        print(f"[!] Storage Error while saving '{filepath}': {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False


def initialize_storage() -> None:
    """Check all data files and pre-populate missing or empty files with synthetic records."""
    ensure_data_directory()
    if not os.path.exists(SERVICES_FILE):
        _save_raw_json(SERVICES_FILE, SEED_SERVICES)
    if not os.path.exists(PROGRAMS_FILE):
        _save_raw_json(PROGRAMS_FILE, SEED_PROGRAMS)
    if not os.path.exists(INQUIRIES_FILE):
        _save_raw_json(INQUIRIES_FILE, SEED_INQUIRIES)


# -------------------------------------------------------------------------
# Typed Entity Loaders and Savers
# -------------------------------------------------------------------------

def load_services() -> List[Service]:
    """Load all services from JSON storage into Service domain objects."""
    raw_list = _load_raw_json(SERVICES_FILE, SEED_SERVICES)
    services: List[Service] = []
    for item in raw_list:
        try:
            services.append(Service.from_dict(item))
        except Exception as e:
            print(f"[!] Warning: Skipped invalid service record {item}: {e}")
    return services


def save_services(services: List[Service]) -> bool:
    """Save a list of Service domain objects to JSON storage."""
    raw_list = [srv.to_dict() for srv in services]
    return _save_raw_json(SERVICES_FILE, raw_list)


def load_programs() -> List[Program]:
    """Load all programs from JSON storage into Program domain objects."""
    raw_list = _load_raw_json(PROGRAMS_FILE, SEED_PROGRAMS)
    programs: List[Program] = []
    for item in raw_list:
        try:
            programs.append(Program.from_dict(item))
        except Exception as e:
            print(f"[!] Warning: Skipped invalid program record {item}: {e}")
    return programs


def save_programs(programs: List[Program]) -> bool:
    """Save a list of Program domain objects to JSON storage."""
    raw_list = [prg.to_dict() for prg in programs]
    return _save_raw_json(PROGRAMS_FILE, raw_list)


def load_inquiries() -> List[Inquiry]:
    """Load all inquiries from JSON storage into Inquiry domain objects."""
    raw_list = _load_raw_json(INQUIRIES_FILE, SEED_INQUIRIES)
    inquiries: List[Inquiry] = []
    for item in raw_list:
        try:
            inquiries.append(Inquiry.from_dict(item))
        except Exception as e:
            print(f"[!] Warning: Skipped invalid inquiry record {item}: {e}")
    return inquiries


def save_inquiries(inquiries: List[Inquiry]) -> bool:
    """Save a list of Inquiry domain objects to JSON storage."""
    raw_list = [inq.to_dict() for inq in inquiries]
    return _save_raw_json(INQUIRIES_FILE, raw_list)


# -------------------------------------------------------------------------
# ID Generation Utilities
# -------------------------------------------------------------------------

def generate_service_id(services: List[Service]) -> str:
    """Generate the next sequential service ID (e.g. SRV-111)."""
    max_num = 100
    for srv in services:
        if srv.id.startswith("SRV-"):
            try:
                num = int(srv.id.split("-")[1])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
    return f"SRV-{max_num + 1}"


def generate_program_id(programs: List[Program]) -> str:
    """Generate the next sequential program ID (e.g. PRG-211)."""
    max_num = 200
    for prg in programs:
        if prg.id.startswith("PRG-"):
            try:
                num = int(prg.id.split("-")[1])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
    return f"PRG-{max_num + 1}"


def generate_inquiry_id(inquiries: List[Inquiry]) -> str:
    """Generate the next sequential inquiry ID (e.g. INQ-311)."""
    max_num = 300
    for inq in inquiries:
        if inq.id.startswith("INQ-"):
            try:
                num = int(inq.id.split("-")[1])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
    return f"INQ-{max_num + 1}"
