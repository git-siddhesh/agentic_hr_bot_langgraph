from typing import Dict, List, Any
from agent import *
from graph.util import *
from graph.routing import *

assistant_config: Dict[str, Dict[str, Any]] = {
    "IMAGE_PROCESSING": {
        "name": "Image Processing Assistant",
        "routing_function": route_image_processing,
        "safe_tools": IMAGE_PROCESSING_SAFE_TOOLS,
        "sensitive_tools": IMAGE_PROCESSING_SENSITIVE_TOOLS,
    },


    "USER_PROFILE": {
        "name": "User Profile Assistant",
        "routing_function": route_user_profile,
        "safe_tools": USER_PROFILE_SAFE_TOOLS,
        "sensitive_tools": USER_PROFILE_SENSITIVE_TOOLS,
    },

    "POLICY_GUIDELINE_FAQ": {
        "name": "Policy & Guideline FAQ retrieval Assistant",
        "routing_function": route_policy_guide_line_faq,
        "safe_tools": POLICY_GUIDELINE_FAQ_SAFE_TOOLS,
        "sensitive_tools": POLICY_GUIDELINE_FAQ_SENSITIVE_TOOLS,
    },
    # "TRANSLATION": {
    #     "name": "Text Processing Assistant",
    #     "routing_function": route_translation,
    #     "safe_tools": TRANSLATION_SAFE_TOOLS,
    #     "sensitive_tools": TRANSLATION_SENSITIVE_TOOLS
    # },
}