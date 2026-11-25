import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area
} from "recharts";
import {
  BarChart3,
  TrendingUp,
  FileText,
  MessageSquare,
  BrainCircuit,
  CalendarCheck2,
  Clock,
  Sparkles,
  Layers,
  Database
} from "lucide-react";
import { getAnalytics } from "../services/api";

const COLORS = ["#4f46e5", "#818cf8", "#10b981", "#f59e0b", "#ec4899"];

export default function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAnalytics()
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load analytics:", err);
        setLoading(false);
      });
  }, []);

  const metrics = data?.metrics || {
    total_documents: 0,
    total_questions: 0,
    total_quizzes_attempted: 0,
    average_quiz_score: 0,
    total_study_topics: 0,
    completed_study_topics: 0,
    study_progress_percentage: 0,
  };

  // Prepare chart data
  const quizScores = data?.quiz_chart_data || [];
  
  // Topic completion distribution for Pie Chart
  const studyDistribution = [
    { name: "Completed Topics", value: metrics.completed_study_topics || 0 },
    { name: "Pending Topics", value: Math.max(0, (metrics.total_study_topics || 0) - (metrics.completed_study_topics || 0)) },
  ];

  // Document chunk size comparison data
  const docChunkData = (metrics.recent_documents || []).map((d) => ({
    name: d.original_name.replace(".pdf", "").slice(0, 16),
    chunks: d.chunk_count,
    pages: d.page_count,
  }));

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-800">
            Academic Performance & Analytics
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Real-time analytics computed directly from your SQLite database, ChromaDB vector store, and quiz interactions.
          </p>
        </div>
      </div>

      {/* KPI Metrics Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase">Total Documents</span>
            <FileText className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="mt-2 text-2xl font-extrabold text-slate-900">{metrics.total_documents}</div>
          <p className="mt-1 text-[11px] text-slate-400">Indexed in ChromaDB</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase">Questions Asked</span>
            <MessageSquare className="w-4 h-4 text-blue-600" />
          </div>
          <div className="mt-2 text-2xl font-extrabold text-slate-900">{metrics.total_questions}</div>
          <p className="mt-1 text-[11px] text-slate-400">RAG chatbot queries</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase">Avg Quiz Score</span>
            <BrainCircuit className="w-4 h-4 text-purple-600" />
          </div>
          <div className="mt-2 text-2xl font-extrabold text-slate-900">{metrics.average_quiz_score}%</div>
          <p className="mt-1 text-[11px] text-slate-400">{metrics.total_quizzes_attempted} tests completed</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500">
            <span className="text-xs font-semibold uppercase">Study Progress</span>
            <CalendarCheck2 className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="mt-2 text-2xl font-extrabold text-slate-900">{metrics.study_progress_percentage}%</div>
          <p className="mt-1 text-[11px] text-slate-400">
            {metrics.completed_study_topics}/{metrics.total_study_topics} topics checked
          </p>
        </div>
      </div>

      {/* Main Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Quiz Scores Bar Chart */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-800 text-sm">Quiz Performance</h3>
              <p className="text-xs text-slate-500">Percentage scored on recent university practice tests</p>
            </div>
            <TrendingUp className="w-4 h-4 text-indigo-600" />
          </div>

          <div className="h-64 w-full">
            {quizScores.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={quizScores}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="name" stroke="#94a3b8" fontSize={11} tickLine={false} />
                  <YAxis stroke="#94a3b8" fontSize={11} domain={[0, 100]} unit="%" />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#1e1b4b", borderRadius: "8px", border: "none", color: "#fff", fontSize: "12px" }}
                  />
                  <Bar dataKey="score" fill="#4f46e5" radius={[6, 6, 0, 0]} name="Score (%)" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center text-slate-400">
                <BrainCircuit className="w-10 h-10 text-slate-200 mb-2" />
                <p className="text-xs">No quiz scores recorded yet.</p>
                <p className="text-[11px] text-slate-400">Attempt a practice quiz in the Quiz Generator.</p>
              </div>
            )}
          </div>
        </div>

        {/* Chart 2: Document Indexing Breakdown */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-800 text-sm">Indexed Document Complexity</h3>
              <p className="text-xs text-slate-500">Page count vs generated semantic chunks in ChromaDB</p>
            </div>
            <Layers className="w-4 h-4 text-violet-600" />
          </div>

          <div className="h-64 w-full">
            {docChunkData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={docChunkData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="name" stroke="#94a3b8" fontSize={10} tickLine={false} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#1e1b4b", borderRadius: "8px", border: "none", color: "#fff", fontSize: "12px" }}
                  />
                  <Bar dataKey="chunks" fill="#6366f1" radius={[4, 4, 0, 0]} name="Semantic Chunks" />
                  <Bar dataKey="pages" fill="#c7d2fe" radius={[4, 4, 0, 0]} name="Total Pages" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center text-slate-400">
                <FileText className="w-10 h-10 text-slate-200 mb-2" />
                <p className="text-xs">No documents available.</p>
              </div>
            )}
          </div>
        </div>

        {/* Chart 3: Study Topic Completion Ratio */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-800 text-sm">Study Topic Completion Ratio</h3>
              <p className="text-xs text-slate-500">Tracked vs pending syllabus topics</p>
            </div>
            <CalendarCheck2 className="w-4 h-4 text-emerald-600" />
          </div>

          <div className="h-64 w-full flex items-center justify-center">
            {metrics.total_study_topics > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={studyDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={85}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    <Cell fill="#10b981" />
                    <Cell fill="#e2e8f0" />
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: "#1e1b4b", borderRadius: "8px", color: "#fff", fontSize: "12px" }} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="text-center text-slate-400">
                <CalendarCheck2 className="w-10 h-10 text-slate-200 mx-auto mb-2" />
                <p className="text-xs">No study topics tracked yet.</p>
                <p className="text-[11px] text-slate-400">Create a plan in Study Planner to see completion breakdown.</p>
              </div>
            )}
          </div>
        </div>

        {/* Chart 4: Vector Store & System Health Info */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-bold text-slate-800 text-sm">System & Vector Store Telemetry</h3>
              <Database className="w-4 h-4 text-indigo-600" />
            </div>
            <p className="text-xs text-slate-500 mb-4">
              Real-time operational parameters for the university assistant engine.
            </p>

            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
                <span className="text-slate-600 font-medium">ChromaDB Collection</span>
                <span className="font-bold text-slate-900">{data?.vector_store_stats?.collection_name || "unimate_knowledge_base"}</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
                <span className="text-slate-600 font-medium">Vector Dimension</span>
                <span className="font-bold text-indigo-600">384 Dimensions (all-MiniLM-L6-v2)</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
                <span className="text-slate-600 font-medium">Total Vector Chunks</span>
                <span className="font-bold text-slate-900">{data?.vector_store_stats?.total_chunks || 0} Chunks</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
                <span className="text-slate-600 font-medium">Active AI Engine</span>
                <span className="font-bold text-slate-900">{data?.ai_engine_status?.model || "Local RAG Mode"}</span>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-400 flex items-center justify-between">
            <span>Database: SQLite 3 (unimate.db)</span>
            <span className="text-emerald-600 font-medium flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Online & Persistent
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
