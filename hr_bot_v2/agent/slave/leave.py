from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from tools.slave.leave import *
from tools.rag import lookup_policy

from agent.schemas import CompleteOrEscalate
llm = ChatOpenAI(model="gpt-4o-mini")

# leave booking assistant

leave_hr_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for managing employee leave-related tasks. "
            "The primary assistant delegates work to you whenever the user requires assistance with leave applications, modifications, cancellations, or status inquiries. "
            "Your primary responsibilities include applying for leave, checking leave status, calculating leave balance, leave encashment, and processing modifications or cancellations of leave requests. "
            "Confirm the details of any leave-related action with the user, provide necessary clarifications, and inform them of any policy-related implications. "
            "\n\nWhen searching for leave policies, balances, or status updates, be persistent and double-check all available data. "
            "If the user changes their mind or requires assistance beyond the scope of your tools, escalate the task back to the main assistant. "
            "Remember, no leave request is finalized until the relevant tool has been successfully executed."
            
            "\nCurrent time: {time}."
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then "
            '"CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)



LEAVE_SAFE_TOOLS = [lookup_policy, apply_leave_request, check_leave_status, calculate_leave_balance, calculate_leave_encashment]
LEAVE_SENSITIVE_TOOLS = [cancel_leave_request, modify_leave_request]
LEAVE_RUNNABLE = leave_hr_prompt | llm.bind_tools(
    LEAVE_SAFE_TOOLS + LEAVE_SENSITIVE_TOOLS + [CompleteOrEscalate]
)