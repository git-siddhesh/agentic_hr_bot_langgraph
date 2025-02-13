from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from tools.slave.hiring import *
from tools.rag import lookup_policy
from agent.schemas import CompleteOrEscalate
llm = ChatOpenAI(model="gpt-4o-mini")

# Flight booking assistant

hiring_hr_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for handling hiring-related tasks. "
            "The primary assistant delegates work to you whenever the user requires assistance with recruitment, onboarding, or HR policies. "
            "Your primary responsibilities include scheduling interviews, tracking candidate statuses, posting job openings, generating hiring reports, and managing offer letters. "
            "Confirm the details of any action with the user and provide any necessary clarifications or follow-ups. "
            "If a task involves sensitive or critical actions, ensure you double-check all available information before proceeding."
            "\n\nWhen searching for policies, reports, or candidate details, be persistent. Expand your query bounds if the initial search returns no results. "
            "If the user requires assistance beyond the scope of your tools, or changes their mind, escalate the task back to the main assistant. "
            "Remember that no task is considered complete until the relevant tool has been successfully executed."
            
            "\nCurrent time: {time}."
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then "
            '"CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)


HIRING_SAFE_TOOLS = [lookup_policy, track_candidate_status, post_job_opening, shortlist_candidates, generate_hiring_report, feedback_collection, interview_reschedule, generate_offer_letter]
HIRING_SENSITIVE_TOOLS = [schedule_interview, initiate_onboarding]
HIRING_RUNNABLE = hiring_hr_prompt | llm.bind_tools(
    HIRING_SAFE_TOOLS + HIRING_SENSITIVE_TOOLS + [CompleteOrEscalate]
)