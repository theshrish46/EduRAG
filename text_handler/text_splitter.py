import json

# REMOVED GLOBAL LISTS FROM HERE (chunk = [], meta_data = [])


# Add 'filename' as an argument
def get_chunks(json_object, filename):
    # Initialize lists INSIDE the function so they are empty for every new file
    chunk = []
    meta_data = []

    for module in json_object["modules"]:
        chunk_text = f"Subject Name {json_object['subject_name']} ({json_object['course_code']})\n Module ({module['module_number']}) ({module['module_name']}) ({module['syllabus_content']})"
        chunk.append(chunk_text)

        meta_data.append(
            {
                "subject_name": json_object.get("subject_name"),
                "course_code": json_object.get("course_code"),
                "course_outcomes": json.dumps(json_object.get("course_outcomes")),
                "program_outcomes": json.dumps(json_object.get("program_outcomes")),
                "source": filename,  # <--- CRITICAL ADDITION
            }
        )
    return chunk, meta_data
