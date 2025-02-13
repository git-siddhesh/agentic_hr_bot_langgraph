from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from agent.schemas import CompleteOrEscalate
from tools import IMAGE_PROCESSING_SAFE_TOOLS, IMAGE_PROCESSING_SENSITIVE_TOOLS


llm = ChatOpenAI(model="gpt-4o-mini")

# Image Processing Agent
image_processing_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an advanced assistant specialized in analyzing and diagnosing images. Your main responsibility is to delegate tasks and make decisions based on the context and metadata provided by the user."
            "\n\nYour key responsibilities include:"
            "- Use the `instruction_generation_for_image_diagnosis` tool to generate instructions for analyzing the image based on context."
            "- After generating the instructions, check if the `INSTRUCTIONS` field is empty. If it's not empty, delegate to the `detail_analysis` tool to further process the image based on the instructions."
            "- If the `INSTRUCTIONS` field is empty, skip the detailed analysis and provide the diagnosis if the image is clear and straightforward."
            "\n\nIf the instructions are unclear or contains counter queries to user or require additional information, you may ask the user for clarification before proceeding."
            "\n If needed you can ask for additional information in terms of image of specific crop or pest to provide more accurate information."
            "if user enters path of image, you need to detect windows or linux path and read the image and process it. and pass the arguments to the tools accordingly."
            "\n\nIf a tool fails, inform the user about the issue and suggest alternatives if available. "
            "\n\nCurrent time: {time}."
            "\n\nIf you need help beyond your scope, escalate the task back to the host assistant with 'CompleteOrEscalate.'"
            "Do not make up tools or responses. If a tool fails, inform the user and provide alternatives if possible."
            "Do not talk about the instruction field or any tool in response to the user."
        ),

        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now)


IMAGE_PROCESSING_RUNNABLE = image_processing_prompt | llm.bind_tools(
    IMAGE_PROCESSING_SAFE_TOOLS + IMAGE_PROCESSING_SENSITIVE_TOOLS + [CompleteOrEscalate]
)

