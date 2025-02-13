from typing import Literal

from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition


from tools import *
# from agent.specialized import *

from utils.visualize import plot_graph
from utils.helper import create_tool_node_with_fallback
from state.specialized_flow import State

from graph.specialized.util import *

builder = StateGraph(State)

#______________________________
# START NODE

builder.add_node("fetch_user_info", user_info)

#______________________________
# ENTRY NODE
builder.add_node("enter_update_flight", create_entry_node("Flight Updates & Booking Assistant", "update_flight"))
builder.add_node("enter_book_car_rental", create_entry_node("Car Rental Assistant", "book_car_rental"))
builder.add_node("enter_book_hotel", create_entry_node("Hotel Booking Assistant", "book_hotel"))
builder.add_node("enter_book_excursion",create_entry_node("Trip Recommendation Assistant", "book_excursion"))

#______________________________
# ASSISTANT NODE

## MASTER ASSISTANT
builder.add_node("primary_assistant", Assistant(assistant_runnable))

## SlAVE ASSISTANT
builder.add_node("update_flight", Assistant(update_flight_runnable))
builder.add_node("book_car_rental", Assistant(book_car_rental_runnable))
builder.add_node("book_hotel", Assistant(book_hotel_runnable))
builder.add_node("book_excursion",  Assistant(book_excursion_runnable))

#______________________________
# TOOL NODE
## FLIGHT TOOL
builder.add_node("update_flight_sensitive_tools",create_tool_node_with_fallback(update_flight_sensitive_tools))
builder.add_node("update_flight_safe_tools",create_tool_node_with_fallback(update_flight_safe_tools))
## CAR RENTAL TOOL
builder.add_node("book_car_rental_safe_tools",create_tool_node_with_fallback(book_car_rental_safe_tools))
builder.add_node("book_car_rental_sensitive_tools", create_tool_node_with_fallback(book_car_rental_sensitive_tools))
## HOTEL BOOKING TOOL
builder.add_node("book_hotel_safe_tools", create_tool_node_with_fallback(book_hotel_safe_tools))
builder.add_node("book_hotel_sensitive_tools",create_tool_node_with_fallback(book_hotel_sensitive_tools))
## EXCURSION TOOL
builder.add_node("book_excursion_safe_tools",create_tool_node_with_fallback(book_excursion_safe_tools))
builder.add_node("book_excursion_sensitive_tools",create_tool_node_with_fallback(book_excursion_sensitive_tools))
## PRIMARY TOOLS
builder.add_node("primary_assistant_tools", create_tool_node_with_fallback(primary_assistant_tools))

#______________________________
# LEAVE NODE
builder.add_node("DEPENDENCY", pop_dialog_state)

#______________________________
# END NODE



#______________________________
# EDGES

## DIRECT EDGES:

builder.add_edge(START, "fetch_user_info")

builder.add_edge("enter_update_flight", "update_flight")
builder.add_edge("update_flight_sensitive_tools", "update_flight")
builder.add_edge("update_flight_safe_tools", "update_flight")

builder.add_edge("enter_book_car_rental", "book_car_rental")
builder.add_edge("book_car_rental_sensitive_tools", "book_car_rental")
builder.add_edge("book_car_rental_safe_tools", "book_car_rental")

builder.add_edge("enter_book_hotel", "book_hotel")
builder.add_edge("book_hotel_sensitive_tools", "book_hotel")
builder.add_edge("book_hotel_safe_tools", "book_hotel")

builder.add_edge("enter_book_excursion", "book_excursion")
builder.add_edge("book_excursion_sensitive_tools", "book_excursion")
builder.add_edge("book_excursion_safe_tools", "book_excursion")


builder.add_edge("DEPENDENCY", "primary_assistant")
builder.add_edge("primary_assistant_tools", "primary_assistant")



#______________________________
# CONDITIONAL EDGES

builder.add_conditional_edges(
    "update_flight",
    route_update_flight,
    ["update_flight_sensitive_tools", "update_flight_safe_tools", "DEPENDENCY", END],
)



builder.add_conditional_edges(
    "book_car_rental",
    route_book_car_rental,
    [
        "book_car_rental_safe_tools",
        "book_car_rental_sensitive_tools",
        "DEPENDENCY",
        END,
    ],
)


builder.add_conditional_edges(
    "book_hotel",
    route_book_hotel,
    ["DEPENDENCY", "book_hotel_safe_tools", "book_hotel_sensitive_tools", END],
)



builder.add_conditional_edges(
    "book_excursion",
    route_book_excursion,
    ["book_excursion_safe_tools", "book_excursion_sensitive_tools", "DEPENDENCY", END],
)


# The assistant can route to one of the delegated assistants,
# directly use a tool, or directly respond to the user
builder.add_conditional_edges(
    "primary_assistant",
    route_primary_assistant,
    [
        "enter_update_flight",
        "enter_book_car_rental",
        "enter_book_hotel",
        "enter_book_excursion",
        "primary_assistant_tools",
        END,
    ],
)


builder.add_conditional_edges("fetch_user_info", route_to_workflow)



#______________________________
# Compile graph
memory = MemorySaver()
part_4_graph = builder.compile(
    checkpointer=memory,
    # Let the user approve or deny the use of sensitive tools
    interrupt_before=[
        "update_flight_sensitive_tools",
        "book_car_rental_sensitive_tools",
        "book_hotel_sensitive_tools",
        "book_excursion_sensitive_tools",
    ],
)

# Save the graph

plot_graph(part_4_graph, "part_4_graph.png")

############ CAR RENTAL ASSISTANT ############
############ PRIMARY ASSISTANT ############
############ Excurions ASSISTANT ############
############ HOTEL BOOKING ASSISTANT ############
############ FLIGHT ASSISTANT ############