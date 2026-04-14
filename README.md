# EduRAG: Syllabus-Aware Examination & Grading System

![Home Page](./assets/home%20page.png)

### The Problem
Academic assessment suffers from a disconnect between static syllabus documents and active evaluation. Manual processes create three core inefficiencies:
* **Drafting Overhead:** Manually aligning exam questions with specific modules and Bloom’s Taxonomy levels is repetitive and error-prone.
* **The Handwriting Gap:** Grading handwritten student work traditionally requires manual transcription or physical handling, slowing down the feedback loop.
* **Contextual Accuracy:** Standard AI graders often rely on general knowledge rather than the specific "ground truth" of a university’s official curriculum.

### The Solution
EduRAG digitizes the academic lifecycle by anchoring every action to the official syllabus. Using **Retrieval-Augmented Generation (RAG)**, it ensures that question generation and answer evaluation are strictly mapped to the uploaded curriculum. It bridges the gap between physical handwriting and digital evaluation through multimodal AI.

![Home Page](./assets/home%20page%20with%20file%20uploading.png)

---

### How It Works
1. **Syllabus Digitization:** Uses Tesseract OCR to extract text from PDF syllabi, cleaning and partitioning data into logical "Modules" to preserve the curriculum structure.
2. **Vectorized Knowledge:** Converts structured text into high-dimensional vectors stored in **ChromaDB**, allowing for topic-specific similarity searches.
3. **Automated Exam Generation:** Retrieves syllabus context based on user-defined parameters (Subject, Module, Bloom’s Level) and generates a structured exam paper following university-standard "Choice" logic (e.g., Q1 OR Q2).
4. **Multimodal Evaluation:** Processes images of handwritten answers by:
    * Transcribing handwriting into digital text via Vision-Language models.
    * Retrieving the specific syllabus "Truth" for the given question.
    * Comparing student output against the syllabus to award marks and provide constructive reasoning.

![Working](./assets/semantic%20search%20results.png)
![Working](./assets/question%20paper%20generation%20.png)
![Working](./assets/answer%20paper%20upload.png)
![Working](./assets/feedback%20from%20model.png)

---

### Technical Stack
* **Orchestration:** LangChain (Chains, PromptTemplates, OutputParsers).
* **Models:** Google Gemini 1.5 Pro & 2.5 Flash-Lite (Multimodal/Vision).
* **OCR Engine:** Tesseract OCR (Initial PDF-to-Text).
* **Vector Database:** ChromaDB (Storage and Retrieval).
* **Document Generation:** FPDF2 (PDF Rendering).
* **Interface:** Streamlit (Web Dashboard).

---

### Local Setup
1. **Install Tesseract OCR:** Ensure the Tesseract engine is installed on your OS and added to your system's PATH.
2. **Clone Repository:** Download the project files to your local environment.
3. **Install Dependencies:** Run `pip install -r requirements.txt`.
4. **Configure API Key:** Create a `.env` file in the root directory and add `GOOGLE_API_KEY=your_key_here`.
5. **Launch App:** Execute `streamlit run app.py` to start the local server.