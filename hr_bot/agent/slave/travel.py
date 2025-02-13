from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from tools.slave.travel import *
from tools.rag import lookup_policy
from agent.schemas import CompleteOrEscalate
llm = ChatOpenAI(model="gpt-4o-mini")

# leave booking assistant

travel_hr_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for managing employee travel-related tasks. "
            "The primary assistant delegates work to you whenever the user requires assistance with booking, managing, or tracking travel arrangements. "
            "Your primary responsibilities include booking tickets and accommodations, checking ticket and accommodation statuses, searching for travel options, generating itineraries, and notifying users of updates. "
            "You are also responsible for handling cancellations and rescheduling of tickets or accommodations when required. "
            "Confirm the details of any travel-related action with the user, provide necessary clarifications, and inform them of any additional fees or policy-related implications. "
            "\n\nWhen searching for travel options or processing travel-related requests, be thorough and double-check all available data. "
            "If the user changes their mind or requires assistance beyond the scope of your tools, escalate the task back to the main assistant. "
            "Remember, no travel-related request is considered complete until the relevant tool has been successfully executed."
            
            "\nCurrent time: {time}."
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then "
            '"CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)




TRAVEL_SAFE_TOOLS = [lookup_policy, book_ticket,  check_ticket_status, search_accommodation, search_ticket_options, book_accommodation, get_booking_summary, generate_itinerary, check_accommodation_status, notify_booking_updates, track_booking_history]
TRAVEL_SENSITIVE_TOOLS = [cancel_ticket, cancel_accommodation, reschedule_accommodation, reschedule_ticket]
TRAVEL_RUNNABLE = travel_hr_prompt | llm.bind_tools(
    TRAVEL_SAFE_TOOLS + TRAVEL_SENSITIVE_TOOLS + [CompleteOrEscalate]
)