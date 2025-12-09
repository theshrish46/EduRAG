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
    """
    Loads the prompt template from the JSON file and creates the chain.
    """
    try:
        # Construct path to src/prompts/QUESTION_GEN_PROMPT.json

        prompt_template = load_prompt("QUESTION_PROMPT.json")
        return prompt_template | model | parser
    except Exception as e:
        print(f"Error loading prompt template: {e}")
        raise e


def generate_questions_chain(topic: str, blooms_level: str):
    """
    Generates 10 questions using the loaded JSON template.
    """
    max_retries = 3
    retry_delay = 5

    try:
        # 1. Retrieval
        print(f"Searching DB for: {topic}")
        results, _ = similarity_search_from_db(topic)

        if not results:
            return {"error": "No relevant syllabus content found."}

        context_text = "\n\n".join([doc.page_content for doc in results])

        # Load the chain
        chain = get_chain()

        # 2. Generation Loop (Retry Logic)
        for attempt in range(max_retries):
            try:
                print(f"Generating questions (Attempt {attempt+1})...")

                response = chain.invoke(
                    {
                        "context": context_text,
                        "topic": topic,
                        "blooms_level": blooms_level,
                    }
                )

                if isinstance(response, list):
                    return response
                else:
                    print("⚠️ LLM response was not a list. Retrying...")

            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    print(f"⚠️ Quota hit. Waiting {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"Error: {e}")
                    pass

        return {"error": "Failed to generate valid questions."}

    except Exception as e:
        return {"error": str(e)}
