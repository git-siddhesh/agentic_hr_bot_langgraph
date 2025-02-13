from typing import Literal
from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition


from memory.state import State
from agent import *



############ USER_INFO ############
# Each delegated workflow can directly respond to the user
# When the user responds, we want to return to the currently active workflow
def route_to_workflow(
    state: State,
) -> Literal[
    "ASSISTANT_PRIMARY",

    "ASSISTANT_HIRING",
    "ASSISTANT_LEAVE",
    "ASSISTANT_PAYSLIP",
    "ASSISTANT_REIMBURSEMENT",
    "ASSISTANT_USER_PROFILE",
    "ASSISTANT_TRAVEL",
    "ASSISTANT_POLICY_GUIDELINE_FAQ",
]:
    """If we are in a delegated state, route directly to the appropriate assistant."""
    dialog_state = state.get("dialog_state")
    print("+++++❤️❤️++++", dialog_state)
    if not dialog_state:
        return "ASSISTANT_PRIMARY"
    return dialog_state[-1]


############ PRIMARY ASSISTANT ############

def route_primary_assistant(
    state: State,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    if tool_calls:
        if tool_calls[0]["name"] == ToHiringAssistant.__name__:
            return "DELEGATE_HIRING_ASSISTANT"
        elif tool_calls[0]["name"] == ToLeaveAssistant.__name__:
            return "DELEGATE_LEAVE_ASSISTANT"
        elif tool_calls[0]["name"] == ToPayslipAssistant.__name__:
            return "DELEGATE_PAYSLIP_ASSISTANT"
        elif tool_calls[0]["name"] == ToReimbursementAssistant.__name__:
            return "DELEGATE_REIMBURSEMENT_ASSISTANT"
        elif tool_calls[0]["name"] == ToUserProfileAssistant.__name__:
            return "DELEGATE_USER_PROFILE_ASSISTANT"
        elif tool_calls[0]["name"] == ToTravelAssistant.__name__:
            return "DELEGATE_TRAVEL_ASSISTANT"
        elif tool_calls[0]["name"] == ToPolicyGuideLineFAQAssistant.__name__:
            return "DELEGATE_POLICY_GUIDELINE_FAQ_ASSISTANT"
        
        return "PRIMARY_ASSISTANT_TOOLS"
    raise ValueError("Invalid route")



############# HIRING ###############
def route_hiring(
    state: State,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "DEPENDENCY"
    safe_toolnames = [t.name for t in HIRING_SAFE_TOOLS]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "HIRING_SAFE_TOOLS"
    return "HIRING_SENSITIVE_TOOLS"


############ LEAVE ASSISTANT ############

def route_leave(
    state: State,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "DEPENDENCY"
    safe_toolnames = [t.name for t in LEAVE_SAFE_TOOLS]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "LEAVE_SAFE_TOOLS"
    return "LEAVE_SENSITIVE_TOOLS"

############ PAYSLIP ASSISTANT ############

def route_payslip(
    state: State,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "DEPENDENCY"
    tool_names = [t.name for t in PAYSLIP_SAFE_TOOLS]
    if all(tc["name"] in tool_names for tc in tool_calls):
        return "PAYSLIP_SAFE_TOOLS"
    return "PAYSLIP_SENSITIVE_TOOLS"


############ REIMBURSEMENT ASSISTANT ############

def route_reimbursement(
    state: State,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "DEPENDENCY"
    tool_names = [t.name for t in REIMBURSEMENT_SAFE_TOOLS]
    if all(tc["name"] in tool_names for tc in tool_calls):
        return  "REIMBURSEMENT_SAFE_TOOLS"
    return "REIMBURSEMENT_SENSITIVE_TOOLS"



############ TRAVEL ASSISTANT ############

def route_travel(
    state: State,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "DEPENDENCY"
    tool_names = [t.name for t in TRAVEL_SAFE_TOOLS]
    if all(tc["name"] in tool_names for tc in tool_calls):
        return "TRAVEL_SAFE_TOOLS"
    return "TRAVEL_SENSITIVE_TOOLS"


############ USER PROFILE ASSISTANT ############

def route_user_profile(
    state: State,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "DEPENDENCY"
    tool_names = [t.name for t in USER_PROFILE_SAFE_TOOLS]
    if all(tc["name"] in tool_names for tc in tool_calls):
        return "USER_PROFILE_SAFE_TOOLS"
    return "USER_PROFILE_SENSITIVE_TOOLS"

############ POLICY GUIDE LINE FAQ ASSISTANT ############

def route_policy_guide_line_faq(
    state: State,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "DEPENDENCY"
    tool_names = [t.name for t in POLICY_GUIDELINE_FAQ_SAFE_TOOLS]
    if all(tc["name"] in tool_names for tc in tool_calls):
        return "POLICY_GUIDELINE_FAQ_SAFE_TOOLS"
    return "POLICY_GUIDELINE_FAQ_SENSITIVE_TOOLS"

