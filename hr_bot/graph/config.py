from typing import Dict, List, Any
from agent import *
from graph.util import *
from graph.routing import *

assistant_config: Dict[str, Dict[str, Any]] = {
    "HIRING": {
        "name": "Hiring and Recruitment Assistant",
        "routing_function": route_hiring,
        "safe_tools": HIRING_SAFE_TOOLS,
        "sensitive_tools": HIRING_SENSITIVE_TOOLS,
    },
    "LEAVE": {
        "name": "Leave Management Assistant",
        "routing_function": route_leave,
        "safe_tools": LEAVE_SAFE_TOOLS,
        "sensitive_tools": LEAVE_SENSITIVE_TOOLS,
    },
    "PAYSLIP": {
        "name": "Salary and Payslip Assistant",
        "routing_function": route_payslip,
        "safe_tools": PAYSLIP_SAFE_TOOLS,
        "sensitive_tools": PAYSLIP_SENSITIVE_TOOLS,
    },
    "REIMBURSEMENT": {
        "name": "Reimbursement Management Assistant",
        "routing_function": route_reimbursement,
        "safe_tools": REIMBURSEMENT_SAFE_TOOLS,
        "sensitive_tools": REIMBURSEMENT_SENSITIVE_TOOLS,
    },
    "USER_PROFILE": {
        "name": "User Profile Assistant",
        "routing_function": route_user_profile,
        "safe_tools": USER_PROFILE_SAFE_TOOLS,
        "sensitive_tools": USER_PROFILE_SENSITIVE_TOOLS,
    },
    "TRAVEL": {
        "name": "Travel management Assistant",
        "routing_function": route_travel,
        "safe_tools": TRAVEL_SAFE_TOOLS,
        "sensitive_tools": TRAVEL_SENSITIVE_TOOLS,
    },
    "POLICY_GUIDELINE_FAQ": {
        "name": "Policy & Guideline FAQ retrieval Assistant",
        "routing_function": route_policy_guide_line_faq,
        "safe_tools": POLICY_GUIDELINE_FAQ_SAFE_TOOLS,
        "sensitive_tools": POLICY_GUIDELINE_FAQ_SENSITIVE_TOOLS,
    },
}