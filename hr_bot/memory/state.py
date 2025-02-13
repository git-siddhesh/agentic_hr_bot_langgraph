from typing import Annotated, Literal, Optional

from typing_extensions import TypedDict

from langgraph.graph.message import AnyMessage, add_messages


def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state."""
    if right is None:
        return left
    if right == "pop":
        return left[:-1]
    return left + [right]


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    # TODO: summarise the older messages above the threshold number of messages
    user_info: str
    dialog_state: Annotated[
        list[
            Literal[
                "assistant",
                "ASSISTANT_PRIMARY",

                "ASSISTANT_HIRING",
                "ASSISTANT_LEAVE",
                "ASSISTANT_PAYSLIP",
                "ASSISTANT_REIMBURSEMENT",
                "ASSISTANT_USER_PROFILE",
                "ASSISTANT_TRAVEL",
                "ASSISTANT_POLICY_GUIDELINE_FAQ",

                "pop",
            ]
        ],
        update_dialog_stack,
    ]


## DIALOG STATE

# "assistant",
# "update_flight",
# "ASSISTANT_LEAVE",
# "ASSISTANT_PAYSLIP",
# "ASSISTANT_REIMBURSEMENT",

# "pop"


# "primary_assistant",

