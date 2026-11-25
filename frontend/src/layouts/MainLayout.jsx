import React, { useState, useEffect } from "react";
import {
  LayoutDashboard,
  MessageSquare,
  FileText,
  FileSpreadsheet,
  BrainCircuit,
  CalendarCheck2,
  BarChart3,
  Sparkles,
  Info,
  GraduationCap,
  Menu,
  X,
  Cpu,
  CheckCircle2,
  AlertCircle
} from "lucide-react";
import { checkHealth } from "../services/api";

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "chat", label: "AI Chatbot", icon: MessageSquare },
  { id: "documents", label: "My Documents", icon: FileText },
  { id: "summarizer", label: "AI Summarizer", icon: FileSpreadsheet },
  { id: "quiz", label: "Quiz Generator", icon: BrainCircuit },
  { id: "study_planner", label: "Study Planner", icon: CalendarCheck2 },
  { id: "analytics", label: "Analytics", icon: BarChart3 },
  { id: "genai_concepts", label: "GenAI Concepts", icon: Sparkles },
  { id: "about", label: "About Project", icon: Info },
];

export default function MainLayout({ activePage, setActivePage, children }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [aiStatus, setAiStatus] = useState({ live_mode: false, model: "Checking..." });

  useEffect(() => {
    checkHealth()
      .then((data) => {
        if (data && data.ai_engine) {
          setAiStatus(data.ai_engine);
        }
      })
      .catch(() => {
        setAiStatus({ live_mode: false, model: "Local RAG Mode" });
      });
  }, []);

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
      {/* Sidebar Desktop */}
      <aside className="hidden md:flex flex-col w-64 bg-slate-900 border-r border-slate-800 text-slate-300 select-none">
        {/* App Brand Header */}
        <div className="h-16 flex items-center px-5 border-b border-slate-800 gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-violet-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30">
            <GraduationCap className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-white tracking-tight flex items-center gap-1.5">
              UniMate <span className="text-[10px] uppercase font-semibold tracking-wider px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">AI</span>
            </h1>
            <p className="text-xs text-slate-400">University Assistant</p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActivePage(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-slate-400"}`} />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded ${
                    isActive ? "bg-white/20 text-white" : "bg-indigo-500/20 text-indigo-300"
                  }`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* AI Engine Status Card */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/60">
          <div className="rounded-lg bg-slate-900 border border-slate-800 p-3 text-xs">
            <div className="flex items-center justify-between mb-1.5">
              <span className="font-semibold text-slate-300 flex items-center gap-1.5 uppercase tracking-wider text-[10px]">
                <Cpu className="w-3.5 h-3.5 text-indigo-400" /> AI ENGINE
              </span>
              <span className={`flex items-center gap-1 text-[10px] font-medium px-1.5 py-0.5 rounded-full ${
                aiStatus.live_mode 
                  ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" 
                  : "bg-blue-500/10 text-blue-400 border border-blue-500/20"
              }`}>
                <span className={`w-1.5 h-1.5 rounded-full ${aiStatus.live_mode ? "bg-emerald-400 animate-pulse" : "bg-blue-400"}`}></span>
                {aiStatus.live_mode ? "Gemini Live" : "Local RAG"}
              </span>
            </div>
            <p className="text-slate-400 text-[11px]">
              Sentence Transformers + ChromaDB
            </p>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top Navbar */}
        <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-4 sm:px-6 z-10">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-slate-800 capitalize">
                {navItems.find((n) => n.id === activePage)?.label || "Dashboard"}
              </h2>
              <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200 hidden sm:inline-block">
                University Academic Portal
              </span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-50 border border-indigo-100 text-xs text-indigo-700 font-medium">
              <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
              <span>Generative AI & RAG Engine</span>
            </div>
          </div>
        </header>

        {/* Mobile Dropdown Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-slate-900 border-b border-slate-800 px-4 py-3 space-y-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  setActivePage(item.id);
                  setMobileMenuOpen(false);
                }}
                className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm ${
                  activePage === item.id ? "bg-indigo-600 text-white" : "text-slate-300 hover:bg-slate-800"
                }`}
              >
                <item.icon className="w-4 h-4" />
                <span>{item.label}</span>
              </button>
            ))}
          </div>
        )}

        {/* Page Body Viewport */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
