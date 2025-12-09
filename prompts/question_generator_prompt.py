from langchain_core.prompts import PromptTemplate
import os

# Define the Prompt Template
template = PromptTemplate(
    template="""
You are an expert academic examiner. Your task is to generate a structured examination paper worth **Total 30 Marks** based strictly on the provided syllabus context.

### INPUT DATA:
- **Topic:** {topic}
- **Target Bloom's Level:** {blooms_level}

### SYLLABUS CONTEXT:
{context}

### STRICT INSTRUCTIONS:
1. **Quantity:** You MUST generate **EXACTLY 10 QUESTIONS**.
2. **Total Marks:** The sum of marks for all questions MUST equal **30**.
3. **Distribution:** Use a mix of 2, 3, and 5 mark questions.
4. **Format:** Return the output as a strictly valid JSON list.
5. **Keys:** Use lowercase keys: "question", "marks", "blooms_level".

### REQUIRED JSON OUTPUT FORMAT:
[
  {{
    "question": "Define Big Data and explain its V's.",
    "marks": 5,
    "blooms_level": "{blooms_level}",
    "expected_answer_key": "Volume, Velocity, Variety..."
  }},
  {{
    "question": "What is a NameNode?",
    "marks": 2,
    "blooms_level": "{blooms_level}",
    "expected_answer_key": "Master node in HDFS..."
  }}
]
""",
    input_variables=["context", "topic", "blooms_level"],
    validate_template=True,
)


# Save the template
template.save("QUESTION_PROMPT.json")

print(f"✅ Template saved successfully")
print("   (It now strictly requires 10 questions and 30 marks total)")
