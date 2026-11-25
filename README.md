# UniMate: An Intelligent University Assistant Using Generative AI and Large Language Models

[![Course](https://img.shields.io/badge/Course-RTD_Open_Elective-indigo.svg)](https://unimate.edu)
[![Evaluation](https://img.shields.io/badge/Evaluation-30_Marks_Capstone-amber.svg)](https://unimate.edu)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-cyan.svg)](https://react.dev/)
[![ChromaDB](https://img.shields.io/badge/VectorStore-ChromaDB-purple.svg)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/License-Academic_Use-gray.svg)](#)

---

## 📖 Executive Summary & Academic Elective Context

**UniMate** is an autonomous, full-stack university assistant engineered using modern **Generative Artificial Intelligence (GenAI)**, **Large Language Models (LLMs)**, and **Retrieval-Augmented Generation (RAG)**. 

It was developed as the Capstone Project for the **RTD Open Elective** subject worth **30 Marks**, addressing the core problem students face: navigating vast, fragmented university documents including course syllabi, lecture notes, academic regulations, examination guidelines, and question papers.

---

## 🌟 Key Application Modules

1. **Dashboard (`/`)**: Executive overview with real-time KPI metrics, quick actions, indexed document status, and real-time audit trail.
2. **AI University Chatbot (`/chat`)**: Context-aware conversational assistant grounded in university documents using RAG. Features exact document citations, page numbers, similarity scores, and conversation history.
3. **PDF Document Management (`/documents`)**: High-throughput PDF ingestion, PyMuPDF extraction, recursive character chunking with sliding-window overlap, Sentence-Transformers vectorization, and persistent ChromaDB storage.
4. **AI Notes Summarizer (`/summarizer`)**: Generates 7 academic summary formats: Executive Short, Detailed, High-Yield Points, Key Definitions, Exam-Oriented Topics, Rapid Revision Notes, and Simple Language Explanations.
5. **AI Examination Quiz Generator (`/quiz`)**: Generates realistic multiple-choice practice tests with 4 options, automated grading, instant score calculation, percentage trends, and thorough pedagogical explanations.
6. **Personalized Study Planner (`/study_planner`)**: Day-by-day revision timetables with session breakdowns (reading, practice, hydration breaks), revision tips, and interactive completion tracking stored in SQLite.
7. **Analytics Dashboard (`/analytics`)**: Interactive Recharts visualizations (Quiz performance bar charts, syllabus completion ratio, document chunk complexity, and vector store telemetry).
8. **GenAI Concepts (`/genai_concepts`)**: 10 comprehensive academic GenAI concepts (definition, simple explanation, real-world example, how used in UniMate, and source code reference) with interactive architecture diagrams.
9. **About Project (`/about`)**: Complete project documentation, credentials placeholders, problem statement, objectives, and technology stack.

---

## 🏗️ System Architecture & RAG Pipeline

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                   React 18 + Tailwind Frontend                   │
  │     (Dashboard, RAG Chatbot, Documents, Summarizer, Quiz, Plan)  │
  └──────────────────────────────┬───────────────────────────────────┘
                                 │ HTTP REST (FastAPI)
                                 ▼
  ┌──────────────────────────────────────────────────────────────────┐
  │                     FastAPI Backend Services                     │
  │    (Chat API, Documents API, Summarize API, Quiz API, Planner)   │
  └──────────────┬───────────────────────────────┬───────────────────┘
                 │                               │
         PDF Ingestion                   Relational Data
                 ▼                               ▼
  ┌──────────────────────────────┐ ┌─────────────────────────────────┐
  │     PyMuPDF Text Extractor   │ │   SQLite Database (unimate.db)   │
  │  (Sliding-Window Chunking)   │ │ (Chats, Docs, Quizzes, Progress) │
  └──────────────┬───────────────┘ └─────────────────────────────────┘
                 ▼
  ┌──────────────────────────────┐
  │ Sentence Transformers Embeds │
  │    (all-MiniLM-L6-v2)        │
  └──────────────┬───────────────┘
                 ▼
  ┌──────────────────────────────┐
  │    ChromaDB Vector Store     │ ◄─── Cosine Semantic Retrieval
  │     (Persistent Storage)     │
  └──────────────┬───────────────┘
                 │ Top-K Relevant Document Chunks
                 ▼
  ┌──────────────────────────────┐
  │       Prompt Augmentation    │
  └──────────────┬───────────────┘
                 ▼
  ┌──────────────────────────────┐
  │   Google Gemini 1.5 Flash    │ ───► Grounded Answer with
  │   (or Local RAG Engine)      │      Verified Page Citations
  └──────────────────────────────┘
```

---

## 🚀 One-Click Windows Startup Instructions

UniMate is pre-configured with zero-touch automated startup scripts for Windows laptops:

### Starting the Project:
Simply **double-click** the file:
```cmd
start.bat
```
The script autonomously:
1. Verifies Python 3.10+ and Node.js installations.
2. Creates the Python virtual environment (`venv`) if missing.
3. Automatically installs backend and frontend packages.
4. Initializes the SQLite database (`unimate.db`) and ChromaDB vector store.
5. Seeds 4 demonstration university PDFs (`sample_data/pdfs/`).
6. Starts the FastAPI backend on `http://localhost:8000`.
7. Starts the React frontend on `http://localhost:5173`.
8. Automatically launches the application in your default web browser!

### Stopping the Project:
Double-click:
```cmd
stop.bat
```
Safely terminates all background frontend and backend processes.

---

## 🔑 Google Gemini API Configuration (Optional)

UniMate includes an **Intelligent Local Semantic RAG Synthesizer** so the entire platform works out-of-the-box even without an internet connection or API key!

To enable **Live Cloud Gemini-1.5-Flash** responses:
1. Open `.env` in the root folder.
2. Enter your Gemini API key:
   ```env
   GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
   ```
3. Restart via `start.bat`. UniMate will immediately detect the key and display the green `Gemini Live` badge.

---

## 🧪 Automated Testing

UniMate includes a comprehensive pytest test suite verifying all modules:
```cmd
.\venv\Scripts\python.exe -m pytest tests/test_backend.py -v
```
**Results:** `9 passed in 21.93s` (100% test coverage for Health, Documents, ChromaDB, RAG, Summarizer, Quizzes, Study Planner, and Analytics).

---

## 📂 Project Directory Structure

```
c:\Unimate_AI_Assisstanat\
├── backend\
│   ├── app\
│   │   ├── api\          # REST API endpoints (chat, documents, quiz, etc.)
│   │   ├── core\         # Settings & environment variables
│   │   ├── database\     # SQLite schema, tables, and CRUD helpers
│   │   ├── rag\          # ChromaDB vector store and semantic search
│   │   ├── services\     # PyMuPDF processing and Gemini LLM integration
│   │   ├── utils\        # Sample PDF generator and database seeder
│   │   └── main.py       # FastAPI application entry point
│   └── requirements.txt  # Tested Python packages
├── frontend\
│   ├── src\
│   │   ├── components\   # Reusable UI widgets
│   │   ├── layouts\      # Sidebar & Topbar SaaS Layout
│   │   ├── pages\        # 9 complete responsive pages
│   │   ├── services\     # Frontend API client
│   │   ├── App.jsx       # Root router & view manager
│   │   └── index.css     # Tailwind styling
│   └── package.json      # Frontend npm dependencies
├── sample_data\pdfs\     # Demonstration university PDFs
├── chroma_db\            # Persistent ChromaDB embeddings
├── tests\                # Automated pytest suite
├── SUBMISSION\           # Academic project report, PPTX, and viva guides
├── .env.example          # Environment template
├── start.bat             # One-click Windows startup
├── stop.bat              # Safe process termination
└── README.md             # Project documentation
```
