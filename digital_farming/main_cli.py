import sys
sys.path.append('.')

# Let's create an example conversation a user might have with the assistant
tutorial_questions = [
    "Hi there, what time is my flight?",
    "Am i allowed to update my flight to something sooner? I want to leave later today.",
    "Update my flight to sometime next week then",
    "The next available option is great",
    "what about lodging and transportation?",
    "Yeah i think i'd like an affordable hotel for my week-long stay (7 days). And I'll want to rent a car.",
    "OK could you place a reservation for your recommended hotel? It sounds nice.",
    "yes go ahead and book anything that's moderate expense and has availability.",
    "Now for a car, what are my options?",
    "Awesome let's just get the cheapest option. Go ahead and book for 7 days",
    "Cool so now what recommendations do you have on excursions?",
    "Are they available while I'm there?",
    "interesting - i like the museums, what options are there? ",
    "OK great pick one and book it for my second day there.",
]


retrieval_questions = """
What is the company’s leave policy?
Can you explain the reimbursement guidelines?
Where can I find the company travel policy?
What are the rules for remote work eligibility?
Could you help me find the policy on expense approvals?
"""

hiring_questions = """
Can you schedule an interview for a shortlisted candidate?
What’s the current status of the candidate I referred?
How do I post a job opening for my department?
Can you help me shortlist candidates for the "JUNIOR PROMPT ENGINEER" role? 
Generate a hiring report for this month. 
How do I initiate the onboarding process for a new hire? 
Collect feedback from the panel about the last interview. 
I need to reschedule the interview for "SIDDHESH". Can you do that?
Can you generate an offer letter for the selected candidate?
"""

leave_questions = """
How do I apply for leave?
What’s the status of my leave request?
Can you cancel my leave request for "25/01/2025"?
How many leave days do I have left?
Can you calculate my leave encashment for this year?
I need to modify my leave request to include "26/01/2025". Can you help?
"""

payslip_questions = """
Can you get me my payslip for "JANUARY"?
What are the deductions on my last paycheck? 
Can you provide me a detailed breakdown of my salary? 
What are my tax details for this financial year?
"""

reimbursement_questions = """
What’s the status of my reimbursement request?
How do I submit a reimbursement request for my travel expenses?
Can you cancel my reimbursement request for "LED PURCHAGE"?
"""

travel_questions = """
Can you book a flight for me to "JAIPUR" on "25/01/2025"?
I need to cancel my flight ticket for "JAIPUR". Can you do that?
What’s the status of my flight booking?
Can you find me accommodation in "JAIPUR" for "26/01/2025"? 
Can you book a hotel for me near "AJMER"? 
I need to cancel my hotel reservation. Can you help? 
Can you provide me a summary of my bookings? 
Generate an itinerary for my trip to "JAIPUR TO UDAIPUR". 
What’s the status of my hotel booking? 
Notify me if there are any updates on my travel bookings. 
Can you track my past travel bookings? 
I need to reschedule my flight to "01/02/2025". Can you help?
Reschedule my hotel stay to start from "02/02/2025". 
"""

user_profile_questions = """
Can you search for "AJAY SINGH" in the directory? 
What are the directory stats for our team? 
Can you verify my profile details? 
Show me my profile information. 
Update my profile to include "BLOOD GROUP AS O+". 
Send a message to "AJAY SINGH". 
How do I register a new employee in the system? 
Can you deactivate the profile for "AJAY SINGH" who has left the company? 
Generate a contact list for my department. 
Add "YATHARTH" as my emergency contact.
""" 

session_questions = """
Can you provide the details of my current session?
What actions have been taken in this session so far?
Can you summarize today’s chat?
How do I access the details of previous sessions?
"""


import uuid
thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        "user_id": "3",
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}

from graph.main import GRAPH
# from utils.visualize import plot_graph
# plot_graph(GRAPH, "HR_BOT_GRAPH.png", display_graph=False)
from utils.helper import _print_event
from langchain_core.messages import ToolMessage
# Update with the backup file so we can restart from the original place in each section
# db = update_dates(db)

_printed = set()

# def run_bot(question_set):
    # We can reuse the tutorial questions from part 1 to see how it does.
    # for question in question_set:


def endpoint(text= "", image_path="", audio_path=""):

    if text:
        question = text
    elif image_path:
        question = "input image uploaded at: " + image_path
    elif audio_path:
        question = "input audio uploaded at: " + audio_path

    events = GRAPH.stream({"messages": ("user", question)}, config, stream_mode="values")
    for event in events:
        _print_event(event, _printed)
    snapshot = GRAPH.get_state(config)

    while snapshot.next:
        # We have an interrupt! The agent is trying to use a tool, and the user can approve or deny it
        # Note: This code is all outside of your graph. Typically, you would stream the output to a UI.
        # Then, you would have the frontend trigger a new run via an API call when the user has provided input.
        try:
            user_input = input("Do you approve of the above actions? Type 'y' to continue; \notherwise, explain your requested changed.\n\n")
        except:
            user_input = "y"
        if user_input.strip() == "y":
            # Just continue
            result = GRAPH.invoke(
                None,
                config,
            )
        else:
            # Satisfy the tool invocation by
            # providing instructions on the requested changes / change of mind
            result = GRAPH.invoke(
                {
                    "messages": [
                        ToolMessage(
                            tool_call_id=event["messages"][-1].tool_calls[0]["id"],
                            content=f"API call denied by user. Reasoning: '{user_input}'. Continue assisting, accounting for the user's input.",
                        )
                    ]
                },
                config,
            )
        snapshot = GRAPH.get_state(config)

    return snapshot.values["messages"][-1].content 


while True:
    user_input = input("Enter your question: ")
    print(endpoint(user_input))


# print(endpoint("What is the company’s leave policy?"))


# run_bot(travel_questions.strip().split("\n"))
# run_bot(reimbursement_questions.strip().split("\n"))
# run_bot(payslip_questions.strip().split("\n"))
# run_bot(leave_questions.strip().split("\n"))
# run_bot(hiring_questions.strip().split("\n"))
# run_bot(retrieval_questions.strip().split("\n"))
# run_bot(user_profile_questions.strip().split("\n"))
