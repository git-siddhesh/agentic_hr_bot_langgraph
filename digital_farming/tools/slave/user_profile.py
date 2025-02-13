from typing import Optional, Dict, Any, List
from datetime import date
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from typing import Dict, List, Any, Optional

@tool
def get_crop_information(
    crop_name: str,
    region: str
) -> Dict[str, Any]:
    """
    Fetches specific crop-related information such as growth cycles, optimal planting times,
    common issues, and pest management for a specific crop in a region.

    Args:
        crop_name: The name of the crop.
        region: The region or climate zone for the crop.

    Returns:
        crop_info: A dictionary with details about the crop's growth cycle, pests, etc.
    """
    return {
        "crop_name": crop_name,
        "region": region,
        "growth_cycle": "6 months",
        "optimal_planting_time": "June to July",
        "common_pests": ["locusts", "aphids"],
        "recommended_fertilizers": ["urea", "NPK"]
    }

@tool
def find_local_suppliers(
    category: str,
    location: str
) -> List[Dict[str, Any]]:
    """
    Search for local suppliers in a specific category (e.g., seeds, fertilizers) and location.

    Args:
        category: The category of supplies (e.g., seeds, fertilizers, tools).
        location: The location or region to search for suppliers.

    Returns:
        suppliers: A list of dictionaries containing information about local suppliers.
    """
    return [
        {
            "supplier_name": "ABC Seeds",
            "category": category,
            "contact": "123-456-7890",
            "address": "123 Farm Road, Location"
        },
        {
            "supplier_name": "XYZ Fertilizers",
            "category": category,
            "contact": "987-654-3210",
            "address": "456 Agricultural Street, Location"
        }
    ]

@tool
def get_market_price(
    crop_name: str,
    region: str
) -> Dict[str, Any]:
    """
    Provides the current market price of a specific crop in a given region.

    Args:
        crop_name: The name of the crop.
        region: The region or market location.

    Returns:
        price_info: A dictionary containing the current market price and potential price fluctuations.
    """
    return {
        "crop_name": crop_name,
        "region": region,
        "current_price_per_kg": 30.5,
        "price_fluctuation": "5% increase in the last week"
    }

@tool
def get_farming_best_practices(
    crop_name: str
) -> str:
    """
    Provides best farming practices related to a specific crop.

    Args:
        crop_name: The name of the crop.

    Returns:
        practices: A string containing detailed farming best practices for the crop.
    """
    return f"Best practices for growing {crop_name}: \n- Ensure proper soil drainage \n- Use organic fertilizers \n- Monitor for pests regularly"

@tool
def get_weather_forecast(
    location: str,
    period: str
) -> Dict[str, Any]:
    """
    Fetches the weather forecast for a specific location and period.

    Args:
        location: The location to get the weather forecast for.
        period: The period for the forecast (e.g., 'weekly', 'daily').

    Returns:
        forecast: A dictionary containing the weather forecast details.
    """
    return {
        "location": location,
        "forecast_period": period,
        "forecast": [
            {"day": "Monday", "weather": "Clear", "temperature": "30°C"},
            {"day": "Tuesday", "weather": "Rainy", "temperature": "28°C"}
        ]
    }

@tool
def search_farming_forum(
    query: str
) -> List[Dict[str, Any]]:
    """
    Searches the farming community forum for discussions related to a query.

    Args:
        query: The query or topic to search for in the forum.

    Returns:
        forum_posts: A list of forum posts related to the query.
    """
    return [
        {
            "post_title": "Best way to plant wheat in rainy season",
            "author": "Farmer123",
            "content": "In the rainy season, you should focus on proper drainage to prevent root rot."
        },
        {
            "post_title": "Dealing with aphid infestations",
            "author": "Farmer456",
            "content": "I found that using neem oil was an effective way to control aphids."
        }
    ]

@tool
def update_farm_profile(
    farmer_id: str,
    profile_data: Dict[str, Any]
) -> str:
    """
    Updates a farmer's profile with new information such as crop history, farm size, and contact details.

    Args:
        farmer_id: The ID of the farmer.
        profile_data: A dictionary containing the updated profile data.

    Returns:
        status: A confirmation message indicating that the profile was updated successfully.
    """
    return f"Farmer {farmer_id}'s profile has been updated successfully."

@tool
def add_emergency_contact(
    farmer_id: str,
    contact_info: Dict[str, Any]
) -> str:
    """
    Adds an emergency contact for a farmer.

    Args:
        farmer_id: The ID of the farmer.
        contact_info: A dictionary containing the contact details of the emergency contact.

    Returns:
        status: A confirmation message indicating the emergency contact was added successfully.
    """
    return f"Emergency contact for Farmer {farmer_id} has been added successfully."

# @tool
# def identify_crop_disease(
#     image_data: bytes
# ) -> str:
#     """
#     Identifies crop diseases or pests from an image.

#     Args:
#         image_data: The image data representing the crop or plant.

#     Returns:
#         diagnosis: A string indicating the disease or pest identified and recommended actions.
#     """
#     return "The image indicates an aphid infestation. Recommended action: Apply neem oil and remove affected leaves."

@tool
def get_training_resources(
    course_type: str
) -> List[Dict[str, Any]]:
    """
    Provides access to available training resources related to farming.

    Args:
        course_type: The type of course (e.g., sustainable farming, irrigation techniques).

    Returns:
        resources: A list of available training courses or certifications.
    """
    return [
        {
            "course_name": "Sustainable Farming Techniques",
            "duration": "6 hours",
            "platform": "AgriLearn",
            "certification": "Yes"
        },
        {
            "course_name": "Advanced Irrigation Methods",
            "duration": "8 hours",
            "platform": "AgriLearn",
            "certification": "Yes"
        }
    ]






@tool
def fetch_farming_data(config: RunnableConfig) -> List[Dict[str, Any]]:
    """Fetch farming-related information (e.g., crop, fertilizer, weather). This is a stub version."""
    configuration = config.get("configurable", {})
    farmer_id = configuration.get("farmer_id", None)
    if not farmer_id:
        raise ValueError("No farmer ID configured.")
    
    # Stub response - In a real implementation, this would query the actual database
    return [
        {
            "crop_name": "Wheat",
            "growth_cycle": "120 days",
            "optimal_planting_time": "March",
            "recommended_fertilizer": "Nitrogen-based",
            "weather_forecast": "Moderate rain expected",
            "market_price": "50 USD/ton"
        },
        {
            "crop_name": "Corn",
            "growth_cycle": "90 days",
            "optimal_planting_time": "April",
            "recommended_fertilizer": "Phosphorus-based",
            "weather_forecast": "Clear skies",
            "market_price": "40 USD/ton"
        }
    ]


@tool
def search_farming_suppliers(
    category: str,
    location: str
) -> List[Dict[str, Any]]:
    """
    Search for local suppliers in a specific category (e.g., seeds, fertilizers) and location.

    Args:
        category: The category of supplies (e.g., seeds, fertilizers, tools).
        location: The location or region to search for suppliers.

    Returns:
        suppliers: A list of dictionaries containing information about local suppliers.
    """
    return [
        {
            "supplier_name": "ABC Seeds",
            "category": category,
            "contact": "123-456-7890",
            "address": "123 Farm Road, Location"
        },
        {
            "supplier_name": "XYZ Fertilizers",
            "category": category,
            "contact": "987-654-3210",
            "address": "456 Agricultural Street, Location"
        }
    ]

@tool
def fetch_crop_market_prices(
    crop_name: str,
    region: str
) -> Dict[str, Any]:
    """
    Provides the current market price of a specific crop in a given region.

    Args:
        crop_name: The name of the crop.
        region: The region or market location.

    Returns:
        price_info: A dictionary containing the current market price and potential price fluctuations.
    """
    return {
        "crop_name": crop_name,
        "region": region,
        "current_price_per_kg": 30.5,
        "price_fluctuation": "5% increase in the last week"
    }

@tool
def fetch_weather_forecast(
    location: str,
    period: str
) -> Dict[str, Any]:
    """
    Fetches the weather forecast for a specific location and period.

    Args:
        location: The location to get the weather forecast for.
        period: The period for the forecast (e.g., 'weekly', 'daily').

    Returns:
        forecast: A dictionary containing the weather forecast details.
    """
    return {
        "location": location,
        "forecast_period": period,
        "forecast": [
            {"day": "Monday", "weather": "Clear", "temperature": "30°C"},
            {"day": "Tuesday", "weather": "Rainy", "temperature": "28°C"}
        ]
    }



@tool
def recommend_farming_courses(
    course_type: str
) -> List[Dict[str, Any]]:
    """
    Provides access to available training resources related to farming.

    Args:
        course_type: The type of course (e.g., sustainable farming, irrigation techniques).

    Returns:
        resources: A list of available training courses or certifications.
    """
    return [
        {
            "course_name": "Sustainable Farming Techniques",
            "duration": "6 hours",
            "platform": "AgriLearn",
            "certification": "Yes"
        },
        {
            "course_name": "Advanced Irrigation Methods",
            "duration": "8 hours",
            "platform": "AgriLearn",
            "certification": "Yes"
        }
    ]
