import sys
import os
import pytest

# --- THE FIX ---
# Get the directory where this test file is located (e.g., /EduRAG/tests)
current_test_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the Project Root (e.g., /EduRAG)
project_root = os.path.dirname(current_test_dir)
# Add Project Root to Python Path so we can find 'utils' and 'text_handler'
sys.path.append(project_root)

# --- IMPORTS ---
# Now Python can find these folders in your root
from utils.pdf_utils import get_clean_marks, generate_pdf_from_questions
from text_handler.text_splitter import get_chunks

# --- TEST CASE 1: The Marks Cleaning Logic ---
def test_marks_extraction_logic():
    # Scenario A: Clean number
    assert get_clean_marks({"marks": 5}) == "5"
    # Scenario B: String with text
    assert get_clean_marks({"marks": "10 Marks"}) == "10"
    # Scenario C: Mixed case key
    assert get_clean_marks({"Marks": "20"}) == "20"
    # Scenario D: Empty/Garbage
    assert get_clean_marks({}) == "0"

# --- TEST CASE 2: PDF Generation (Smoke Test) ---
def test_pdf_generation_integrity():
    mock_questions = [
        {"question": "What is Python?", "marks": 5},
        {"question": "Define Big Data.", "marks": 10}
    ]
    
    # Generate PDF (Topic="Test", Level="L1")
    pdf_bytes = generate_pdf_from_questions(mock_questions, "Unit Test Topic", "L1")
    
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 0
    assert isinstance(pdf_bytes, bytes)
    assert pdf_bytes.startswith(b"%PDF")

# --- TEST CASE 3: Syllabus Chunking Logic ---
def test_chunking_logic():
    mock_json = {
        "subject_name": "Test Subject",
        "course_code": "CS101",
        "modules": [
            {
                "module_number": "1",
                "module_name": "Intro",
                "syllabus_content": "Basic testing content."
            }
        ],
        "course_outcomes": [],
        "program_outcomes": []
    }
    
    # We pass a fake filename
    chunks, metadata = get_chunks(mock_json, "test_syllabus.pdf")
    
    assert len(chunks) == 1
    # Check if the filename was correctly saved in metadata
    assert metadata[0]["source"] == "test_syllabus.pdf"