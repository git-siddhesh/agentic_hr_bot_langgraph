from database.utils import db
from langchain_core.tools import tool
import requests
import sqlite3
from datetime import datetime, date
from typing import Optional, Dict, List, Any

from utils.db_utils import execute_query



@tool
def cancel_reimbursement_request(
    user_id: int,
    reimbursement_id: int,
    ) -> bool:
    """
    Cancels a reimbursement request for a user.

    Args:
        user_id: The user ID of the user who is cancelling the reimbursement request.
        reimbursement_id: The ID of the reimbursement request to be cancelled.
    
    Returns:
        status: True if the reimbursement request was successfully cancelled, False otherwise.
    """

    return True


@tool
def check_reimbursement_status(
    user_id: int,
    reimbursement_id: int,
    ) -> Optional[Dict[str, Any]]:
    """
    Checks the status of a reimbursement request for a user.

    Args:
        user_id: The user ID of the user who is checking the reimbursement request status.
        reimbursement_id: The ID of the reimbursement request to check the status of.
    
    Returns:
        status: A dictionary containing the status of the reimbursement request.
    """

    return {
        "status": "pending",
        "stage": "manager_approval",
    }

@tool
def submit_reimbursement_request(
    user_id: int,
    amount: float,
    description: str,
    date: date,
    category: str,
    ) -> Optional[int]:
    """
    Submits a reimbursement request for a user.

    Args:
        user_id: The user ID of the user who is submitting the reimbursement request.
        amount: The amount of the reimbursement request.
        description: The description of the reimbursement request.
        date: The date of the expense.
        category : (personal, travel, food, other)
    
    Returns:
        reimbursement_id: The ID of the reimbursement request that was submitted.
    """

    return 1