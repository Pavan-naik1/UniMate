# UniMate: Faculty Project Demonstration Script
## Step-by-Step Viva & Faculty Evaluation Sequence (RTD Open Elective - 30 Marks)

This guide provides the exact step-by-step walkthrough to demonstrate UniMate to your university faculty and project examiners.

---

### PREPARATION (1 Minute Before Demo)
1. Ensure your laptop is on.
2. Double-click `start.bat`.
3. Wait 10 seconds for the browser to open to `http://localhost:5173`.
4. Maximize the browser window.

---

### DEMONSTRATION STEPS & SPEAKING SCRIPT

#### STEP 1: Introduce Project & Problem Statement (Dashboard)
- **Action**: Stay on the **Dashboard** page.
- **Speaking Notes**:
  > *"Respected Faculty, for our RTD Open Elective project worth 30 marks, we have developed 'UniMate: An Intelligent University Assistant Using Generative AI and Large Language Models'.*
  > *Students face a significant problem: university documents—syllabi, academic regulations, examination guidelines, and lecture notes—are scattered across dozens of long PDFs. Generic search tools like Ctrl+F only find exact keywords, while public chatbots like ChatGPT hallucinate university policies and cannot cite exact page numbers.*
  > *UniMate solves this using a local Retrieval-Augmented Generation (RAG) pipeline."*
- **Visuals to highlight**: Point out the KPI cards (Indexed Documents, Questions Answered, Quizzes Attempted, Study Progress) and the real-time system activity audit trail.

---

#### STEP 2: Show Document Ingestion & Vector Storage (My Documents)
- **Action**: Click **My Documents** in the sidebar.
- **Speaking Notes**:
  > *"Here is the Document Management module. UniMate has already preloaded and indexed 4 realistic demonstration university documents: Generative AI Study Notes, Computer Science Syllabus, University Academic Regulations, and Examination Guidelines.*
  > *When a PDF is uploaded, PyMuPDF extracts text page-by-page. The system then applies sliding-window recursive chunking (800 characters with 150-character overlap) to preserve sentence context. Each chunk is vectorized into 384 dimensions using Sentence-Transformers (all-MiniLM-L6-v2) and indexed in ChromaDB."*
- **Visuals to highlight**: Point to the "Vectorized" badges, chunk counts, and page counts.

---

#### STEP 3: Demonstrate RAG Conversational Q&A with Citations (AI Chatbot)
- **Action**: Click **AI Chatbot** in the sidebar.
- **Speaking Notes**:
  > *"Now let's test the conversational RAG chatbot. We will ask a question about university attendance regulations."*
- **Action**: Click the suggested prompt: *"What is the minimum attendance requirement according to university regulations?"* or type it and press **Ask AI**.
- **Speaking Notes**:
  > *"Notice what happened here: the system converted the student's question into a numerical embedding, retrieved the top semantic passages from ChromaDB using Cosine Similarity, and augmented the prompt with this context.*
  > *The assistant answered accurately (75% minimum attendance, with condonation up to 10% on medical grounds).*
  > *Crucially, observe the source citation badge below: it cites 'University_Academic_Regulations.pdf', Page 1, with the exact excerpt. There are zero hallucinations!"*
- **Visuals to highlight**: Show the citation cards with document name, page badge, and excerpt.

---

#### STEP 4: Demonstrate Document-Specific Scope Filtering
- **Action**: In the top dropdown "Query Scope", switch from "All Uploaded Documents" to *"GenAI_Study_Notes.pdf"*.
- **Action**: Ask: *"What is the difference between Generative AI and traditional programming?"*
- **Speaking Notes**:
  > *"UniMate allows students to query either the entire institutional knowledge base or restrict their search to a single subject document. Notice the answer is directly sourced from the GenAI study notes."*

---

#### STEP 5: Demonstrate AI Notes Summarizer (AI Summarizer)
- **Action**: Click **AI Summarizer** in the sidebar.
- **Action**: Select *"GenAI_Study_Notes.pdf"*, choose *"Important Points"* or *"Key Definitions"*, and click **Generate AI Summary**.
- **Speaking Notes**:
  > *"Students preparing for semester examinations need quick revision material. UniMate provides 7 academic summary formats: Executive Short, Detailed, Important Points, Key Definitions, Exam Topics, and Rapid Revision Notes.*
  > *Notice how cleanly it formats high-yield points with core formulas and definitions. Students can copy these notes with one click for rapid exam preparation."*

---

#### STEP 6: Demonstrate AI Examination Quiz Generator (Quiz Generator)
- **Action**: Click **Quiz Generator** in the sidebar.
- **Action**: Select *"GenAI and LLMs"*, set 3 Questions, Medium Difficulty, and click **Create Practice Quiz**.
- **Speaking Notes**:
  > *"To test understanding, UniMate dynamically generates university-standard multiple-choice questions with 4 options using Gemini. Let's answer the questions."*
- **Action**: Select options for the questions and click **Submit Examination Quiz**.
- **Speaking Notes**:
  > *"Upon submission, the system evaluates the score, calculates percentage, highlights correct answers in green and incorrect ones in red, and provides pedagogical explanations for each concept. The attempt is automatically recorded in SQLite."*

---

#### STEP 7: Demonstrate Personalized Study Planner (Study Planner)
- **Action**: Click **Study Planner** in the sidebar.
- **Action**: Show the active schedule for *"Generative AI & LLMs"*.
- **Speaking Notes**:
  > *"Here is the personalized AI Study Planner. Students enter their subject, topics, daily available study hours, and exam date. UniMate synthesizes a day-by-day timetable with theory blocks, practice sessions, break intervals, and revision tips.*
  > *As students complete topics, they check them off. Watch the progress bar update in real-time. This state is permanently stored in SQLite."*
- **Action**: Check off a topic and point to the progress percentage updating.

---

#### STEP 8: Demonstrate Real-Time Analytics (Analytics)
- **Action**: Click **Analytics** in the sidebar.
- **Speaking Notes**:
  > *"The Analytics dashboard visualizes real application telemetry using Recharts. Here is the Quiz Performance Bar Chart showing test scores, the Document Chunk Complexity Chart comparing pages and chunks in ChromaDB, the Study Topic Completion Ratio, and ChromaDB vector telemetry (384 dimensions, all-MiniLM-L6-v2).*
  > *All charts are computed dynamically from SQLite records—there are zero hardcoded fake metrics."*

---

#### STEP 9: Review GenAI Concepts & Architecture (GenAI Concepts)
- **Action**: Click **GenAI Concepts** in the sidebar.
- **Speaking Notes**:
  > *"Finally, we have created a dedicated 'GenAI Concepts' curriculum module specifically for the RTD Open Elective evaluation.*
  > *It covers 10 fundamental concepts: GenAI, LLMs, Gemini, Prompt Engineering, RAG, Text Embeddings, Semantic Search, Vector Databases, Chunking, and Grounding.*
  > *Each concept provides a formal definition, student-friendly explanation, real-world example, how it is used in UniMate, and the exact source code file.*
  > *Above, you can see the complete 6-layer End-to-End System Architecture Diagram and the 13-step RAG Workflow diagram."*

---

#### STEP 10: Conclusion & Examiner Questions
- **Speaking Notes**:
  > *"In summary, UniMate is a complete, working full-stack application running entirely locally on this laptop. It combines React, FastAPI, ChromaDB, Sentence Transformers, and Google Gemini to deliver genuine educational utility. Thank you, and I am now ready for your questions!"*
