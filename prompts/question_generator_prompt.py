from langchain_core.prompts import PromptTemplate
from pathlib import Path

# Define the Prompt Template string
# FIX: Double curly braces {{ }} are used for the JSON example to tell LangChain
# "this is literal text, not a variable placeholder".
template_string = """
You are an expert question paper generator.

Your task is to generate a question paper based on the following context:
CONTEXT: {context}

----------------------------------------
TASK:
Generate questions for the Subject: {subject} on the Topic: {topic}.
Difficulty Level: {temperature} 
Cognitive Level (Bloom's Taxonomy): {blooms_level}

You must strictly follow the format based on the "format_type" provided.

----------------------------------------
FORMAT RULES:

If {format_type} == "FA Internals (Max Marks 30)":
- You must generate EXACTLY 6 questions.
- Each question carries 10 marks.
- The structure represents 3 choices (Q1 OR Q2, Q3 OR Q4, Q5 OR Q6).
- Since only one from each pair is answered, the total marks for the student will be 30.

If {format_type} == "SA Externals (Max Marks 100)":
- You must generate EXACTLY 10 different distinct questions.
- Each question carries 20 marks.
- The structure represents 5 choices (Q1 OR Q2, Q3 OR Q4, Q5 OR Q6, Q7 OR Q8, Q9 OR Q10).
- Since only one from each pair is answered, the total marks for the student will be 100.

----------------------------------------

GENERAL INSTRUCTIONS:
- Clearly mention marks for each question and sub-question.
- Questions should be appropriate to the given Blooms level: {blooms_level}.
- Use the provided context to source information: {context}.
- Avoid repetition and ensure logical progression.

----------------------------------------
INPUTS:
Subject: {subject}
Context: {context}
Topic: {topic}
Blooms Level: {blooms_level}
Format Type: {format_type}
Temperature Setting: {temperature}

----------------------------------------
OUTPUT FORMAT INSTRUCTIONS:
Return a JSON array of objects.

Example for Internals:
[
  {{
    "question": "Explain Linear Regression.",
    "marks": 10
  }},
  {{
    "question": "Explain Logistic Regression.",
    "marks": 10
  }}
]
----------------------------------------

Notes:
- Each object must only contain "question" and "marks".
- Do NOT include "qno", "subquestions", or "qsubno".
- Ensure the total marks sum up exactly to the requirement of the {format_type}.
- Return **valid JSON only**, so it can be directly loaded into Python with `json.loads()`.
----------------------------------------
"""

# Create the Template
# Using from_template is safer as it auto-detects variables
template = PromptTemplate.from_template(template_string)

# Save the template
# Ensure the file is saved in the same directory as your app expects
template.save("QUESTION_PROMPT.json")

print("✅ Template saved successfully!")
print(
    "Fixed: Escaped JSON braces by doubling them {{ }} to avoid LangChain validation errors."
)
