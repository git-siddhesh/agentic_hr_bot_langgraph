from database.utils import db
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from typing import Dict, List, Any

@tool
def sessoion_details(config: RunnableConfig) -> Dict[str, Any]:
    """
    Fetches the user details from the database.

    Returns:
        user_id: The user ID of the user.
        user_name: The name of the user.
        user_type: The type of the user.
    """
    
    configuration = config.get("configurable", {})
    user_id = configuration.get("user_id", None)
    if not user_id:
        raise ValueError("No user ID configured.")

    print("------------- Fetching user details from the DB using user id only-------------")
    user_name = "John Doe" # db.get_user_name(user_id) @TODO: Implement this
    user_type = "DEV_TESTER" # db.get_user_type(user_id) @TODO: Implement this

    return {
        "user_id": user_id,
        "user_name": user_name,
        "user_type": user_type,
    }

