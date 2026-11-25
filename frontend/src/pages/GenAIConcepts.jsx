import React, { useState, useEffect } from "react";
import {
  Sparkles,
  BrainCircuit,
  FileCode,
  Layers,
  ArrowRight,
  Database,
  Search,
  BookOpen,
  Cpu,
  GraduationCap,
  Network
} from "lucide-react";
import { getGenAIConcepts } from "../services/api";

export default function GenAIConcepts() {
  const [data, setData] = useState(null);
  const [selectedConcept, setSelectedConcept] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getGenAIConcepts()
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load GenAI concepts:", err);
        setLoading(false);
      });
  }, []);

  const concepts = data?.concepts || [];
  const currentConcept = concepts.find((c) => c.id === selectedConcept) || concepts[0];

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 to-indigo-950 p-6 sm:p-8 rounded-2xl text-white shadow-lg border border-slate-800">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold mb-3 border border-indigo-500/30">
          <GraduationCap className="w-3.5 h-3.5 text-amber-400" /> Core Engineering & Architecture Reference
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
          GenAI & LLM Theoretical Concepts
        </h1>
        <p className="mt-2 text-slate-300 text-xs sm:text-sm max-w-3xl leading-relaxed">
          Comprehensive academic explanations of the core foundational concepts powering UniMate, including mathematical representations, prompt design principles, vector search, and contextual retrieval architectures.
        </p>
      </div>

      {/* Visual System Architecture Diagram (Interactive Card) */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-6">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div>
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Network className="w-5 h-5 text-indigo-600" /> UniMate End-to-End System Architecture
            </h2>
            <p className="text-xs text-slate-500">
              Interaction flow across Presentation, API, PDF Ingestion, Vector Embedding, and Cognitive LLM Layers
            </p>
          </div>
          <span className="px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-700 text-xs font-semibold">
            6 Core Layers
          </span>
        </div>

        {/* Interactive Architecture Flow Diagram */}
        <div className="grid grid-cols-1 md:grid-cols-6 gap-3">
          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-center flex flex-col items-center justify-between">
            <span className="text-[10px] uppercase font-bold text-indigo-600 mb-1">Layer 1</span>
            <div className="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center my-2 font-bold text-xs">UI</div>
            <h4 className="font-bold text-xs text-slate-800">React Frontend</h4>
            <p className="text-[10px] text-slate-500 mt-1">SaaS Dashboard, Chatbot, Recharts</p>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-center flex flex-col items-center justify-between">
            <span className="text-[10px] uppercase font-bold text-blue-600 mb-1">Layer 2</span>
            <div className="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center my-2 font-bold text-xs">API</div>
            <h4 className="font-bold text-xs text-slate-800">FastAPI Backend</h4>
            <p className="text-[10px] text-slate-500 mt-1">REST Endpoints & SQLite CRUD</p>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-center flex flex-col items-center justify-between">
            <span className="text-[10px] uppercase font-bold text-purple-600 mb-1">Layer 3</span>
            <div className="w-8 h-8 rounded-lg bg-purple-100 text-purple-700 flex items-center justify-center my-2 font-bold text-xs">PDF</div>
            <h4 className="font-bold text-xs text-slate-800">PyMuPDF Ingestion</h4>
            <p className="text-[10px] text-slate-500 mt-1">Extraction & Sliding Overlap Chunking</p>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-center flex flex-col items-center justify-between">
            <span className="text-[10px] uppercase font-bold text-violet-600 mb-1">Layer 4</span>
            <div className="w-8 h-8 rounded-lg bg-violet-100 text-violet-700 flex items-center justify-center my-2 font-bold text-xs">VEC</div>
            <h4 className="font-bold text-xs text-slate-800">ChromaDB Store</h4>
            <p className="text-[10px] text-slate-500 mt-1">Sentence Transformers Embeddings</p>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-center flex flex-col items-center justify-between">
            <span className="text-[10px] uppercase font-bold text-amber-600 mb-1">Layer 5</span>
            <div className="w-8 h-8 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center my-2 font-bold text-xs">RAG</div>
            <h4 className="font-bold text-xs text-slate-800">RAG Context Engine</h4>
            <p className="text-[10px] text-slate-500 mt-1">Cosine Retrieval & Citations Mapping</p>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 text-center flex flex-col items-center justify-between">
            <span className="text-[10px] uppercase font-bold text-emerald-600 mb-1">Layer 6</span>
            <div className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center my-2 font-bold text-xs">LLM</div>
            <h4 className="font-bold text-xs text-slate-800">Google Gemini</h4>
            <p className="text-[10px] text-slate-500 mt-1">Cognitive Synthesis & Grounded Output</p>
          </div>
        </div>

        {/* Visual RAG Step-by-Step Flow */}
        <div className="p-4 rounded-xl bg-gradient-to-r from-indigo-50/60 to-violet-50/60 border border-indigo-100">
          <h4 className="font-bold text-xs text-indigo-900 mb-2 uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" /> Complete RAG Pipeline Lifecycle (13-Step Academic Workflow)
          </h4>
          <div className="flex flex-wrap items-center gap-2 text-[11px] text-slate-700">
            <span className="px-2 py-1 bg-white rounded border border-slate-200 font-semibold">1. Upload PDF</span>
            <ArrowRight className="w-3 h-3 text-slate-400" />
            <span className="px-2 py-1 bg-white rounded border border-slate-200 font-semibold">2. PyMuPDF Extraction</span>
            <ArrowRight className="w-3 h-3 text-slate-400" />
            <span className="px-2 py-1 bg-white rounded border border-slate-200 font-semibold">3. Sliding Overlap Chunking</span>
            <ArrowRight className="w-3 h-3 text-slate-400" />
            <span className="px-2 py-1 bg-white rounded border border-slate-200 font-semibold">4. Sentence-Transformers Vectorization</span>
            <ArrowRight className="w-3 h-3 text-slate-400" />
            <span className="px-2 py-1 bg-white rounded border border-slate-200 font-semibold">5. ChromaDB HNSW Indexing</span>
            <ArrowRight className="w-3 h-3 text-slate-400" />
            <span className="px-2 py-1 bg-white rounded border border-slate-200 font-semibold">6. Student Query Input</span>
            <ArrowRight className="w-3 h-3 text-slate-400" />
            <span className="px-2 py-1 bg-white rounded border border-slate-200 font-semibold">7. Query Embedding</span>
            <ArrowRight className="w-3 h-3 text-slate-400" />
            <span className="px-2 py-1 bg-white rounded border border-slate-200 font-semibold">8. Cosine Similarity Retrieval</span>
            <ArrowRight className="w-3 h-3 text-slate-400" />
            <span className="px-2 py-1 bg-white rounded border border-slate-200 font-semibold">9. Context Augmentation</span>
            <ArrowRight className="w-3 h-3 text-slate-400" />
            <span className="px-2 py-1 bg-white rounded border border-slate-200 font-semibold">10. Gemini LLM Synthesis</span>
            <ArrowRight className="w-3 h-3 text-slate-400" />
            <span className="px-2 py-1 bg-emerald-600 text-white rounded font-bold shadow-sm">11. Grounded Output with Page Citations</span>
          </div>
        </div>
      </div>

      {/* 10 Core GenAI Concepts Navigator */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left concept tabs */}
        <div className="lg:col-span-4 space-y-2">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2 px-1">
            Curriculum Concepts (10)
          </span>
          <div className="space-y-1.5 max-h-[560px] overflow-y-auto pr-1">
            {concepts.map((c) => (
              <button
                key={c.id}
                onClick={() => setSelectedConcept(c.id)}
                className={`w-full text-left p-3 rounded-xl border transition flex items-center justify-between text-xs ${
                  selectedConcept === c.id
                    ? "bg-indigo-600 text-white border-indigo-600 shadow-md shadow-indigo-600/20"
                    : "bg-white border-slate-200 text-slate-700 hover:bg-slate-50"
                }`}
              >
                <div className="flex items-center gap-2.5 truncate">
                  <span className={`w-5 h-5 rounded-full flex items-center justify-center font-bold text-[10px] ${
                    selectedConcept === c.id ? "bg-white/20 text-white" : "bg-slate-100 text-slate-600"
                  }`}>
                    {c.id}
                  </span>
                  <span className="font-semibold truncate">{c.title}</span>
                </div>
                <span className={`text-[10px] px-1.5 py-0.5 rounded ${
                  selectedConcept === c.id ? "bg-white/20 text-white" : "bg-slate-100 text-slate-500"
                }`}>
                  {c.badge}
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Right Concept In-depth Card */}
        <div className="lg:col-span-8">
          {currentConcept && (
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-5">
              {/* Concept Title & Badge */}
              <div className="pb-4 border-b border-slate-200 flex flex-wrap items-center justify-between gap-2">
                <div>
                  <span className="text-[11px] font-bold text-indigo-600 uppercase tracking-wider block">
                    Concept #{currentConcept.id} • {currentConcept.badge}
                  </span>
                  <h2 className="text-xl sm:text-2xl font-extrabold text-slate-900 mt-0.5">
                    {currentConcept.title}
                  </h2>
                </div>
              </div>

              {/* Formal Academic Definition */}
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5 text-indigo-600" /> Formal Academic Definition
                </h4>
                <p className="text-xs sm:text-sm text-slate-800 leading-relaxed font-medium">
                  {currentConcept.definition}
                </p>
              </div>

              {/* Simple Student Explanation */}
              <div>
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-amber-500" /> Simplified Explanation for Students
                </h4>
                <p className="text-xs sm:text-sm text-slate-700 leading-relaxed">
                  {currentConcept.simple_explanation}
                </p>
              </div>

              {/* Real World Example */}
              <div>
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                  <Cpu className="w-3.5 h-3.5 text-blue-500" /> Real-World Example
                </h4>
                <p className="text-xs sm:text-sm text-slate-700 leading-relaxed bg-blue-50/50 p-3 rounded-lg border border-blue-100">
                  {currentConcept.real_world_example}
                </p>
              </div>

              {/* How it is implemented in UniMate */}
              <div>
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5 text-emerald-600" /> How It Is Used in UniMate
                </h4>
                <p className="text-xs sm:text-sm text-slate-700 leading-relaxed bg-emerald-50/50 p-3 rounded-lg border border-emerald-100">
                  {currentConcept.used_in_unimate}
                </p>
              </div>

              {/* Relevant implementation file or code reference */}
              <div className="pt-3 border-t border-slate-200 flex items-center justify-between text-xs">
                <span className="text-slate-500 flex items-center gap-1.5">
                  <FileCode className="w-4 h-4 text-indigo-600" /> Implementation Source:
                </span>
                <code className="px-2.5 py-1 rounded bg-slate-100 text-indigo-700 font-mono font-semibold text-[11px] border border-slate-200">
                  {currentConcept.code_reference}
                </code>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
