from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import tools_condition

from state.zero_shot import State
from agent.zero_shot import Assistant, part_1_assistant_runnable, part_1_tools
from utils.helper import create_tool_node_with_fallback
from utils.visualize  import plot_graph


builder = StateGraph(State)


# Define nodes: these do the work
builder.add_node("assistant", Assistant(part_1_assistant_runnable))
builder.add_node("tools", create_tool_node_with_fallback(part_1_tools))
# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
memory = MemorySaver()
part_1_graph: CompiledStateGraph = builder.compile(checkpointer=memory)

# Save the graph
plot_graph(part_1_graph, "part_1_graph.png")
