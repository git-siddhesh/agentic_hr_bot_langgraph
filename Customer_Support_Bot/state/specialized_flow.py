from typing import Annotated, Literal, Optional

from typing_extensions import TypedDict

from langgraph.graph.message import AnyMessage, add_messages



from typing import Annotated, Any, Literal, Optional, Sequence
from typing_extensions import TypedDict, Annotated

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
        ),

        ("placeholder", "{messages}"),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini")

class SummarizationRunnable:
    counter : int = 0
    def __init__(self, runnable):
        self.runnable = runnable

    def invoke(self, *args: Any, **kwds: Any) -> Any:
        
        print("_________________________")
        SummarizationRunnable.counter +=1
        print(args)
        print(kwds)
        print(f"LLM INVOKED {SummarizationRunnable.counter} times")
        print("_________________________")
        result = self.runnable.invoke(*args, **kwds)
        print(result)
        return result

# from langchain_core.runnables import RunnableSequence
SUMMARIZATION_RUNNABLE  = summarization_prompt | llm | StrOutputParser()




def summarize_messages(messages: Messages) -> Messages:
    """Summarizes a list of messages using an LLM."""
    last_id = messages[-1].id
    text_to_summarize = "\n".join([msg.content for msg in messages])
    # summary = SUMMARIZATION_RUNNABLE.invoke({"messages": text_to_summarize})
    summary = SummarizationRunnable(SUMMARIZATION_RUNNABLE).invoke({"messages": messages})
    # return BaseMessage(content=summary, id=last_id)
    return SystemMessage(content=summary, id=last_id)

    

MESSAGE_THRESHOLD = 3
LAST_K_CONTINUATION_MESSAGES = 1

def custom_add_messages(left: Messages, right: Messages) -> Messages :
    """
    Custom version of add_messages that summarizes messages if their length exceeds a threshold.
    """

    print("+++++++++++++++++++++++++++++++++++++++")
    print(type(left),left)
    print("---------------------------------------")
    print(type(right),right)
    print("+++++++++++++++++++++++++++++++++++++++")

    updated_messages: Messages = add_messages(left, right)
    
    # if len(updated_messages) > MESSAGE_THRESHOLD:
    #     print("################################# !!! MESSAGE LEMGTH INCREASES !!! #################################")
    #     summarized_part: Messages = summarize_messages(updated_messages[:-LAST_K_CONTINUATION_MESSAGES])  # Summarize first N-3 messages
    #     updated_messages: Messages = add_messages(summarized_part, updated_messages[-LAST_K_CONTINUATION_MESSAGES:])
    #     print(updated_messages)
    #     print("################################# !!! MESSAGE LEMGTH INCREASES !!! #################################")
    
    print("#######            updated_messages                ########")
    for message in updated_messages:
        print(message)
        print()
    # print(updated_messages)
    print("#######--------------------------------------------########")

    return updated_messages



def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state."""
    if right is None:
        return left
    if right == "pop":
        return left[:-1]
    return left + [right]


class State(TypedDict):
    messages: Annotated[list[AnyMessage], custom_add_messages]
    # messages: Annotated[list[AnyMessage], add_messages]
    user_info: str
    dialog_state: Annotated[
        list[
            Literal[
                "assistant",
                "update_flight",
                "book_car_rental",
                "book_hotel",
                "book_excursion",
            ]
        ],
        update_dialog_stack,
    ]




