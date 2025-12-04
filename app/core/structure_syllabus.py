import re
import uuid


def split_into_modules(cleaned_text=""):
    # Universal module pattern
    pattern = r"(Module[\s\-–_:]*(?:\d+|[IVXLCDM]+).*?)\n"
    
    # Find all module headers
    headers = re.findall(pattern, cleaned_text, flags=re.IGNORECASE)

    if not headers:
        return []

    # Split using headers as anchors
    parts = re.split(pattern, cleaned_text, flags=re.IGNORECASE)

    modules = []
    i = 1
    while i < len(parts):
        module_name = parts[i].strip()
        module_content = parts[i+1].strip()
        
        # Hard rule: modules must not accidentally include CO or PO
        if "course outcome" in module_name.lower():
            break
        if "mapping" in module_name.lower():
            break

        modules.append((module_name, module_content))
        i += 2

    return modules


def extract_unit_title(module_content):
    # First line becomes the unit title
    caps = re.findall(r"\b[A-Z]+\b", module_content)
    title = " ".join(caps)

    if title:
        return title
    return "Untitled Section"


def extract_topics(text):
    STOP_WORDS = r"(Experiments|Suggested Books|References|Text Books|Books|Suggested Learning Resources:)"
    cleaned = re.split(STOP_WORDS, text, flags=re.IGNORECASE)[0].strip()

    topics = re.split(r"[.,;:\n]", cleaned)
    topics = [t.strip().lower() for t in topics if len(t.strip()) > 2]
    return topics[:25]  # limit tags


def extract_co_llevels(course_outcome_text):
    if not course_outcome_text:
        return []  # nothing found
    
    pattern = r"(\bC[O0]\d+_?)\s*\|\s*(.*?)\s+(L\d+)"
    matches = re.findall(pattern, course_outcome_text)

    co_list = [{"code": co, "description": desc, "bloom_level": level} 
               for co, desc, level in matches]
    return co_list

def build_chunk_json(module_name, unit_title, text_block):
    module = module_name.split()[0]

    STOP_WORDS = r"(Experiments|Suggested Books|References|Text Books|Books|Suggested Learning Resources:)"
    cleaned = re.split(STOP_WORDS, text_block, flags=re.IGNORECASE)[0].strip()
    
    pattern = r'Course Outcome[:\s]*(.*)'
    match = re.search(pattern, text_block, re.IGNORECASE)
    co_text = match.group(1) if match else ""
    
    return {
        "id": str(uuid.uuid4()),
        "text": cleaned,
        "module": module,
        "unit_title": unit_title,
        "topic_tags": extract_topics(text_block),
        "content_type": "syllabus",
        # defaults, will refine later from CO-PO mapping
        "co_tag": extract_co_llevels(co_text),
        "po_tags": [],
        "source_file": "uploaded_file",
    }
