from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Annotated, Union

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

class ToTranslationAssistant(BaseModel):
    """Transfers work to a specialized assistant for translating text, converting speech to text, and text-to-speech tasks."""

    text: Optional[str] = Field(
        description="The text that needs to be translated."
    )
    current_language: Optional[str] = Field(
        description="The current language of the text."
    )
    output_language: Optional[str] = Field(
        description="The target language to translate the text into."
    )
    audio_file: Optional[str] = Field(
        default=None,
        description="An optional audio file for speech-to-text conversion or text-to-speech output."
    )

    class Config:
        json_schema_extra: dict[str, dict[str, str]] = {
            "example 1 - text to text transaltion": {
                "text": "For the love of God, Montresor!",
                "current_language": "en",
                "output_language": "es",
                "audio_file": '',
            },
            "example 2 - speech to text": {
                "text": "",
                "current_language": "",
                "output_language": "",
                "audio_file": "audio.mp3",
            },
            "example 3 - text to speech": {
                "text": "Help me identifing the disease in my plant.",
                "current_language": "",
                "output_language": "",
                "audio_file": "audio.mp3",
            },
            "example 3 - text to soeech in target language":  {
                "text": "Help me identifing the disease in my plant.",
                "current_language": "en",
                "output_language": "es",
                "audio_file": "audio.mp3",
            },
        }



class ToImageProcessingAssistant(BaseModel):
    """Transfers work to a specialized assistant for image processing, analysis, and diagnosis tasks."""

    context: str = Field(
        default=None,
        description="context about the image, the user query, or the specific task at hand. Context will be created based on user query and chat history."
    )

    image_path: str = Field(
        description="The path to the image that needs to be analyzed."
    )
    metadata: Dict[str, str]= Field(
        default={},
        description="metadata related to the image, like crop type, location, image name or any other information related to farming and agriculture."
    )

    class Config:
        json_schema_extra: Dict[str, Dict[str, Dict[str, str] | str]] = {
            "example": {
                "image_path": "images\\user_input",
                "context": "My banana plant leaves are turning yellow. Can you help me identify the disease?",
                "metadata": {"crop_type": "banana", "location": "Indore, India"}
            },
            "example 2": {
                "image_path": "images\\user_input",
                "context": "so many yellow bugs on the leaf, what is this?",
                "metadata": {"crop_type": "banana", "location": "Indore, India", "pest_type": "insect"}
            },
        }


