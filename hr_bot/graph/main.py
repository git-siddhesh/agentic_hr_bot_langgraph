from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from utils.visualize import plot_graph
from utils.helper import create_tool_node_with_fallback
from memory.state import State

from agent import *
print("------------")
from graph.util import create_entry_node, pop_dialog_state, user_info
from graph.config import assistant_config
from graph.routing import route_primary_assistant, route_to_workflow


import time

class AgenticGraph():
    def __init__(self, state) -> None:
        self.state = state
        self.app = StateGraph(state)
        self.memory = MemorySaver()
        self.initialize_graph()

    def add_node(self):
        #_______________________________________________________________________________________
        # START NODE

        self.app.add_node("USER_INFO", user_info)

        #_______________________________________________________________________________________
        # ENTRY NODES
        for assistant, config in assistant_config.items():
            self.app.add_node(f"DELEGATE_{assistant}_ASSISTANT", create_entry_node(config["name"], f"ASSISTANT_{assistant}"))

        #_______________________________________________________________________________________
        # ASSISTANT NODE

        ## MASTER ASSISTANT
        self.app.add_node("ASSISTANT_PRIMARY", Assistant(ASSISTANT_RUNNABLE))
        ## SlAVE ASSISTANT
        for assistant, config in assistant_config.items():
            self.app.add_node(f"ASSISTANT_{assistant}", Assistant(globals()[f"{assistant}_RUNNABLE"]))

        #_______________________________________________________________________________________
        # TOOL NODES
        for assistant, config in assistant_config.items():
            self.app.add_node(f"{assistant}_SAFE_TOOLS", create_tool_node_with_fallback(config["safe_tools"]))
            self.app.add_node(f"{assistant}_SENSITIVE_TOOLS", create_tool_node_with_fallback(config["sensitive_tools"]))


        ## PRIMARY TOOLS
        self.app.add_node("PRIMARY_ASSISTANT_TOOLS", create_tool_node_with_fallback(PRIMARY_ASSISTANT_TOOLS))

        #_______________________________________________________________________________________
        # LEAVE NODE
        self.app.add_node("DEPENDENCY", pop_dialog_state)

        #_______________________________________________________________________________________
        # END NODE

    #_______________________________________________________________________________________
    # EDGES
    def add_direct_edge(self):

        ## DIRECT EDGES:
        self.app.add_edge(START, "USER_INFO")
        self.app.add_edge("DEPENDENCY", "ASSISTANT_PRIMARY")
        self.app.add_edge("PRIMARY_ASSISTANT_TOOLS", "ASSISTANT_PRIMARY")

        for assistant in assistant_config.keys():
            self.app.add_edge(f"DELEGATE_{assistant}_ASSISTANT", f"ASSISTANT_{assistant}")
            self.app.add_edge(f"{assistant}_SAFE_TOOLS", f"ASSISTANT_{assistant}")
            self.app.add_edge(f"{assistant}_SENSITIVE_TOOLS", f"ASSISTANT_{assistant}")
    
    def add_conditional_edge(self):
        #______________________________
        # CONDITIONAL EDGES

        ## SLAVE ASSISTANT EDGES

        for assistant, config in assistant_config.items():
            self.app.add_conditional_edges(
                f"ASSISTANT_{assistant}",
                config["routing_function"],
                [f"{assistant}_SAFE_TOOLS", f"{assistant}_SENSITIVE_TOOLS", "DEPENDENCY", END],
            )

        ## MASTER ASSISTANT EDGES
        self.app.add_conditional_edges(
            "ASSISTANT_PRIMARY",
            route_primary_assistant,
            [
                "PRIMARY_ASSISTANT_TOOLS",
                *[f"DELEGATE_{key}_ASSISTANT" for key in assistant_config.keys()],
                END,
            ],
        )


        ## User Info Routing
        self.app.add_conditional_edges(
            "USER_INFO",
            route_to_workflow,
            ["ASSISTANT_PRIMARY", *[f"ASSISTANT_{key}" for key in assistant_config.keys()]],
        )
    
    def compile_graph(self):
        #______________________________
        # Compile graph
  
        print("Compiling the graph...")
        self.GRAPH = self.app.compile(
            checkpointer=self.memory,
            interrupt_before=[f"{key}_SENSITIVE_TOOLS" for key in assistant_config.keys()],     # Let the user self.approve or deny the use of sensitive tools
        )
        print("Graph compiled successfully.")


    def visualize_graph(self, display_graph=False):
        #______________________________
        # Visualize the graph
        print("Visualizing the graph...")
        plot_graph(self.GRAPH, "HR_BOT_GRAPH.png", display_graph=display_graph)
        print("Graph visualized successfully.")

    def initialize_graph(self):
        st = time.time()
        self.add_node()
        st1 =  time.time()
        print("ADDING NODES took ", st1-st, " seconds")
        self.add_direct_edge()
        st = time.time()
        print("ADDING DIRECT EDGES took ", st-st1, " seconds")
        self.add_conditional_edge()
        st1 = time.time()
        print("ADDING CONDITIONAL EDGES took ", st1-st, " seconds")
        self.compile_graph()
        print("COMPILING GRAPH took ", time.time()-st1, " seconds\n\n")

       

#_______________________________________________________________________________________
print("Initializing the graph...")
GRAPH = AgenticGraph(State).GRAPH