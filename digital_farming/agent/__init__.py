import time
st = time.time()
print("Defining agent schemas...")
from agent.schemas import (
    ToImageProcessingAssistant,
    ToTranslationAssistant,
    ToUserProfileAssistant,
    CompleteOrEscalate,
    ToPolicyGuideLineFAQAssistant
)
pt =  time.time()
print("Time taken to define agent schemas: ",pt-st)
print("Importing base agents...")
from agent.base import Assistant
et = time.time()
print("Time taken to import base agents: ", et-st)

print("Initializing agents...")
from agent.runnables.image_processing import (
    IMAGE_PROCESSING_RUNNABLE
)

from agent.runnables.translation import (
    TRANSLATION_RUNNABLE
)

from agent.runnables.user_profile import (
    USER_PROFILE_RUNNABLE
)

from agent.runnables.policy_guideline_faq import (
    POLICY_GUIDELINE_FAQ_RUNNABLE
)

from agent.master.primary import (
    ASSISTANT_RUNNABLE
)




print("Time taken to import all the agents: ", time.time()-et)

__all__ = [
    "ToImageProcessingAssistant",
    "ToTranslationAssistant",

    "ToUserProfileAssistant",
    "Assistant",
    "CompleteOrEscalate",
    "ToPolicyGuideLineFAQAssistant",

    "IMAGE_PROCESSING_RUNNABLE",
    "TRANSLATION_RUNNABLE",
    "USER_PROFILE_RUNNABLE",
    "POLICY_GUIDELINE_FAQ_RUNNABLE",
    "ASSISTANT_RUNNABLE",


]