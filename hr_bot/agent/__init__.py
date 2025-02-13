import time
st = time.time()
print("Defining agent schemas...")
from agent.schemas import (
    ToHiringAssistant, 
    ToLeaveAssistant, 
    ToPayslipAssistant, 
    ToReimbursementAssistant, 
    ToTravelAssistant, 
    ToUserProfileAssistant,
    CompleteOrEscalate,
    ToPolicyGuideLineFAQAssistant
)
pt =  time.time()
print("Time taken to define agent schemas: ",pt-st)
print("Importing base agents...")
from agent.base import Assistant
et = time.time()
print("Time taken to import base agents: ", et-st)

print("Initializing agents...")
from agent.slave.hiring import (
    HIRING_SENSITIVE_TOOLS,
    HIRING_SAFE_TOOLS,
    HIRING_RUNNABLE
)

from agent.slave.leave import (
    LEAVE_SENSITIVE_TOOLS,
    LEAVE_SAFE_TOOLS,
    LEAVE_RUNNABLE
)

from agent.slave.payslip import (
    PAYSLIP_SENSITIVE_TOOLS,
    PAYSLIP_SAFE_TOOLS,
    PAYSLIP_RUNNABLE
)

from agent.slave.reimbursement import (
    REIMBURSEMENT_SENSITIVE_TOOLS,
    REIMBURSEMENT_SAFE_TOOLS,
    REIMBURSEMENT_RUNNABLE
)

from agent.slave.travel import (
    TRAVEL_SENSITIVE_TOOLS,
    TRAVEL_SAFE_TOOLS,
    TRAVEL_RUNNABLE
)

from agent.slave.user_profile import (
    USER_PROFILE_SENSITIVE_TOOLS,
    USER_PROFILE_SAFE_TOOLS,
    USER_PROFILE_RUNNABLE
)

from agent.slave.policy_guideline_faq import (
    POLICY_GUIDELINE_FAQ_SENSITIVE_TOOLS,
    POLICY_GUIDELINE_FAQ_SAFE_TOOLS,
    POLICY_GUIDELINE_FAQ_RUNNABLE
)

from agent.master.primary import (
    PRIMARY_ASSISTANT_TOOLS,
    ASSISTANT_RUNNABLE
)

print("Time taken to import all the agents: ", time.time()-et)

__all__ = [
    "ToHiringAssistant",
    "ToLeaveAssistant",
    "ToPayslipAssistant",
    "ToReimbursementAssistant",
    "ToTravelAssistant",
    "ToUserProfileAssistant",
    "Assistant",
    "CompleteOrEscalate",
    "ToPolicyGuideLineFAQAssistant",

    "HIRING_SENSITIVE_TOOLS",
    "HIRING_SAFE_TOOLS",
    "HIRING_RUNNABLE",

    "LEAVE_SENSITIVE_TOOLS",
    "LEAVE_SAFE_TOOLS",
    "LEAVE_RUNNABLE",

    "PAYSLIP_SENSITIVE_TOOLS",
    "PAYSLIP_SAFE_TOOLS",
    "PAYSLIP_RUNNABLE",

    "REIMBURSEMENT_SENSITIVE_TOOLS",
    "REIMBURSEMENT_SAFE_TOOLS",
    "REIMBURSEMENT_RUNNABLE",

    "TRAVEL_SENSITIVE_TOOLS",
    "TRAVEL_SAFE_TOOLS",
    "TRAVEL_RUNNABLE",
    
    "USER_PROFILE_SENSITIVE_TOOLS",
    "USER_PROFILE_SAFE_TOOLS",
    "USER_PROFILE_RUNNABLE",

    "POLICY_GUIDELINE_FAQ_SENSITIVE_TOOLS",
    "POLICY_GUIDELINE_FAQ_SAFE_TOOLS",
    "POLICY_GUIDELINE_FAQ_RUNNABLE",

    "PRIMARY_ASSISTANT_TOOLS",
    "ASSISTANT_RUNNABLE",

]