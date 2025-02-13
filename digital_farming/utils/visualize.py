from IPython.display import Image, display
from langgraph.graph.state import CompiledStateGraph
from typing import Any

import os

import os
from typing import Any
from PIL import Image as PILImage
from IPython.display import display, Image

def plot_graph(graph: CompiledStateGraph, save_path: Any = None, display_graph: bool = True):
    """
    Generates a graph image from a graph object, displays it in the notebook, 
    and optionally saves it to a file.

    Args:
        graph: The graph object to render.
        save_path (str, optional): File path to save the graph image (e.g., 'graph.png').
        display_graph (bool, optional): Whether to display the graph in the notebook. Defaults to True.
    
    Returns:
        str: The file path of the saved image if saved, otherwise None.
    """
    try:
        # Configure the graph rendering with increased dimensions and resolution
        graph_image = graph.get_graph(xray=True).draw_mermaid_png()
              # scale=2 for higher clarity

        # Save the graph to a file if a save path is provided
        if save_path:
            save_path: str = os.path.join("images", "graphs", save_path)
            with open(save_path, "wb") as f:
                f.write(graph_image)
            print(f"Graph saved to {save_path}", flush=True)
        else:
            save_path = os.path.join("images", "graphs", f"{graph.name}.png")
            with open(save_path, "wb") as f:
                f.write(graph_image)

        # Display the graph in the notebook if requested
        if display_graph:
            # Use PIL to resize the image for better dimensions
            with open(save_path, "rb") as f:
                pil_image = PILImage.open(f)
                resized_image = pil_image.resize(
                    (int(pil_image.width * 1.5), int(pil_image.height * 1.5)), PILImage.LANCZOS
                )
                resized_image.show()
                display(Image(resized_image))

        return save_path if save_path else None
    except Exception as e:
        print(f"An error occurred while processing the graph: {e}", flush=True)
        return None


# def plot_graph(graph:CompiledStateGraph, save_path:Any=None, display_graph:bool=True):
#     """
#     Generates a graph image from a graph object, displays it in the notebook, 
#     and optionally saves it to a file.

#     Args:
#         graph: The graph object to render.
#         save_path (str, optional): File path to save the graph image (e.g., 'graph.png').
#         display_graph (bool, optional): Whether to display the graph in the notebook. Defaults to True.
    
#     Returns:
#         str: The file path of the saved image if saved, otherwise None.
#     """
#     try:
#         # Generate the graph as a PNG image
#         graph_image = graph.get_graph(xray=True).draw_mermaid_png()

#         # Save the graph to a file if a save path is provided
#         if save_path:
#             save_path: str = os.path.join("images", "graphs", save_path)
#             with open(save_path, "wb") as f:
#                 f.write(graph_image)
#             print(f"Graph saved to {save_path}", flush=True)
#         else:
#             save_path = os.path.join("images", "graphs", f"{graph.name}.png")
#             with open(save_path, "wb") as f:
#                 f.write(graph_image)

#         # Display the graph in the notebook if requested
#         if display_graph:
#             display(Image(graph_image))

#         return save_path if save_path else None
#     except Exception as e:
#         print(f"An error occurred while processing the graph: {e}", flush=True)
#         return None
