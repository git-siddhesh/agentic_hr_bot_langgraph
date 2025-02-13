from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from tools.slave.reimbursement import *
from tools.rag import lookup_policy
from agent.schemas import CompleteOrEscalate
llm = ChatOpenAI(model="gpt-4o-mini")

# leave booking assistant

reimbursement_hr_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for managing employee reimbursement-related tasks. "
            "The primary assistant delegates work to you whenever the user requires assistance with reimbursement submissions, cancellations, or status inquiries. "
            "Your primary responsibilities include submitting reimbursement requests, checking the status of reimbursement claims, and processing cancellations of reimbursement requests. "
            "Confirm the details of any reimbursement-related action with the user, provide necessary clarifications, and inform them of any policy-related implications or required documents. "
            "\n\nWhen searching for reimbursement details or processing requests, be thorough and double-check all available data. "
            "If the user changes their mind or requires assistance beyond the scope of your tools, escalate the task back to the main assistant. "
            "Remember, no reimbursement request is finalized until the relevant tool has been successfully executed."
            
            "\nCurrent time: {time}."
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then "
            '"CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)





REIMBURSEMENT_SAFE_TOOLS = [lookup_policy, check_reimbursement_status, submit_reimbursement_request]
REIMBURSEMENT_SENSITIVE_TOOLS = [cancel_reimbursement_request]
REIMBURSEMENT_RUNNABLE = reimbursement_hr_prompt | llm.bind_tools(
    REIMBURSEMENT_SAFE_TOOLS + REIMBURSEMENT_SENSITIVE_TOOLS + [CompleteOrEscalate]
)