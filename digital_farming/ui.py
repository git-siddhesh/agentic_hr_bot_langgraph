from typing import Union, Any, Dict, List
import json
import asyncio
import os
import shutil
import uuid
from main_cli import endpoint
from pathlib import Path

import streamlit as st
st.set_page_config(page_title="Digital Farming", page_icon="🌾", layout="wide")

# Main Chat UI
st.markdown("<h1 style='text-align: center;'>DIGITAL FARMING</h1>", unsafe_allow_html=True)


# Initialize session state for maintaining state across interactions
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "uploaded_audio" not in st.session_state:
    st.session_state.uploaded_audio = None
if "user_input" not in st.session_state:
    st.session_state.user_input = None
if "submit_media" not in st.session_state:
    st.session_state.submit_media = None
if "image_uploader_key" not in st.session_state:
    st.session_state["image_uploader_key"] = 1
if "audio_uploader_key" not in st.session_state:
    st.session_state["audio_uploader_key"] = 100



# Directory setup
IMAGE_DIR = "./images/user_input/"
AUDIO_INPUT_DIR = "./audio/user_input/"
AUDIO_OUTPUT_DIR = "./audio/bot_output/"
AUDIO_ARCHIVE_DIR = "./audio/past_audios/"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(AUDIO_INPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_ARCHIVE_DIR, exist_ok=True)

# Function to move and render generated audio output
def handle_bot_audio():
    bot_audio_path = os.path.join(AUDIO_OUTPUT_DIR, "speech_tts.mp3")
    if os.path.exists(bot_audio_path):
        unique_name = f"bot_audio_{uuid.uuid4().hex}.mp3"
        archive_path = os.path.join(AUDIO_ARCHIVE_DIR, unique_name)
        shutil.move(bot_audio_path, archive_path)
        return archive_path
    return None

# Page content function
def page_content(column):
    with column:
        # Display chat history
        # print("Chat history:", st.session_state.chat_history)
        with st.container(height=800, border=True):
            for message in st.session_state.chat_history:
                role, content = message["role"], message["content"]
                with st.chat_message(role):
                    if content.startswith("audio:"):
                        audio = content.split("audio:")[1]
                        st.audio(audio, format="audio/mp3")
                    if content.startswith("image:"):
                        image = content.split("image:")[1].strip()
                        st.image(image)
                    else:
                        st.markdown(content)

# import streamlit.logger as streamlit_root_logger

def process_uploaded_image():
    # streamlit_root_logger.debug(f"Uploaded File: {st.session_state['uploaded_invoice']}")
    file_name = st.session_state[st.session_state.image_uploader_key].name
    file_content = st.session_state[st.session_state.image_uploader_key].getvalue()

    image_path = os.path.join(IMAGE_DIR, file_name)
    st.session_state.chat_history.append({"role": "user", "content": f"image:{Path(image_path)}"})

    with open(image_path, "wb") as f:
        f.write(file_content)

    st.session_state.uploaded_image = image_path
    st.session_state.image_uploader_key += 1
    st.rerun()
        
def process_uploaded_audio():
    file_name = st.session_state[st.session_state.audio_uploader_key].name
    file_content = st.session_state[st.session_state.audio_uploader_key].getvalue()

                                  
    audio_path = os.path.join(AUDIO_INPUT_DIR, file_name)
    st.session_state.chat_history.append({"role": "user", "content": f"audio:{Path(audio_path)}"})

    with open(audio_path, "wb") as f:
        f.write(file_content )

    st.session_state.uploaded_audio = audio_path
    st.session_state.audio_uploader_key += 1
    st.rerun()

# Main Streamlit App
async def main():
    
    col1, col2= st.columns([1,4])
    page_content(column=col2)
    
    with col1:

        audio_file = st.audio_input("Record a voice message", key=st.session_state["audio_uploader_key"], 
                                    on_change= process_uploaded_audio
                                    )

        # if audio_file:
        # if audio_file and st.session_state.uploaded_audio is None:
        #     process_uploaded_audio(audio_file)

        image_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key=str(st.session_state["image_uploader_key"]),
                                    
                                      on_change= process_uploaded_image
                                      )
        
        # if image_file and st.session_state.uploaded_image is None:
        #     process_uploaded_image(image_file)

        # st.session_state.submit_media = st.button("Submit media")

    st.session_state.user_input = st.chat_input("Ask me anything...")


    # Process the user input or uploaded files
    if st.session_state.user_input or st.session_state.uploaded_image or st.session_state.uploaded_audio:
        response = None
        if st.session_state.user_input:
            input_text = st.session_state.user_input 
            st.session_state.user_input = None

            print("User input:", input_text)

            st.session_state.chat_history.append({"role": "user", "content": input_text})
            # with st.chat_message("user"):
            #     st.markdown(input_text)

            # with st.spinner("Processing"):
            response = endpoint(text=input_text)
        else:
    

            if st.session_state.uploaded_image:
                input_text = st.session_state.uploaded_image
                st.session_state.uploaded_image = None
                st.session_state.submit_media = None
                print("Uploaded an image:", input_text)   
                # with st.spinner("Processing"):
                response = endpoint(image_path=input_text)

            elif st.session_state.uploaded_audio:
                input_text = st.session_state.uploaded_audio
                st.session_state.uploaded_audio = None
                st.session_state.submit_media = None

                print("Uploaded an audio:", input_text)
                # with st.spinner("Processing"):
                response = endpoint(audio_path=input_text)


        if response:
            # Append the assistant's response
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            # with st.chat_message("assistant"):
            #     st.markdown(response)

            # Check for generated audio and handle it
            bot_audio = handle_bot_audio()
            if bot_audio:
                st.session_state.chat_history.append({"role": "assistant", "content": f"audio:{bot_audio}"})
                with st.chat_message("assistant"):
                    st.audio(bot_audio, format="audio/mp3")

        st.rerun()

def dummy_endpoint(text="", image_path="", audio_path=""):
    print("DummyEndpoint called.", text, image_path, audio_path)
    input()
    if text:
        return f"Processed text: {text}"
    elif image_path:
        return f"Processed image at: {image_path}"
    elif audio_path:
        return f"Processed audio at: {audio_path}"
    else:
        return "No input provided."

if __name__ == "__main__":
    asyncio.run(main())
