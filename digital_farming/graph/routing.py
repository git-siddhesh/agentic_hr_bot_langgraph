from typing import Literal
from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition


from memory.state import State
from agent import *
from tools import *


############ USER_INFO ############
# Each delegated workflow can directly respond to the user
# When the user responds, we want to return to the currently active workflow
def route_to_workflow(
    state: State,
) -> Literal[
    "ASSISTANT_PRIMARY",
    "ASSISTANT_IMAGE_PROCESSING",
    # "ASSISTANT_TRANSLATION",
    "ASSISTANT_USER_PROFILE",
    "ASSISTANT_POLICY_GUIDELINE_FAQ",
]:
    """If we are in a delegated state, route directly to the appropriate assistant."""
    
    dialog_state = state.get("dialog_state")
    print("************ DIALOG STATE ************")
    print("+++++❤️❤️++++", dialog_state)

    if not dialog_state:
        return "ASSISTANT_PRIMARY"
    return dialog_state[-1]


############ PRIMARY ASSISTANT ############

def route_primary_assistant(
    state: State,
):
    #  returns the END string if no tool calls are made.  @mc'lupr
    print("************ ROUTE PRIMARY ASSISTANT ************")
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    if tool_calls:
        if tool_calls[0]["name"] == ToImageProcessingAssistant.__name__:
            return "DELEGATE_IMAGE_PROCESSING_ASSISTANT"
        elif tool_calls[0]["name"] == ToTranslationAssistant.__name__:
            return "DELEGATE_TRANSLATION_ASSISTANT"
        elif tool_calls[0]["name"] == ToUserProfileAssistant.__name__:
            return "DELEGATE_USER_PROFILE_ASSISTANT"
        elif tool_calls[0]["name"] == ToPolicyGuideLineFAQAssistant.__name__:
            return "DELEGATE_POLICY_GUIDELINE_FAQ_ASSISTANT"
        
        return "PRIMARY_ASSISTANT_TOOLS"
    raise ValueError("Invalid route")


# # Define the agent decorator
# def agent(name):
#     # def decorator(func):
#     def wrapper(state: State):
#         route = tools_condition(state)
#         if route == END:
#             return END
#         tool_calls = state["messages"][-1].tool_calls
#         did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
#         if did_cancel:
#             return "DEPENDENCY"
#         # Dynamically construct tool list names
#         safe_tool_list = toolList[f"{name}_SAFE_TOOLS"]
#         if all(tc["name"] in [t.name for t in safe_tool_list] for tc in tool_calls):
#             return f"{name}_SAFE_TOOLS"
#         return f"{name}_SENSITIVE_TOOLS"
#     return wrapper
#     # return decorator


# # Usage examples
# @agent("USER_PROFILE")
# def route_user_profile(state: State):
#     pass

# @agent("POLICY_GUIDELINE_FAQ")
# def route_policy_guide_line_faq(state: State):
#     pass



############ TRANSLATION ############

def route_translation(
    state: State,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "DEPENDENCY"
    tool_names = [t.name for t in TRANSLATION_SAFE_TOOLS]
    if all(tc["name"] in tool_names for tc in tool_calls):
        return "TRANSLATION_SAFE_TOOLS"
    return "TRANSLATION_SENSITIVE_TOOLS"
        

############ IMAGE PROCESSING ############

def route_image_processing(
    state: State,
):
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "DEPENDENCY"
    tool_names = [t.name for t in IMAGE_PROCESSING_SAFE_TOOLS]
    if all(tc["name"] in tool_names for tc in tool_calls):
        return "IMAGE_PROCESSING_SAFE_TOOLS"
    return "IMAGE_PROCESSING_SENSITIVE_TOOLS"


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

