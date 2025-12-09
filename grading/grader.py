import os
import base64
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

def get_image_base64(image_file):
    """
    Reads a file buffer and converts it to base64 string.
    """
    # Read the file bytes
    image_bytes = image_file.getvalue()
    # Encode to base64
    encoded_string = base64.b64encode(image_bytes).decode("utf-8")
    return encoded_string

def grade_answer_image(question, syllabus_context, image_file, max_marks):
    """
    Sends the Question + Context + Student Image to Gemini for grading.
    """
    # 1. Initialize Model (Gemini 1.5 Flash is Multimodal)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.0, # We want strict grading, no creativity
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # 2. Prepare the Image Data
    image_b64 = get_image_base64(image_file)
    
    # 3. Define the Prompt
    # Note: For multimodal messages, we use a list of content blocks
    
    system_instruction = """
    You are a strict academic examiner. 
    You will be provided with an exam question, the official syllabus context, and a student's handwritten answer (image).
    
    Your Task:
    1. Read the handwritten answer from the image.
    2. Compare it against the Syllabus Context.
    3. Award marks based on accuracy, depth, and key concepts mentioned.
    4. Provide constructive feedback.
    
    Output Format (JSON):
    {
        "handwriting_transcription": "What you read from the image...",
        "marks_awarded": "X out of Y",
        "reasoning": "Why you gave these marks",
        "improvement_tips": "What was missing"
    }
    """

    user_message_content = [
        {
            "type": "text",
            "text": f"""
            ### EXAM DETAILS:
            **Question:** {question}
            **Max Marks:** {max_marks}
            
            ### OFFICIAL SYLLABUS CONTEXT:
            {syllabus_context}
            
            ### INSTRUCTION:
            Grade the student's answer image below.
            """
        },
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
        }
    ]

    # 4. Invoke the Model
    try:
        messages = [
            SystemMessage(content=system_instruction),
            HumanMessage(content=user_message_content)
        ]
        
        response = llm.invoke(messages)
        
        # Parse the JSON string from the response
        parser = JsonOutputParser()
        return parser.parse(response.content)
        
    except Exception as e:
        return {"error": str(e)}