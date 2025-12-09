from fpdf import FPDF
from datetime import date
import re

class QuestionPDF(FPDF):
    def header(self):
        # Header is handled manually in the generate function for flexibility
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def get_clean_marks(q_dict):
    """
    Robustly extracts integer marks from messy LLM output.
    Ex: "5" -> "5", "5 marks" -> "5", "Marks: 5" -> "5"
    """
    # 1. Try finding the key (case-insensitive)
    raw_val = q_dict.get("marks") or q_dict.get("Marks") or q_dict.get("score")
    
    if raw_val is None:
        return "0"
    
    # 2. If it's already a number
    if isinstance(raw_val, (int, float)):
        return str(int(raw_val))
        
    # 3. If it's a string, use Regex to find the first number
    raw_str = str(raw_val)
    match = re.search(r'\d+', raw_str)
    if match:
        return match.group()
        
    return "0"

def generate_pdf_from_questions(questions_json, topic, blooms_level):
    pdf = QuestionPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    today_date = date.today().strftime("%d-%b-%Y")
    
    # --- HEADER ---
    pdf.set_font("Arial", "B", 12)
    
    # Subject (Left)
    pdf.cell(100, 8, f"Subject: {topic}", ln=0, align='L')
    
    # Max Marks (Right)
    pdf.set_x(140)
    pdf.cell(50, 8, "Max Marks: 30", ln=1, align='R')
    
    # Date (Left)
    pdf.cell(100, 8, f"Date: {today_date}", ln=0, align='L')
    
    # Level (Right)
    pdf.set_x(140)
    pdf.cell(50, 8, f"Level: {blooms_level}", ln=1, align='R')
    
    # Separator Line
    pdf.ln(2)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)
    
    # --- QUESTIONS ---
    pdf.set_font("Arial", size=11)
    
    for i, q in enumerate(questions_json):
        question_text = q.get("question", "N/A")
        marks = get_clean_marks(q) # <--- USE THE HELPER FUNCTION
        
        # Encoding fix
        question_text = question_text.encode("latin-1", "ignore").decode("latin-1")

        # 1. Question Number
        pdf.set_font("Arial", "B", 11)
        pdf.cell(10, 6, f"Q{i+1}.", ln=0)
        
        # 2. Store Start Position
        start_x = pdf.get_x()
        start_y = pdf.get_y()
        
        # 3. Print Question Text (Wrapped)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(160, 6, question_text)
        
        # 4. Get End Position
        end_y = pdf.get_y()
        
        # 5. Move to Right for Marks
        pdf.set_xy(180, start_y)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(15, 6, f"[{marks} M]", align='R')
        
        # 6. Reset cursor below the content
        pdf.set_xy(10, end_y)
        pdf.ln(4) # Gap

    return pdf.output(dest="S").encode("latin-1", "replace")