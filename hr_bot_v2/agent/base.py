from langchain_core.messages.ai import  AIMessageChunk
from langchain_core.messages.chat import  ChatMessageChunk
from langchain_core.messages.function import  FunctionMessageChunk
from langchain_core.messages.human import  HumanMessageChunk
from langchain_core.messages.system import  SystemMessageChunk
from langchain_core.messages.tool import  ToolMessageChunk
from langchain_core.runnables import Runnable, RunnableConfig

from langgraph.graph.message import AnyMessage

from memory.state import State
from tools import *

# The top-level assistant performs general Q&A and delegates specialized tasks to other assistants.
# The task delegation is a simple form of semantic routing / does simple intent detection

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)

            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                # messages: list[tuple[str, str] | AIMessage | HumanMessage | ChatMessage | SystemMessage | FunctionMessage | ToolMessage | AIMessageChunk | HumanMessageChunk | ChatMessageChunk | SystemMessageChunk | FunctionMessageChunk | ToolMessageChunk] = state["messages"] + [("user", "Respond with a real output.")]
                messages: list[tuple[str, str] | AnyMessage |  AIMessageChunk | HumanMessageChunk | ChatMessageChunk | SystemMessageChunk | FunctionMessageChunk | ToolMessageChunk] = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}
