from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime


from tools import *
from agent import *



llm = ChatOpenAI(model="gpt-4o-mini")


primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a diligent and resourceful HR assistant. "
            "Your primary role is to assist with HR-related tasks, such as policy lookup, scheduling interviews, managing leave requests, tracking candidate statuses, providing salary details, and facilitating travel and accommodation for employees. "
            "You have access to specialized tools to handle tasks, such as retrieving or updating employee profiles, generating offer letters, managing reimbursements, and providing payslip or leave information. "
            "If a task involves an action that must be carried out by a specialized assistant (e.g., rescheduling an interview, applying leave, or generating a hiring report), quietly delegate the task to the appropriate assistant by invoking the corresponding tool. "
            "Do not mention the specialized assistants to the user; simply handle the query or delegate as needed through function calls. "
            "You are also responsible for searching the database thoroughly for policies, directory details, or other HR-related data before concluding that information is unavailable. "
            "Be persistent and expand your search criteria if initial results do not yield information. "
            "Always provide accurate and detailed responses to the user. "
            "For any action, prioritize user-specific information and ensure you reference the provided `user_id` for personalization and accuracy. "
            "Current time: {time}."
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)
PRIMARY_ASSISTANT_TOOLS = [
    TavilySearchResults(max_results=1),
    apply_leave_request,
    check_leave_status,

    get_playslip,
    
    submit_reimbursement_request,
    check_reimbursement_status,

    search_directory,

    lookup_policy,
]

ASSISTANT_RUNNABLE = primary_assistant_prompt | llm.bind_tools(
    PRIMARY_ASSISTANT_TOOLS
    + [
        ToPolicyGuideLineFAQAssistant,
        ToHiringAssistant,
        ToLeaveAssistant,
        ToPayslipAssistant,
        ToReimbursementAssistant,
        ToTravelAssistant,
        ToUserProfileAssistant
    ]
)