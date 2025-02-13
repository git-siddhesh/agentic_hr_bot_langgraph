from typing import Optional, Dict, Any, List
from datetime import datetime
from langchain_core.tools import tool

from dotenv import load_dotenv
load_dotenv(override=True)
import json
from pathlib import Path
from openai import OpenAI
import base64
import os

client = OpenAI()

def encode_image(image_path):
    """
    Encode the image file to Base64 format.
    """
    print("Encoding image...")
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                return  base64.b64encode(image_file.read()).decode("utf-8")
        else:
            print("Image file not found.")
            return None
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def process_image_using_llm(image_path:Path, text:str) -> str:
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            # "detail": "high"
                        },
                    },
                ],
            }
        ],
    )

    # print(response.choices[0])
    return response.choices[0].message.content


# def instruction_generation_for_image_diagnosis(context: str, image: bytes, metadata: Dict[str, str]) -> str:
@tool
def instruction_generation_for_image_diagnosis(context: str, image: str, metadata: Dict[str, str] = {}) -> str:
    """
    Generates instructions or commands for diagnosing an image based on the context and image data.
    The instructions are used to guide the user or system in analyzing the image in a structured manner depending on the context.
    Instructions may include questions, tasks, or specific steps to follow for image diagnosis.
    
    Args:
        context: The context or scenario in which the image diagnosis is required.
        image: The input image path.
        metadata: Dictioanry Additional metadata related to the image. For example, crop type, location, etc.

    Returns:
        instructions: The generated instructions for diagnosing the image.
        These instructions can be further used to detect or analyze the same image in detail.
    """



    print("Generating instructions for image diagnosis...")

    # image = "images\\user_input"
    # convert to absolute path
    print(image)
    image = os.path.abspath(image)
    print(image)
    image_path = Path(image)
    print(image_path)
    # image_path = image

    text = f"""
        CONTEXT: {context}

        You are tasked with analyzing an image to diagnose a specific issue based on the provided context. The image may either be very clear, containing a single component or object for diagnosis, or it may contain multiple objects or features that need to be identified and assessed.

        1. **If the image contains a single, clear object or component for diagnosis**, directly provide the diagnosis. For example, if the image contains a single plant with visible disease symptoms, provide a diagnosis of the condition (e.g., "The plant has a fungal infection due to visible yellow spots on the leaves").

        2. **If the image contains multiple objects or components**, or if the context is complex (e.g., a large field with various crops, pests, and diseases), generate a detailed set of instructions for the next steps of image analysis:
        - Break down the image into components or objects that need to be identified (e.g., crops, pests, diseases, etc.).
        - Based on the context, generate tasks to process and diagnose the image:
            - Identify the plant's leaves and check their condition.
            - Detect any weeds around the crop.
            - Identify if there are visible insects or pests on the plant.
            - Examine the leaf texture and color for signs of disease or stress.
            - Check if there are any external factors like weather damage or nutrient deficiency.
            - If needed ask for additional information or metadata related to the image from the user.

        3. **Output Format**:
            Case 1: If the image is clear enough for direct diagnosis, return the diagnosis in the following format:
            - `DIAGNOSIS`: [The diagnosis text]
            - `INSTRUCTIONS`: ""
            - `COUNTER_QUERIES`: ""

            Case 2: If the image requires multiple steps for diagnosis, generate a series of instructions in the following format:
            - `DIAGNOSIS`: "Base diagnosis on the identified components if possible."
            - `INSTRUCTIONS`: [The list of instructions for detailed image processing step]
            - `COUNTER_QUERIES`: [Any additional questions or queries for the user for the disambiguation of the context]

        4. If there are specific diagnostic checks or areas that require special attention based on the context (e.g., crop type, location), include those in the instructions as well.

        5. If require any additional information or metadata related to the image from the user, include it in the "Counter query".

        NOTE: The instructions should be only related to the image to have specific and detailed diagnosis of same image in next phase.

        Metadata: {metadata}

        Please analyze the image and determine whether a direct diagnosis is possible or if instructions/disambiguation for further analysis are needed. 
        """


    return process_image_using_llm(image_path, text)

@tool
def analyze_detect_classify_image(context:str, instructions:str, image_path:str, metadata:Dict[str, str] = {}) -> str:
    """
    Analyze, detect, and classify the image based on the given instructions and context.
    The function uses the specific instructions provided to diagnose the image by answering questions, identifying objects, and providing a detailed analysis.

    Args:
        context: The context or scenario in which the image analysis is required.
        instructions: The generated instructions for diagnosing the image.
        image_path: The path to the input image file.
        metadata: Additional metadata related to the image. For example, crop type, location, etc.

    Returns:
        analysis_result: The result of the image analysis, including features, classification, and diagnosis based on the instructions provided.
    """
    print("Analyzing, detecting, and classifying image...")

    text = f"CONTEXT: {context}\n METADATA {metadata}\n INSTRUCTIONS: {instructions} \n\n Based on the given instructions, analyze the image and provide response for each question or task."

    return process_image_using_llm(image_path, text)
    
