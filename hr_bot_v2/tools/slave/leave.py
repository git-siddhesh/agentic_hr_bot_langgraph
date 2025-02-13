from datetime import date
from typing import Optional, Dict, Any
from langchain_core.tools import tool
import random
@tool
def apply_leave_request(
    user_id: int,
    start_date: date,
    end_date: date,
    leave_type: str,
    reason: str,
) -> Optional[int]:
    """
    Submits a leave request for a user.

    Args:
        user_id: The user ID of the user applying for leave.
        start_date: The start date of the leave.
        end_date: The end date of the leave.
        leave_type: Type of leave (e.g., annual, sick, casual, etc.).
        reason: The reason for the leave.

    Returns:
        leave_request_id: The ID of the leave request that was submitted, or None if the request failed.
    """
    return 101  # Mocked leave request ID

@tool
def check_leave_status(
    user_id: int,
    leave_request_id: int,
) -> Optional[Dict[str, Any]]:
    """
    Checks the status of a leave request for a user.

    Args:
        user_id: The user ID of the user checking the leave status.
        leave_request_id: The ID of the leave request.

    Returns:
        status: A dictionary containing the status and details of the leave request.
        1. if approved: (status, approval_date, approved_by)
        2. if pending: (status, reason, stage)
    """
    case1 = {
        "status": "approved",
        "approval_date": "2025-01-10",
        "approved_by": "Manager A",
    }
    case2 = {
        "status": "pending",
        "reason": "More information required",
        "stage": "HR review",
    }
    return random.choice([case1, case2])

@tool
def cancel_leave_request(
    user_id: int,
    leave_request_id: int,
) -> bool:
    """
    Cancels a leave request for a user.

    Args:
        user_id: The user ID of the user cancelling the leave request.
        leave_request_id: The ID of the leave request to be cancelled.

    Returns:
        status: True if the leave request was successfully cancelled, False otherwise.
    """
    return True

@tool
def calculate_leave_balance(
    user_id: int,
) -> Dict[str, int]:
    """
    Calculates the remaining leave balance for a user.
    how many leaves i have (left)how

    Args:
        user_id: The user ID of the user checking leave balance.

    Returns:
        leave_balance: A dictionary containing leave types and their remaining balances.
    """
    return {
        "annual_leave": 10,
        "sick_leave": 5,
        "casual_leave": 3,
        "maternity_leave": 0,
    }

@tool
def calculate_leave_encashment(
    user_id: int,
    leave_type: str,
    days_to_encash: int,
) -> Optional[float]:
    """
    Calculates the amount a user would receive for encashing leave days.

    Args:
        user_id: The user ID of the user calculating leave encashment.
        leave_type: The type of leave to encash (e.g., annual).
        days_to_encash: The number of leave days to encash.

    Returns:
        encashment_amount: The total encashment amount, or None if encashment is not allowed.
    """
    per_day_rate = 150.0  # Example daily rate
    return days_to_encash * per_day_rate

@tool
def modify_leave_request(
    user_id: int,
    leave_request_id: int,
    new_start_date: Optional[date] = None,
    new_end_date: Optional[date] = None,
    new_reason: Optional[str] = None,
) -> bool:
    """
    Modifies an existing leave request for a user.

    Args:
        user_id: The user ID of the user modifying the leave request.
        leave_request_id: The ID of the leave request to be modified.
        new_start_date: The new start date of the leave (optional).
        new_end_date: The new end date of the leave (optional).
        new_reason: The new reason for the leave (optional).

    Returns:
        status: True if the modification was successful, False otherwise.
    """
    return True
