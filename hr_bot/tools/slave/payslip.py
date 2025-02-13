from database.utils import db
from langchain_core.tools import tool
import requests
import sqlite3
from datetime import datetime, date
from typing import Optional, Dict, List, Any

from utils.db_utils import execute_query


ACCESS_URL = 'https://hrbotapi.chapterapps.ai/api/v1/auth/token'
SALARY_URL = 'https://hrbotapi.chapterapps.ai/api/v1/paysheet/paysheet'


def get_access_token(user_id: int=3) -> str:
    """Get the access token for the user"""
    response = requests.post(ACCESS_URL, params={"user_id": user_id}, timeout=30)
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response['message']}")
    response = response.json()
    access_token = response['access_token']
    return access_token

@tool
def get_playslip(user_id : int = 3, start_date: str = '12-2024', end_date: str = '12-2024', total_records:int = 1) -> Dict[str, str]:
    """fetch the paysheet details of a user for a given period"""
    try:
        access_token = get_access_token(user_id)
        
        # call the api to get the paysheet details with ?start_date=12-2024&end_date=12-2024
        response = requests.get(SALARY_URL, params={'start_date': start_date, 'end_date': end_date}, headers={'Authorization': f'bearer {access_token}'}, timeout=30)
        response = response.json()
        return response
    except Exception as e:
        return {"error": str(e)}
    
@tool
def get_deduction_info(
    user_id: int,
    amount: float,
    ) -> Dict[str, Any]:
    """
    Get the deduction details for the user
    - Name
    - Deductions
    - Reason
    """

    # Fetch the salary details from the database
    query = f"SELECT * FROM other_deduction WHERE id = {user_id} and Deductions = {amount}"  
    print(query)
    # query = f"SELECT * FROM master_reco"
    salary_details = execute_query(query, args=() )
    if not salary_details:
        return {"error": "No salary details found for the user"}
    if salary_details:
        return {
            "Name": salary_details[0]['Name'],
            "Deductions": salary_details[0]['Deductions'],
            "Reason": salary_details[0]['Reason']
        }
    return {}


@tool
def get_salary_breakdown(user_id: int) -> Dict[str, Any]:
    """Get the salary breakdown for the user 
    - basic
    - hra
    - conveyance
    - Special Allowance
    - pf employer
    - CTC pm
    - FIXED CTC
    - CTC Per Annum
    """

    # Fetch the salary details from the database
    query = f"SELECT * FROM master_reco WHERE id = {user_id}"  
    print(query)
    # query = f"SELECT * FROM master_reco"
    salary_details = execute_query(query, args=() )
    if not salary_details:
        return {"error": "No salary details found for the user"}
    return salary_details[0] if salary_details else {}


@tool
def get_taxation_details(user_id: int) -> Dict[str, Any]:
    """Get the salary breakdown for the user 
    
    Args:
        user_id (int): The user id of the user
    
    Returns:
        - Income tax
    """

    return {
        "income_tax": 100
    }
