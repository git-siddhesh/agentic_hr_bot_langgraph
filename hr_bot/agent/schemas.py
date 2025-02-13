from pydantic import BaseModel, Field

class CompleteOrEscalate(BaseModel):
    """A tool to mark the current task as completed and/or to escalate control of the dialog to the main assistant,
    who can re-route the dialog based on the user's needs."""

    cancel: bool = True
    reason: str

    class Config:
        json_schema_extra = {
            "example": {
                "cancel": True,
                "reason": "User changed their mind about the current task.",
            },
            "example 2": {
                "cancel": True,
                "reason": "I have fully completed the task.",
            },
            "example 3": {
                "cancel": False,
                "reason": "I need to search the user's emails or calendar for more information.",
            },
        }

class ToPolicyGuideLineFAQAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle policy lookup and FAQ-related tasks."""

    request: str = Field(
        description="Any necessary followup questions the policy assistant should clarify before proceeding."
    )
    class Config:
        json_schema_extra: dict[str, dict[str, str]] = {
            "example": {
                "request": "I would like to know the policy on parental leave.",
            }
        }


class ToHiringAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle hiring-related tasks."""

    user_id: str = Field(
        description="The unique identifier of the user profile to be accessed."
    )
    request: str = Field(
        description="Any necessary followup questions the hiring assistant should clarify before proceeding."
    )
    class Config:
        json_schema_extra: dict[str, dict[str, str]] = {
            "example": {
                "user_id": "12345",
                "request": "I would like to schedule an interview for this candidate.",
            }
        }

class ToLeaveAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle leave-related tasks."""

    user_id: str = Field(
        description="The unique identifier of the user profile to be accessed."
    )
    request: str = Field(
        description="Any necessary followup questions the leave assistant should clarify before proceeding."
    )
    class Config:
        json_schema_extra: dict[str, dict[str, str]] = {
            "example": {
                "user_id": "12345",
                "request": "I would like to apply for leave for next week.",
            }
        }

class ToPayslipAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle payslip-related tasks."""

    user_id: str = Field(
        description="The unique identifier of the user profile to be accessed."
    )
    request: str = Field(
        description="Any necessary followup questions the payslip assistant should clarify before proceeding."
    )
    class Config:   
        json_schema_extra: dict[str, dict[str, str]] = {
            "example": {
                "user_id": "12345",
                "request": "I would like to view my payslip for this month.",
            }
        }

class ToReimbursementAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle reimbursement-related tasks."""

    user_id: str = Field(
        description="The unique identifier of the user profile to be accessed."
    )
    request: str = Field(
        description="Any necessary followup questions the reimbursement assistant should clarify before proceeding."
    )
    class Config:
        json_schema_extra: dict[str, dict[str, str]] = {
            "example": {
                "user_id": "12345",
                "request": "I would like to submit a reimbursement request for my travel expenses.",
            }
        }

class ToTravelAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle travel-related tasks."""

    user_id: str = Field(
        description="The unique identifier of the user profile to be accessed."
    )
    location: str = Field(
        description="The location where the user wants to travel."
    )
    request: str = Field(
        description="Any necessary followup questions the travel assistant should clarify before proceeding."
    )
    class Config:
        json_schema_extra: dict[str, dict[str, str]] = {
            "example": {
                "user_id": "12345",
                "location": "Paris",
                "request": "I would like to book a flight to Paris for next month.",
            }
        }

class ToUserProfileAssistant(BaseModel):
    """Transfers work to a specialized assistant to handle user profile-related tasks."""

    user_id: str = Field(
        description="The unique identifier of the user profile to be accessed."
    )
    request: str = Field(
        description="Any necessary followup questions the user profile assistant should clarify before proceeding."
    )
    class Config:
        json_schema_extra: dict[str, dict[str, str]] = {
            "example": {
                "user_id": "12345",
                "request": "I would like to update my contact information.",
            }
        }


