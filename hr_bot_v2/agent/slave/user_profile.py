from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from tools.slave.user_profile import *
from tools.rag import lookup_policy
from agent.schemas import CompleteOrEscalate
llm = ChatOpenAI(model="gpt-4o-mini")

# leave booking assistant
user_profile_hr_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for managing employee profile-related tasks. "
            "The primary assistant delegates work to you whenever the user requires assistance with directory searches, profile management, or contact-related updates. "
            "Your primary responsibilities include searching and viewing directory information, verifying profiles, initiating registrations, and generating contact lists. "
            "You are also responsible for handling sensitive tasks such as updating profiles, deactivating profiles, and adding emergency contacts. "
            "Confirm the details of any profile-related action with the user, provide necessary clarifications, and ensure that sensitive changes are executed carefully and securely. "
            "\n\nWhen searching for directory or profile information, or processing profile-related requests, be thorough and double-check all available data. "
            "If the user changes their mind or requires assistance beyond the scope of your tools, escalate the task back to the main assistant. "
            "Remember, no profile-related request is considered complete until the relevant tool has been successfully executed."
            
            "\nCurrent time: {time}."
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then "
            '"CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)




USER_PROFILE_SAFE_TOOLS = [lookup_policy, search_directory, view_directory_stats, verify_profile, view_profile, send_message, initiate_registration,  generate_contact_list]
USER_PROFILE_SENSITIVE_TOOLS = [ update_profile, deactivate_profile, add_emergency_contact]
USER_PROFILE_RUNNABLE = user_profile_hr_prompt | llm.bind_tools(
    USER_PROFILE_SAFE_TOOLS + USER_PROFILE_SENSITIVE_TOOLS + [CompleteOrEscalate]
)