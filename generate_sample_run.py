"""
generate_sample_run.py
----------------------
Script to run main.py interactively via standard input, exercising each feature
and writing a clean, realistic sample run transcript to sample_output/sample_run.txt.
"""

import subprocess
import sys
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_PY = os.path.join(PROJECT_DIR, "main.py")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "sample_output", "sample_run.txt")

# Define a scripted series of user inputs:
# 1 -> Service Management:
#   1 -> View All Services
#   2 -> View Service Details -> SRV-101
#   3 -> Add New Service -> Blockchain Smart Contract Auditing -> 6 (Cybersecurity) -> Thorough security audit of EVM smart contracts. -> 4800.0 -> 1 (Active)
#   0 -> Back
# 2 -> Program Management:
#   1 -> View All Programs
#   2 -> View Program Details -> PRG-201
#   3 -> Add New Program -> Autonomous AI Agents Workshop -> 3 (Technology) -> 4 Weeks -> 1150.0 -> 25 -> 1 (Open)
#   0 -> Back
# 3 -> Customer Inquiry Management:
#   1 -> View All Inquiries
#   2 -> View Inquiry Details -> INQ-301
#   3 -> Record New Inquiry -> Tech Corp Global -> contact@techcorpglobal.com -> +1-8005550199 -> 1 (Active Services) -> 1 (Custom Web Application Development) -> We require enterprise SLA and dedicated developer team. -> 2026-11-05 -> 1 (New)
#   4 -> Update Inquiry Status -> INQ-303 -> 2 (In Progress) -> Sent curriculum and installment agreement via email
#   0 -> Back
# 4 -> Search & Filter Hub:
#   1 -> Services -> 1 (Keyword) -> Cloud -> 0
#   2 -> Programs -> 2 (Type) -> 2 (Internship) -> 0
#   3 -> Inquiries -> 2 (Status) -> 2 (In Progress) -> 0
#   0 -> Back
# 5 -> Business Analytics & Reports:
#   1 -> View Executive Report Console
#   3 -> View Revenue Potential Summary
#   4 -> View Most Requested Topics
#   2 -> Export Report -> Enter (uses default path)
#   0 -> Back
# 6 -> System Storage & Data Status:
#   n -> (don't reload)
# 7 -> Exit Application

simulated_inputs = [
    # 1. Service Management
    "1",       # Menu 1: Services
    "1",       # View all
    "2",       # View detail
    "SRV-101",
    "3",       # Add new service
    "Smart Contract Security Audit",
    "6",       # Cybersecurity
    "Thorough security verification and formal audit of EVM smart contracts.",
    "4800.0",
    "1",       # Active
    "0",       # Back to Main Menu

    # 2. Program Management
    "2",       # Menu 2: Programs
    "1",       # View all
    "2",       # View detail
    "PRG-201",
    "3",       # Add new program
    "Autonomous AI Agents Workshop",
    "3",       # Technology
    "4 Weeks",
    "1150.0",
    "25",
    "1",       # Open
    "0",       # Back to Main Menu

    # 3. Customer Inquiry Management
    "3",       # Menu 3: Inquiries
    "1",       # View all
    "2",       # View detail
    "INQ-301",
    "3",       # Add new inquiry
    "Kavita Sharma",
    "kavita.sharma@apexsystems.com",
    "+91-9876541234",
    "1",       # Active Services
    "1",       # First service
    "Seeking dedicated developers for long-term ERP modernization project.",
    "2026-11-05",
    "1",       # New
    "4",       # Update inquiry status
    "INQ-303",
    "2",       # In Progress
    "Scheduled interview call with academic coordinator.",
    "0",       # Back to Main Menu

    # 4. Search & Multi-Criteria Filtering
    "4",       # Menu 4: Search & Filter Hub
    "1",       # Service search
    "1",       # Keyword search
    "Cloud",
    "0",       # Back to Search Hub
    "2",       # Program search
    "2",       # Filter by type
    "2",       # Internship
    "0",       # Back to Search Hub
    "3",       # Inquiry search
    "2",       # Filter by status
    "2",       # In Progress
    "0",       # Back to Search Hub
    "0",       # Back to Main Menu

    # 5. Business Analytics & Reports
    "5",       # Menu 5: Reports
    "1",       # View executive report in console
    "3",       # View revenue potential
    "4",       # View most requested
    "2",       # Export report to file
    "",        # Press enter to accept default path
    "0",       # Back to Main Menu

    # 6. System Data Status
    "6",       # Check status
    "n",       # Do not reload

    # 7. Exit Application
    "7",       # Exit
]

input_stream = "\n".join(simulated_inputs) + "\n"

print("Running automated CLI simulation...")
process = subprocess.Popen(
    [sys.executable, MAIN_PY],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    cwd=PROJECT_DIR,
)

stdout, stderr = process.communicate(input=input_stream)

if stderr:
    print(f"Subprocess stderr:\n{stderr}")

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(stdout)

print(f"Sample run successfully saved to: {OUTPUT_FILE}")
print(f"Exit code: {process.returncode}")
