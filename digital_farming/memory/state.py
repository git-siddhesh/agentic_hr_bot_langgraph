from typing import Annotated, Any, Literal, Optional, TypedDict
from typing_extensions import TypedDict, Annotated
from pydantic import BaseModel, model_validator

from langgraph.graph.message import AnyMessage, add_messages, Messages, BaseMessageChunk, MessageLikeRepresentation
from langchain_core.messages import BaseMessage, trim_messages, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


summarization_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an advanced assistant specialized in summarizing the conversation. Your main responsibility is to summarize the conversation based on the context and metadata provided by the user."
            "Keep the one liner summary of each message and provide the summary of the conversation."
            "For example, \n if the agent is transfered to 'ASSISTANT_IMAGE_PROCESSING' then state 'AGENT->ASSISTANT_IMAGE_PROCESSING' \n If some tools is called then state 'AGENT->TOOL_NAME' \n If some error occurs then state 'AGENT->ERROR:error msg' \n If the conversation is ended then state 'AGENT->END'"
            "Keep the factual information in key-value pairs along with the summary."
        ),

        ("placeholder", "{messages}"),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini")

# === Schema Validation === #
class SchemaMessage(BaseModel):
    MESSAGE_THRESHOLD: int
    LAST_K_CONTINUATION_MESSAGES: int 

    @model_validator(mode='before')
    @classmethod
    def validate_threshold(cls, values):
        if values["MESSAGE_THRESHOLD"] < values["LAST_K_CONTINUATION_MESSAGES"]:
            raise ValueError("MESSAGE_THRESHOLD must be greater than LAST_K_CONTINUATION_MESSAGES")
        return values

# === Dialog State Updater === #
def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state based on user action."""
    return left[:-1] if right == "pop" else left + [right] if right else left



# === Summarization Runnable === #
class SummarizationRunnable:
    _instance = None  # Singleton Instance
    counter: int = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.runnable = summarization_prompt | llm | StrOutputParser()
        return cls._instance

    def __call__(self, messages: Messages) -> Messages:
        SummarizationRunnable.counter += 1
        print(f"\n🔄 LLM INVOKED for Summarization ({SummarizationRunnable.counter} times)\n")
        return self.runnable.invoke({"messages": messages})


# === Summarizer === #
class Summarizer:
    counter = 0  # Instance counter
    def __init__(self, config: SchemaMessage) -> None:
        self.config = config
        self.Summarize = SummarizationRunnable()

    def __call__(self, left: Messages, right: Messages) -> Messages:
        self.counter += 1
        print(f"📝 STATE UPDATE CALLED ({self.counter} times)")
        return self.custom_add_messages(left, right)

    def custom_add_messages(self, left: Messages, right: Messages) -> Messages:
        updated_messages = add_messages(left, right)

        if len(updated_messages) > self.config.MESSAGE_THRESHOLD: # and Summarizer.counter % 2 == 0:
            print("\n⚡ MESSAGE LENGTH EXCEEDED: Summarizing Messages...\n")
            past_messages = updated_messages[:-self.config.LAST_K_CONTINUATION_MESSAGES]
            summary = self.Summarize(past_messages)
            print(f"\n☑️ SUMMARY: {summary}\n")
            summarized_part =  SystemMessage(content=summary, id=past_messages[-1].id)
            updated_messages = add_messages(summarized_part, updated_messages[-self.config.LAST_K_CONTINUATION_MESSAGES:])
        
        return updated_messages


# === State Management === #
class State(TypedDict):
    messages: Annotated[list["AnyMessage"], Summarizer(SchemaMessage(MESSAGE_THRESHOLD=15, LAST_K_CONTINUATION_MESSAGES=4))]
    user_info: str
    metadata: dict[str, str]
    dialog_state: Annotated[
        list[
            Literal[
                "assistant",
                "ASSISTANT_PRIMARY",
                "ASSISTANT_IMAGE_PROCESSING",
                "ASSISTANT_TRANSLATION",
                "ASSISTANT_USER_PROFILE",
                "ASSISTANT_POLICY_GUIDELINE_FAQ",
                "pop",
            ]
        ],
        update_dialog_stack,
    ]
