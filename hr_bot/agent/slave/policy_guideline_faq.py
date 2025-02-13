from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from tools.rag import *
from agent.schemas import CompleteOrEscalate

llm = ChatOpenAI(model="gpt-4o-mini")

# Policy Guideline and FAQ Assistant
policy_guideline_faq_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a specialized assistant for providing information on company policies, guidelines, and FAQs. "
            "The primary assistant delegates work to you whenever the user requests information or clarification about policy-related matters. "
            "Your primary responsibilities include looking up policy details, answering frequently asked questions, and providing clear explanations about company rules or procedures. "
            "\n\nWhen searching for policies or answering FAQs, be persistent and ensure the information you provide is accurate and complete. "
            "If you are unable to find the requested information or the user changes their query, escalate the task back to the main assistant. "
            "Your responses should always be clear, concise, and based on verified data from the tools at your disposal. "
            "\n SPECIAL UES CASE: If the user needs some supporing documents to give more analytical support to any results, then you can use the RAG model to generate the documents. "
            "\nCurrent time: {time}."
            "\n\nIf the user needs help, and none of your tools are appropriate for it, then "
            '"CompleteOrEscalate" the dialog to the host assistant. Do not waste the user\'s time. Do not make up invalid tools or functions.',
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)

# Define tools
POLICY_GUIDELINE_FAQ_SAFE_TOOLS = [lookup_policy]
POLICY_GUIDELINE_FAQ_SENSITIVE_TOOLS = []

# Bind tools and create runnable
POLICY_GUIDELINE_FAQ_RUNNABLE = policy_guideline_faq_prompt | llm.bind_tools(
    POLICY_GUIDELINE_FAQ_SAFE_TOOLS + POLICY_GUIDELINE_FAQ_SENSITIVE_TOOLS + [CompleteOrEscalate]
)
