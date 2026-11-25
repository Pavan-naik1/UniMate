import React, { useState, useEffect } from "react";
import {
  FileText,
  MessageSquare,
  BrainCircuit,
  CalendarCheck2,
  TrendingUp,
  Clock,
  ArrowRight,
  Sparkles,
  BookOpen,
  CheckCircle2,
  FileSpreadsheet
} from "lucide-react";
import { getAnalytics, getDocuments } from "../services/api";

export default function Dashboard({ setActivePage }) {
  const [data, setData] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getAnalytics(), getDocuments()])
      .then(([analyticsRes, docsRes]) => {
        setData(analyticsRes);
        setDocuments(docsRes || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Dashboard data error:", err);
        setLoading(false);
      });
  }, []);

  const metrics = data?.metrics || {
    total_documents: documents.length || 4,
    total_questions: 0,
    total_quizzes_attempted: 0,
    study_progress_percentage: 0,
    average_quiz_score: 0,
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-indigo-900 via-indigo-800 to-violet-900 p-6 sm:p-8 text-white shadow-xl shadow-indigo-950/20">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-indigo-200 text-xs font-semibold mb-4 border border-white/10">
            <Sparkles className="w-3.5 h-3.5 text-amber-300" /> Intelligent Academic Platform
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            UniMate: Your Generative AI Academic Assistant
          </h1>
          <p className="mt-2 text-indigo-100 text-sm sm:text-base leading-relaxed">
            Upload university syllabi, lecture notes, regulations, and question papers. 
            Ask questions with semantic RAG citations, generate exam summaries, solve quizzes, and organize your study schedule.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <button
              onClick={() => setActivePage("chat")}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white text-indigo-950 font-semibold text-sm hover:bg-indigo-50 transition shadow-lg shadow-black/10"
            >
              <MessageSquare className="w-4 h-4 text-indigo-600" /> Start Academic Chat
            </button>
            <button
              onClick={() => setActivePage("documents")}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-700/60 hover:bg-indigo-700 text-white font-medium text-sm border border-indigo-400/30 transition backdrop-blur-md"
            >
              <FileText className="w-4 h-4" /> Manage Documents
            </button>
          </div>
        </div>
        {/* Background decorative graphic */}
        <div className="absolute right-0 bottom-0 opacity-10 pointer-events-none transform translate-x-10 translate-y-10">
          <BrainCircuit className="w-96 h-96" />
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Indexed Documents</span>
            <div className="w-9 h-9 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600">
              <FileText className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-slate-800">{metrics.total_documents}</span>
            <span className="text-xs text-emerald-600 font-medium">In ChromaDB</span>
          </div>
          <p className="mt-1 text-xs text-slate-400">PDFs processed & vectorized</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Questions Answered</span>
            <div className="w-9 h-9 rounded-lg bg-blue-50 flex items-center justify-center text-blue-600">
              <MessageSquare className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-slate-800">{metrics.total_questions}</span>
            <span className="text-xs text-indigo-600 font-medium">RAG Queries</span>
          </div>
          <p className="mt-1 text-xs text-slate-400">With page citations</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Quizzes Attempted</span>
            <div className="w-9 h-9 rounded-lg bg-purple-50 flex items-center justify-center text-purple-600">
              <BrainCircuit className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-slate-800">{metrics.total_quizzes_attempted}</span>
            <span className="text-xs text-purple-600 font-medium">
              {metrics.average_quiz_score ? `${metrics.average_quiz_score}% Avg` : "Ready"}
            </span>
          </div>
          <p className="mt-1 text-xs text-slate-400">GenAI generated assessments</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Study Progress</span>
            <div className="w-9 h-9 rounded-lg bg-emerald-50 flex items-center justify-center text-emerald-600">
              <CalendarCheck2 className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-slate-800">{metrics.study_progress_percentage}%</span>
            <span className="text-xs text-emerald-600 font-medium">Topics Done</span>
          </div>
          <div className="mt-2 w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
            <div 
              className="bg-emerald-500 h-1.5 rounded-full transition-all duration-500" 
              style={{ width: `${Math.min(100, metrics.study_progress_percentage || 5)}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Quick Action Feature Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <button
          onClick={() => setActivePage("chat")}
          className="p-4 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-600 text-white text-left hover:scale-[1.02] transition shadow-sm"
        >
          <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center mb-3">
            <MessageSquare className="w-4 h-4 text-white" />
          </div>
          <h3 className="font-bold text-sm">Academic Chatbot</h3>
          <p className="text-xs text-indigo-100 mt-1">Ask questions across all uploaded university PDFs</p>
        </button>

        <button
          onClick={() => setActivePage("summarizer")}
          className="p-4 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 text-white text-left hover:scale-[1.02] transition shadow-sm"
        >
          <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center mb-3">
            <FileSpreadsheet className="w-4 h-4 text-white" />
          </div>
          <h3 className="font-bold text-sm">AI Notes Summarizer</h3>
          <p className="text-xs text-violet-100 mt-1">Extract high-yield exam points & definitions</p>
        </button>

        <button
          onClick={() => setActivePage("quiz")}
          className="p-4 rounded-xl bg-gradient-to-br from-sky-500 to-blue-600 text-white text-left hover:scale-[1.02] transition shadow-sm"
        >
          <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center mb-3">
            <BrainCircuit className="w-4 h-4 text-white" />
          </div>
          <h3 className="font-bold text-sm">Quiz Generator</h3>
          <p className="text-xs text-sky-100 mt-1">Create multiple-choice exam practice questions</p>
        </button>

        <button
          onClick={() => setActivePage("study_planner")}
          className="p-4 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 text-white text-left hover:scale-[1.02] transition shadow-sm"
        >
          <div className="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center mb-3">
            <CalendarCheck2 className="w-4 h-4 text-white" />
          </div>
          <h3 className="font-bold text-sm">AI Study Planner</h3>
          <p className="text-xs text-emerald-100 mt-1">Auto-generate day-by-day revision timetables</p>
        </button>
      </div>

      {/* Two Column Layout: Recent Documents & Activity Log */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Preloaded Documents */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 shadow-sm p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="font-bold text-base text-slate-800">Indexed University Documents</h2>
              <p className="text-xs text-slate-500">Documents available for natural language queries and RAG</p>
            </div>
            <button
              onClick={() => setActivePage("documents")}
              className="text-xs font-semibold text-indigo-600 hover:text-indigo-700 flex items-center gap-1"
            >
              View All <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="divide-y divide-slate-100">
            {documents.slice(0, 5).map((doc) => (
              <div key={doc.id} className="py-3 flex items-center justify-between hover:bg-slate-50/50 px-2 rounded-lg transition">
                <div className="flex items-center gap-3 min-w-0">
                  <div className="w-9 h-9 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600 flex-shrink-0">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div className="min-w-0">
                    <h4 className="text-sm font-semibold text-slate-800 truncate">{doc.original_name}</h4>
                    <p className="text-xs text-slate-400">
                      {doc.page_count} pages • {doc.chunk_count} semantic chunks • {(doc.file_size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-100">
                    Vectorized
                  </span>
                  <button
                    onClick={() => setActivePage("chat")}
                    className="p-1.5 rounded-lg text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 transition"
                    title="Ask question about this document"
                  >
                    <MessageSquare className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Recent Activities Audit Trail */}
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="font-bold text-base text-slate-800">System Activity</h2>
              <p className="text-xs text-slate-500">Real-time application audit trail</p>
            </div>
            <Clock className="w-4 h-4 text-slate-400" />
          </div>

          <div className="flex-1 space-y-3 overflow-y-auto max-h-[340px]">
            {data?.recent_activities?.length > 0 ? (
              data.recent_activities.map((act) => (
                <div key={act.id} className="p-2.5 rounded-lg bg-slate-50 border border-slate-100 text-xs">
                  <div className="flex items-center justify-between text-slate-600 font-medium">
                    <span className="capitalize">{act.action_type.replace('_', ' ')}</span>
                    <span className="text-[10px] text-slate-400">{act.created_at?.slice(11, 16) || "Just now"}</span>
                  </div>
                  <p className="text-slate-800 mt-1 line-clamp-2">{act.description}</p>
                </div>
              ))
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center py-8 text-slate-400">
                <BookOpen className="w-8 h-8 text-slate-300 mb-2" />
                <p className="text-xs">No recent activity yet.</p>
                <p className="text-[11px] text-slate-400">Ask a question or upload a PDF to begin!</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
