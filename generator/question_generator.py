import json
import os
import sys
import time
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import JsonOutputParser

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.llm_model import get_genai_model
from embeddings.chroma_store import similarity_search_from_db

model = get_genai_model()
parser = JsonOutputParser()


def get_chain():
    try:
        prompt_template = load_prompt("QUESTION_PROMPT.json")
        # --- FIX 1: Add the parser to the chain pipe ---
        return prompt_template | model | parser
    except Exception as e:
        print(f"Error loading prompt template: {e}")
        raise e


def generate_questions_chain(
    subject: str,
    topic: str,
    blooms_level: list[str],
    format_type: str,
    temperature: float,
):
    max_retries = 3
    retry_delay = 2

    try:
        # 1. Retrieval
        print(f"Searching DB for: {topic}")
        results, _ = similarity_search_from_db(topic)

        if not results:
            return {"error": "No relevant syllabus content found."}

        context_text = "\n\n".join([doc.page_content for doc in results])
        chain = get_chain()

        # 2. Generation Loop
        for attempt in range(max_retries):
            try:
                print(f"Generating questions (Attempt {attempt+1})...")

                # --- FIX 2: The chain now returns a Python LIST directly ---
                # No more text.split("\n") or .content calls needed!
                questions = chain.invoke(
                    {
                        "subject": subject,
                        "context": context_text,
                        "topic": topic,
                        "blooms_level": blooms_level,
                        "format_type": format_type,
                        "temperature": temperature,
                    }
                )
                if not questions:
                    print("No questions found")
                print("========INNERSTART============")
                print(questions)
                print(type(questions))
                print("========INNEREND============")

                # Validate that we got a list back
                if isinstance(questions, list) and len(questions) > 0:
                    return questions
                else:
                    print("⚠️ Response was not a valid list. Retrying...")

            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    # If JSON parsing fails (parser error), it will catch here
                    print(f"Parsing/Generation Error: {e}")

        return {"error": "Failed to generate valid JSON questions after retries."}

    except Exception as e:
        return {"error": str(e)}
