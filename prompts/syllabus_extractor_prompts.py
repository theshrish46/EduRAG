from langchain_core.prompts import PromptTemplate


template = PromptTemplate(
    template="""

        "system",
        "You are an assistant that extracts structured syllabus information from raw syllabus text."
    ),
    (
        "user",
Extract the following information from the syllabus text provided. 
Return output strictly as JSON.

Fields required:

1. subject_name: Name of the course.
2. course_code: Code of the course.
3. modules: A list of all modules. Each module should include:
    - module_number: e.g., Module-1
    - module_name: Title of the module
    - syllabus_content: Full text description of the module (all topics, examples, pedagogy)
4. course_outcomes: A list of outcomes. Each should include:
    - description: Text of the outcome
    - blooms_level: Level in Bloom's taxonomy (L1-L6)
5. program_outcomes: A dictionary mapping PO codes to their mapping with COs

Here is the syllabus text:

{syllabus_text}

Important instructions:
- Return a valid JSON only.
- Do not include any extra explanations or text outside JSON.
- Make sure multi-line contents like syllabus_content are preserved properly.
- Use arrays/lists for multiple modules and outcomes.
""",
    input_variables=["syllabus_text"],
    validate_template=True,
)


template.save("SYLLABUS_PROMPT.json")
