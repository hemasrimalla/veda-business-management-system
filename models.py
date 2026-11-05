"""
models.py
---------
Domain models for Veda Technology Business & Service Management System.

Contains class definitions for:
- Service: Represents digital and IT services offered by Veda Technology.
- Program: Represents training, internship, and technology programs.
- Inquiry: Represents prospective customer/client inquiries and interaction history.

Each class implements `to_dict()` and `from_dict()` for clean serialization with JSON.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class Service:
    """Represents a digital or technical service provided by Veda Technology.

    Attributes:
        id (str): Unique service identifier (e.g., 'SRV-101').
        name (str): Service title (e.g., 'Cloud Infrastructure Setup').
        category (str): Service category (e.g., 'Cloud Services', 'Web Development').
        description (str): Comprehensive overview of what the service covers.
        price (float): Base or starting price in USD ($).
        status (str): Operational status ('Active' or 'Inactive').
    """

    def __init__(
        self,
        id: str,
        name: str,
        category: str,
        description: str,
        price: float,
        status: str = "Active",
    ) -> None:
        self.id = id.strip()
        self.name = name.strip()
        self.category = category.strip()
        self.description = description.strip()
        self.price = float(price)
        self.status = status.strip().title()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Service instance to a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "price": round(self.price, 2),
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Service":
        """Instantiate a Service object from a dictionary.

        Args:
            data (dict): Dictionary with keys: id, name, category, description, price, status.

        Returns:
            Service: Initialized Service instance.
        """
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            category=data.get("category", "General"),
            description=data.get("description", ""),
            price=float(data.get("price", 0.0)),
            status=data.get("status", "Active"),
        )

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.category}) - ${self.price:,.2f} [{self.status}]"


class Program:
    """Represents a training, internship, or technology program offered by Veda Technology.

    Attributes:
        id (str): Unique program identifier (e.g., 'PRG-201').
        title (str): Title or course name (e.g., 'Full-Stack Web Development Bootcamp').
        type (str): Type of program ('Training', 'Internship', 'Technology').
        duration (str): Program duration (e.g., '12 Weeks', '6 Months').
        fee (float): Enrollment fee in USD ($). Can be 0.0 for sponsored internships.
        seats (int): Maximum student/participant seat capacity.
        status (str): Enrollment status ('Open', 'Upcoming', 'Closed', 'Ongoing').
    """

    VALID_TYPES = ["Training", "Internship", "Technology"]
    VALID_STATUSES = ["Open", "Upcoming", "Closed", "Ongoing"]

    def __init__(
        self,
        id: str,
        title: str,
        type: str,
        duration: str,
        fee: float,
        seats: int,
        status: str = "Open",
    ) -> None:
        self.id = id.strip()
        self.title = title.strip()
        self.type = type.strip().title()
        self.duration = duration.strip()
        self.fee = float(fee)
        self.seats = int(seats)
        self.status = status.strip().title()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Program instance to a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "duration": self.duration,
            "fee": round(self.fee, 2),
            "seats": self.seats,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Program":
        """Instantiate a Program object from a dictionary.

        Args:
            data (dict): Dictionary with keys: id, title, type, duration, fee, seats, status.

        Returns:
            Program: Initialized Program instance.
        """
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            type=data.get("type", "Training"),
            duration=data.get("duration", "4 Weeks"),
            fee=float(data.get("fee", 0.0)),
            seats=int(data.get("seats", 20)),
            status=data.get("status", "Open"),
        )

    def __str__(self) -> str:
        fee_display = f"${self.fee:,.2f}" if self.fee > 0 else "Free/Sponsored"
        return f"[{self.id}] {self.title} | {self.type} ({self.duration}) - {fee_display} - Seats: {self.seats} [{self.status}]"


class Inquiry:
    """Represents a prospective customer or candidate inquiry.

    Attributes:
        id (str): Unique inquiry identifier (e.g., 'INQ-301').
        customer_name (str): Full name of the prospect.
        email (str): Contact email address.
        phone (str): Contact phone number.
        interest (str): Service or program title of interest.
        message (str): Detailed message or requirement query.
        date (str): Date of submission (YYYY-MM-DD or YYYY-MM-DD HH:MM).
        status (str): Follow-up status ('New', 'In Progress', 'Resolved').
        history (List[Dict[str, str]]): Chronological audit log of status changes and notes.
    """

    VALID_STATUSES = ["New", "In Progress", "Resolved"]

    def __init__(
        self,
        id: str,
        customer_name: str,
        email: str,
        phone: str,
        interest: str,
        message: str,
        date: str,
        status: str = "New",
        history: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        self.id = id.strip()
        self.customer_name = customer_name.strip()
        self.email = email.strip()
        self.phone = phone.strip()
        self.interest = interest.strip()
        self.message = message.strip()
        self.date = date.strip()
        self.status = status.strip().title()
        if history is None:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.history = [
                {
                    "timestamp": now_str,
                    "status": self.status,
                    "note": "Inquiry recorded in system",
                }
            ]
        else:
            self.history = history

    def add_status_update(self, new_status: str, note: str = "") -> None:
        """Update inquiry status and append an audit record to history.

        Args:
            new_status (str): 'New', 'In Progress', or 'Resolved'.
            note (str): Optional context note describing the change.
        """
        self.status = new_status.strip().title()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.history.append(
            {
                "timestamp": now_str,
                "status": self.status,
                "note": note.strip() or f"Status changed to {self.status}",
            }
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Inquiry instance to a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "email": self.email,
            "phone": self.phone,
            "interest": self.interest,
            "message": self.message,
            "date": self.date,
            "status": self.status,
            "history": self.history,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Inquiry":
        """Instantiate an Inquiry object from a dictionary.

        Args:
            data (dict): Dictionary with keys: id, customer_name, email, phone,
                         interest, message, date, status, history.

        Returns:
            Inquiry: Initialized Inquiry instance.
        """
        return cls(
            id=data.get("id", ""),
            customer_name=data.get("customer_name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            interest=data.get("interest", ""),
            message=data.get("message", ""),
            date=data.get("date", datetime.now().strftime("%Y-%m-%d")),
            status=data.get("status", "New"),
            history=data.get("history", []),
        )

    def __str__(self) -> str:
        return f"[{self.id}] {self.customer_name} -> {self.interest} ({self.date}) [{self.status}]"
