from typing import Optional, Dict, Any, List
from datetime import date, datetime
from langchain_core.tools import tool

from dotenv import load_dotenv
load_dotenv(override=True)
import json
import re
import os


from openai import OpenAI, AsyncOpenAI
from pathlib import Path
client = OpenAI()


# client_async = AsyncOpenAI()

@tool
def translate_text(
    text: str,
    source_language: str,
    target_language: str,
) -> str:
    """
    Translates text from a source language to a target language.

    Args:
        text: The text to be translated.
        source_language: The language code of the source text.
        target_language: The language code of the target translation.

    Returns:
        translated_text: The translated text in the target language.
    """
    print("Translating text...")
    response: Any = client.chat.completions.create(
        model= "gpt-4o-mini",
        messages=[
            # {"role": "system", "content": self.system_prompts[use]},
            {"role": "system", "content": f"Translate the following text from {source_language} to {target_language}. Do not include the source text in the translation. Do not modify the original text format."},
            {"role": "user", "content": text},
        ],
        temperature=0.0,
    )
    message = response.choices[0].message.content

    return message



@tool
def tts(text: str) -> str:
    """
    Converts text to speech using a text-to-speech model.

    Args:
        text: The text to be converted to speech.

    Returns:
        speech_file_path: The audio data path of the synthesized speech; default is "audio\\bot_output\\speech_tts.mp3"
    """

    # speech_file_path = Path(__file__).parent / "speech_tts.mp3"
    speech_file_path = "audio\\bot_output\\speech_tts.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    response.stream_to_file(speech_file_path)

    
    return speech_file_path

@tool
def stt(speech_file_path: Path) -> str:
    """
    Converts speech to text using a speech-to-text model.

    Args:
        speech_file_path: The audio data path of the speech to be converted ; default is "audio\\user_input\\speech_sst.mp3"

    Returns:
        text: The transcribed text from the speech.
    """

    # speech_file_path = Path(__file__).parent / "speech_sst.mp3"
    # speech_file_path = "audio\\user_input\\speech_sst.mp3"
    if not os.path.exists(speech_file_path):
        raise FileNotFoundError(f"File not found: {speech_file_path}")
    
    # convert the path to absolute path
    speech_file_path = os.path.abspath(speech_file_path)
    print(f"Converting speech to text... {speech_file_path}")

    audio_data = open(speech_file_path, "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_data, 
        response_format="text"
    )

    print(transcription)

    return transcription