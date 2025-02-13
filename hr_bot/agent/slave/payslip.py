from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from tools.slave.payslip import *
from tools.rag import lookup_policy
from agent.schemas import CompleteOrEscalate
llm = ChatOpenAI(model="gpt-4o-mini")

# leave booking assistant

salary_hr_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for managing employee salary-related tasks. "
            "The primary assistant delegates work to you whenever the user requires assistance with payslips, salary breakdowns, taxation details, or deduction information. "
            "Your primary responsibilities include retrieving payslip details, providing information on salary deductions, offering salary breakdowns, and explaining taxation details. "
            "Confirm the details of any salary-related action with the user, provide necessary clarifications, and ensure all provided information is accurate and up-to-date. "
            "\n\nWhen searching for salary-related information, be thorough and double-check all available data. "
            "If the user changes their mind or requires assistance beyond the scope of your tools, escalate the task back to the main assistant. "
            "Remember, no salary-related request is considered complete until the relevant tool has been successfully executed."
            
            "\nCurrent time: {time}."
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then "
            '"CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)




PAYSLIP_SAFE_TOOLS = [lookup_policy, get_playslip, get_deduction_info, get_salary_breakdown, get_taxation_details]
PAYSLIP_SENSITIVE_TOOLS = []
PAYSLIP_RUNNABLE = salary_hr_prompt | llm.bind_tools(
    PAYSLIP_SAFE_TOOLS + PAYSLIP_SENSITIVE_TOOLS + [CompleteOrEscalate]
)