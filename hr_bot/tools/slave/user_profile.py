from typing import Optional, Dict, Any, List
from datetime import date
from langchain_core.tools import tool

from database.utils import db
from langchain_core.tools import tool
import sqlite3
from langchain_core.runnables import RunnableConfig

@tool
def fetch_user_information(config: RunnableConfig) -> List[Dict[str, Any]]:
    """Fetch all minimum information required to process any user query.

    Returns:
        A list of dictionaries where each dictionary contains the user details
    """
    configuration = config.get("configurable", {})
    passenger_id = configuration.get("passenger_id", None)
    if not passenger_id:
        raise ValueError("No passenger ID configured.")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = """
    SELECT 
        t.ticket_no, t.book_ref,
        f.flight_id, f.flight_no, f.departure_airport, f.arrival_airport, f.scheduled_departure, f.scheduled_arrival,
        bp.seat_no, tf.fare_conditions
    FROM 
        tickets t
        JOIN ticket_flights tf ON t.ticket_no = tf.ticket_no
        JOIN flights f ON tf.flight_id = f.flight_id
        JOIN boarding_passes bp ON bp.ticket_no = t.ticket_no AND bp.flight_id = f.flight_id
    WHERE 
        t.passenger_id = ?
    """
    cursor.execute(query, (passenger_id,))
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results



@tool
def search_directory(
    query: str,
    filter_by: Optional[str] = None,  # e.g., "department", "location", "role"
    limit: Optional[int] = 10,
) -> List[Dict[str, Any]]:
    """
    Searches the employee directory based on a query.

    Args:
        query: The search term (e.g., name, role).
        filter_by: Optional; filter results by department, location, or role.
        limit: Optional; limit the number of results.

    Returns:
        results: A list of employees matching the search criteria.
    """
    return [
        {"employee_id": 101, "name": "Alice Johnson", "role": "Software Engineer", "department": "IT"},
        {"employee_id": 102, "name": "Bob Smith", "role": "Data Analyst", "department": "Finance"},
    ]

@tool
def view_profile(
    employee_id: int,
) -> Dict[str, Any]:
    """
    Retrieves detailed information about an employee's profile.

    Args:
        employee_id: The ID of the employee.

    Returns:
        profile: A dictionary containing the employee's profile details.
    """
    return {
        "employee_id": employee_id,
        "name": "Alice Johnson",
        "role": "Software Engineer",
        "department": "IT",
        "email": "alice.johnson@example.com",
        "phone": "123-456-7890",
        "location": "New York",
        "hire_date": "2022-01-15",
        "status": "Active",
    }

@tool
def update_profile(
    employee_id: int,
    updates: Dict[str, Any],  # Example: {"phone": "987-654-3210", "location": "San Francisco"}
) -> bool:
    """
    Updates specific fields in an employee's profile.

    Args:
        employee_id: The ID of the employee.
        updates: A dictionary containing the fields to update and their new values.

    Returns:
        status: True if the profile was successfully updated, False otherwise.
    """
    return True

@tool
def send_message(
    sender_id: int,
    recipient_id: int,
    message: str,
) -> bool:
    """
    Sends a message to an employee.

    Args:
        sender_id: The ID of the sender.
        recipient_id: The ID of the recipient.
        message: The message content.

    Returns:
        status: True if the message was successfully sent, False otherwise.
    """
    return True

@tool
def initiate_registration(
    name: str,
    email: str,
    role: str,
    department: str,
    start_date: date,
) -> int:
    """
    Initiates the registration process for a new employee.

    Args:
        name: The name of the new employee.
        email: The email address of the new employee.
        role: The role of the new employee.
        department: The department of the new employee.
        start_date: The start date of the new employee.

    Returns:
        employee_id: The ID assigned to the new employee.
    """
    return 201

@tool
def verify_profile(
    employee_id: int,
) -> bool:
    """
    Verifies the details of an employee's profile to ensure accuracy and completeness.

    Args:
        employee_id: The ID of the employee.

    Returns:
        status: True if the profile is verified, False otherwise.
    """
    return True

@tool
def deactivate_profile(
    employee_id: int,
    reason: Optional[str] = None,
) -> bool:
    """
    Deactivates an employee's profile in the system.

    Args:
        employee_id: The ID of the employee to deactivate.
        reason: Optional; the reason for deactivation.

    Returns:
        status: True if the profile was successfully deactivated, False otherwise.
    """
    return True

@tool
def view_directory_stats() -> Dict[str, Any]:
    """
    Provides statistics about the employee directory.

    Returns:
        stats: A dictionary containing directory statistics, such as total employees and active employees.
    """
    return {
        "total_employees": 1500,
        "active_employees": 1450,
        "departments": 12,
        "locations": 5,
    }

@tool
def generate_contact_list(
    department: Optional[str] = None,
    location: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Generates a contact list of employees, optionally filtered by department or location.

    Args:
        department: Optional; filter the contact list by department.
        location: Optional; filter the contact list by location.

    Returns:
        contacts: A list of dictionaries containing employee contact details.
    """
    return [
        {"name": "Alice Johnson", "email": "alice.johnson@example.com", "phone": "123-456-7890"},
        {"name": "Bob Smith", "email": "bob.smith@example.com", "phone": "987-654-3210"},
    ]

@tool
def add_emergency_contact(
    employee_id: int,
    contact_name: str,
    contact_phone: str,
    relationship: str,
) -> bool:
    """
    Adds an emergency contact to an employee's profile.

    Args:
        employee_id: The ID of the employee.
        contact_name: The name of the emergency contact.
        contact_phone: The phone number of the emergency contact.
        relationship: The relationship of the emergency contact to the employee.

    Returns:
        status: True if the emergency contact was successfully added, False otherwise.
    """
    return True
