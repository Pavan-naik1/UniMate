import React from "react";
import {
  GraduationCap,
  Info,
  CheckCircle2,
  Code2,
  Cpu,
  Layers,
  Sparkles,
  Award,
  Terminal,
  ShieldCheck,
  Zap
} from "lucide-react";

export default function AboutProject() {
  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Hero Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-indigo-900 to-slate-900 text-white p-8 border border-slate-800 shadow-xl">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold mb-4 border border-indigo-500/30">
          <Award className="w-3.5 h-3.5 text-amber-400" /> Academic Capstone Project | Generative AI & LLMs
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
          UniMate: An Intelligent University Assistant Using Generative AI and Large Language Models
        </h1>
        <p className="mt-3 text-slate-300 text-xs sm:text-sm leading-relaxed max-w-3xl">
          An autonomous, end-to-end educational platform applying state-of-the-art Generative AI, Retrieval-Augmented Generation (RAG), and vector database semantic search to empower university students with contextual academic assistance.
        </p>
      </div>

      {/* Academic Submission Information Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
        <h3 className="font-bold text-slate-900 text-sm mb-4 flex items-center gap-2">
          <GraduationCap className="w-4 h-4 text-indigo-600" /> Academic Project Credentials
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span className="text-slate-400 text-[10px] uppercase font-bold block">Domain / Track</span>
            <span className="font-bold text-slate-800 mt-0.5 block">Generative AI & LLM Systems</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span className="text-slate-400 text-[10px] uppercase font-bold block">Project Type</span>
            <span className="font-bold text-indigo-600 mt-0.5 block">Full-Stack RAG University Assistant</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span className="text-slate-400 text-[10px] uppercase font-bold block">Student Name & USN</span>
            <span className="font-bold text-slate-800 mt-0.5 block">[STUDENT_NAME_PLACEHOLDER]</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span className="text-slate-400 text-[10px] uppercase font-bold block">Faculty Guide</span>
            <span className="font-bold text-slate-800 mt-0.5 block">[FACULTY_GUIDE_PLACEHOLDER]</span>
          </div>
        </div>
      </div>

      {/* Abstract & Problem Statement */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-3">
          <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
            <Info className="w-4 h-4 text-indigo-600" /> Project Abstract
          </h3>
          <p className="text-xs sm:text-sm text-slate-700 leading-relaxed">
            University students navigate voluminous course syllabi, extensive textbook materials, complex academic regulations, and examination guidelines dispersed across multiple disparate PDFs. UniMate resolves this cognitive bottleneck by integrating PyMuPDF text extraction, sliding-window chunking, dense Sentence-Transformers vector embeddings, ChromaDB semantic vector search, and Google Gemini LLM synthesis. The system produces factual, non-hallucinated answers accompanied by page-level citations, notes summaries, dynamic practice quizzes, and customizable daily revision timetables.
          </p>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-3">
          <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-rose-600" /> Problem Statement
          </h3>
          <p className="text-xs sm:text-sm text-slate-700 leading-relaxed">
            Traditional institutional web portals rely on rigid keyword queries or manual browsing, making information retrieval tedious and error-prone. Conversely, raw public LLMs frequently suffer from hallucinations, lack institutional syllabus knowledge, and cannot furnish verifiable page references. UniMate bridges this critical gap through a local Retrieval-Augmented Generation architecture that grounds generative capabilities in official university documents.
          </p>
        </div>
      </div>

      {/* Key Objectives & Proposed Solution */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-4">
        <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Objectives and Proposed Solution
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-100 space-y-1">
            <h4 className="font-bold text-slate-900">1. Contextual RAG Retrieval</h4>
            <p className="text-slate-600">Provide verifiable natural language Q&A strictly grounded in indexed university PDFs with document and page citations.</p>
          </div>
          <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-100 space-y-1">
            <h4 className="font-bold text-slate-900">2. Examination Assistance</h4>
            <p className="text-slate-600">Generate multi-format academic notes (definitions, exam topics, bulleted key points) and self-grading interactive quizzes.</p>
          </div>
          <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-100 space-y-1">
            <h4 className="font-bold text-slate-900">3. Personalized Timetables</h4>
            <p className="text-slate-600">Synthesize structured day-by-day study plans with topic prioritization, break intervals, and SQLite completion tracking.</p>
          </div>
        </div>
      </div>

      {/* Technology Stack Grid */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-4">
        <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
          <Code2 className="w-4 h-4 text-indigo-600" /> Full-Stack Technology Stack
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3 text-center">
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-800 text-xs block">React 18 & Vite</span>
            <span className="text-[10px] text-slate-400">Frontend UI</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-800 text-xs block">Tailwind CSS</span>
            <span className="text-[10px] text-slate-400">SaaS Styling</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-800 text-xs block">FastAPI</span>
            <span className="text-[10px] text-slate-400">Python REST API</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-800 text-xs block">ChromaDB</span>
            <span className="text-[10px] text-slate-400">Vector Store</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-800 text-xs block">PyMuPDF</span>
            <span className="text-[10px] text-slate-400">PDF Extraction</span>
          </div>
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span className="font-bold text-slate-800 text-xs block">Google Gemini</span>
            <span className="text-[10px] text-slate-400">GenAI & LLM</span>
          </div>
        </div>
      </div>

      {/* Future Scope */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-3">
        <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
          <Zap className="w-4 h-4 text-amber-500" /> Future Enhancements
        </h3>
        <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-700">
          <li className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-indigo-600"></div> Multilingual regional language translation for lecture notes.
          </li>
          <li className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-indigo-600"></div> Voice-activated audio queries for visually impaired students.
          </li>
          <li className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-indigo-600"></div> Automated OCR parsing for handwritten lecture whiteboards.
          </li>
          <li className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-indigo-600"></div> Direct LMS integration with Canvas, Moodle, and Google Classroom.
          </li>
        </ul>
      </div>
    </div>
  );
}
