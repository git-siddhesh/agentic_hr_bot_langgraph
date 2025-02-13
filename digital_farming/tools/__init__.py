import time
print("intializing tools")
st = time.time()
from tools.rag import lookup_policy
from tools.chat_session import sessoion_details
from tools.slave.image_processing import instruction_generation_for_image_diagnosis, analyze_detect_classify_image
from tools.slave.translation import translate_text, tts, stt
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List, Any


from tools.slave.user_profile import (
    get_crop_information, 
    find_local_suppliers,
    get_market_price,
    get_farming_best_practices,
    get_weather_forecast,
    search_farming_forum,
    update_farm_profile,
    add_emergency_contact,
    get_training_resources,
    fetch_farming_data,
    search_farming_suppliers,
    fetch_crop_market_prices,
    fetch_weather_forecast,
    recommend_farming_courses
)


IMAGE_PROCESSING_SAFE_TOOLS = [instruction_generation_for_image_diagnosis, analyze_detect_classify_image]
IMAGE_PROCESSING_SENSITIVE_TOOLS = []

TRANSLATION_SAFE_TOOLS = [translate_text, tts, stt]
TRANSLATION_SENSITIVE_TOOLS = []

USER_PROFILE_SAFE_TOOLS = [
    lookup_policy,     
    get_crop_information, 
    find_local_suppliers,
    get_market_price,
    get_farming_best_practices,
    get_weather_forecast,
    search_farming_forum, 
    get_training_resources,
    fetch_farming_data,
    search_farming_suppliers,
    fetch_crop_market_prices,
    fetch_weather_forecast,
    recommend_farming_courses
]
USER_PROFILE_SENSITIVE_TOOLS = [ 
    update_farm_profile,
    add_emergency_contact
]

POLICY_GUIDELINE_FAQ_SAFE_TOOLS = [lookup_policy]
POLICY_GUIDELINE_FAQ_SENSITIVE_TOOLS = []

PRIMARY_ASSISTANT_TOOLS = [
    TavilySearchResults(max_results=1),
    lookup_policy,  # Access farming policies and guidelines
    fetch_farming_data,  # Fetch farming-related information (stub function for now)
    fetch_weather_forecast,  # for weather information
    search_farming_suppliers,  # for finding local suppliers  
    get_market_price,  # for current market prices
    translate_text,
    tts,
    stt
]

SAFE_TOOLS: List[Any] = [
    *IMAGE_PROCESSING_SAFE_TOOLS,
    *TRANSLATION_SAFE_TOOLS,
    *USER_PROFILE_SAFE_TOOLS,
    *POLICY_GUIDELINE_FAQ_SAFE_TOOLS
]

SENSITIVE_TOOLS: List[Any] = [
    *IMAGE_PROCESSING_SENSITIVE_TOOLS,
    *TRANSLATION_SENSITIVE_TOOLS,
    *USER_PROFILE_SENSITIVE_TOOLS,
    *POLICY_GUIDELINE_FAQ_SENSITIVE_TOOLS
]




print("tools intialized in", time.time()-st)
__all__: List[str] = [
    "lookup_policy",
    "sessoion_details",
    "instruction_generation_for_image_diagnosis",
    "analyze_detect_classify_image",
    "translate_text",
    "tts",
    "stt",
    "get_crop_information",
    "find_local_suppliers",
    "get_market_price",
    "get_farming_best_practices",
    "get_weather_forecast",
    "search_farming_forum",
    "update_farm_profile",
    "add_emergency_contact",
    "get_training_resources",
    "fetch_farming_data",
    "search_farming_suppliers",
    "fetch_crop_market_prices",
    "fetch_weather_forecast",
    "recommend_farming_courses",
    
    "TavilySearchResults",
    "IMAGE_PROCESSING_SAFE_TOOLS",
    "IMAGE_PROCESSING_SENSITIVE_TOOLS",
    "TRANSLATION_SAFE_TOOLS",
    "TRANSLATION_SENSITIVE_TOOLS",
    "USER_PROFILE_SAFE_TOOLS",
    "USER_PROFILE_SENSITIVE_TOOLS",
    "POLICY_GUIDELINE_FAQ_SAFE_TOOLS",
    "POLICY_GUIDELINE_FAQ_SENSITIVE_TOOLS",
    "PRIMARY_ASSISTANT_TOOLS",

    "SAFE_TOOLS",
    "SENSITIVE_TOOLS"
]