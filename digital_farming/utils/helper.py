from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda

from langgraph.prebuilt import ToolNode
from typing import Any, Dict, List, Set



def handle_tool_error(state) -> Dict[str, Any]:
    error = state.get("error")
    dialog_state = state.get("dialog_state")
    print(f"ERROR: _______________ in {dialog_state} _______________")
    
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: List) -> Dict[Any, Any]:
    return ToolNode(tools).with_fallbacks([RunnableLambda(handle_tool_error)], exception_key="error")


def _print_event(event: Dict[Any, Any], _printed: Set[Any], max_length:int=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1], flush=True)
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr, flush=True)
            _printed.add(message.id)