from typing import Union, Any, Dict, List
import json
import asyncio


import streamlit as st
from main_cli import endpoint



# Initialize session state for maintaining state across interactions
if "selected_path" not in st.session_state:
    st.session_state.selected_path = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "query_type" not in st.session_state:
    st.session_state.query_type = "main"
if "docs" not in st.session_state:
    st.session_state.docs = []
if "send_user_data" not in st.session_state:
    st.session_state.send_user_data = False
if "last_payload" not in st.session_state:
    st.session_state.last_payload = None

# HR tree structure
hr_tree = json.load(open("dump\\ui_tree_data.json"))

def display_menu():
    # Start at the top of the menu tree
    # current_menu may be list or dict

    current_menu: Union[Dict, List] = hr_tree["Main Menu"]
    for path in st.session_state.selected_path:
        current_menu: Any | Any = (
            current_menu[path] if isinstance(current_menu, dict) else current_menu
        )

    # Display the full path of the current selection as a flow of buttons in a single line
    st.markdown("### Current Selection Path:")

    # Display buttons on a single line using columns
    if st.session_state.selected_path:
        cols = st.columns(
            len(st.session_state.selected_path) * 2 - 1
        )  # We need 2 columns for each button + 1 for the arrow
        for i, path in enumerate(st.session_state.selected_path):
            with cols[i * 2]:  # Use every other column for buttons
                # Display each path as a disabled button in the corresponding column
                st.button(f"**{path}**", disabled=True)
            if i != len(st.session_state.selected_path) - 1:
                with cols[i * 2 + 1]:  # Use the columns between buttons for the arrows
                    st.markdown(
                        "<p style='font-size: 30px;'>→</p>", unsafe_allow_html=True
                    )  # Arrow

    else:
        st.button(
            "Main Menu", disabled=True
        )  # Show "Main Menu" if there's no selection

    # Display options for the current menu
    st.markdown("---")  # Separator
    if isinstance(current_menu, dict):
        st.markdown("### Select a Category:")
        for key in current_menu.keys():
            if st.button(key):
                st.session_state.selected_path.append(key)
                st.rerun()
    elif isinstance(current_menu, list):
        st.markdown("### Select an Option:")
        for item in current_menu:
            if item in st.session_state.selected_path:
                st.button(
                    item, disabled=True
                )  # Disable button if it has already been selected
            else:
                if st.button(item):
                    st.session_state.selected_path.append(
                        item
                    )  # Add the list item to the path
                    st.session_state.chat_history.append(
                        {
                            "role": "system",
                            "content": f"User selected: {' > '.join(st.session_state.selected_path)}",
                        }
                    )
                    st.rerun()

    else:
        st.error("Invalid menu structure")
    # Provide a "Back" button to go to the previous level
    if len(st.session_state.selected_path) > 0:
        if st.button("Back"):
            st.session_state.selected_path.pop()
            st.rerun()


def page_content():

    st.set_page_config(page_title="HR ChatBot", layout="wide")

    # Sidebar for settings and document rendering
    with st.sidebar:
        st.header("Settings")
        st.text("Customize chatbot behavior")
        st.header("Document Renderer")
        st.text("Display selected documents here.")
    # Main Chat UI
    st.title("HR ChatBot")
    st.subheader("Navigate HR options or ask anything.")

    # Display current menu
    display_menu()

    for message in st.session_state.chat_history:
        role, content = message["role"], message["content"]
        with st.chat_message(role):
            st.markdown(content)

    for i, doc in enumerate(st.session_state.docs):
        with st.sidebar:
            with st.expander(f"Document {i+1}"):
                st.write(doc['page_content'])
            with st.expander(f"Metadata {i+1}"):
                st.write(doc['metadata'])



# Main Streamlit App
async def main():
    page_content()

    # Chat input using `st.chat_input`
    if user_input := st.chat_input("Ask me anything..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
 
        text = endpoint(user_input)


        st.session_state.chat_history.append({"role": "assistant", "content": text})

        with st.chat_message("assistant"):
            st.markdown(text)
        

        st.rerun()


if __name__ == "__main__":
    asyncio.run(main())



