import React, { useState, useEffect } from "react";
import {
  FileSpreadsheet,
  FileText,
  Copy,
  Check,
  Sparkles,
  BookOpen,
  Layers,
  ArrowRight
} from "lucide-react";
import { getDocuments, generateSummary } from "../services/api";

const SUMMARY_TYPES = [
  { id: "detailed", label: "Detailed Summary", desc: "Comprehensive syllabus and conceptual breakdown" },
  { id: "short", label: "Executive Short Summary", desc: "High-level overview under 200 words" },
  { id: "key_points", label: "Important Points", desc: "Bulleted high-yield academic concepts" },
  { id: "definitions", label: "Key Definitions", desc: "Core terminology, formulas, and vocabulary" },
  { id: "exam_topics", label: "Exam-Oriented Topics", desc: "High-probability university examination questions" },
  { id: "exam_notes", label: "Rapid Revision Notes", desc: "Last-minute study sheet for revision" },
  { id: "simple_language", label: "Simple Language Explanations", desc: "Intuitive analogies for difficult theories" },
];

export default function Summarizer() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocId, setSelectedDocId] = useState("");
  const [customText, setCustomText] = useState("");
  const [summaryType, setSummaryType] = useState("detailed");
  const [length, setLength] = useState("medium");
  const [summaryResult, setSummaryResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getDocuments()
      .then((docs) => {
        setDocuments(docs || []);
        if (docs && docs.length > 0) {
          setSelectedDocId(docs[0].id);
        }
      })
      .catch(console.error);
  }, []);

  const handleSummarize = async () => {
    setLoading(true);
    setError("");
    setSummaryResult(null);

    try {
      const res = await generateSummary({
        documentId: selectedDocId || null,
        customText: selectedDocId ? null : customText,
        summaryType,
        length,
      });
      setSummaryResult(res);
    } catch (err) {
      setError(err.message || "Failed to generate summary.");
    } finally {
      setLoading(false);
    }
  };

  const copyText = () => {
    if (!summaryResult?.summary) return;
    navigator.clipboard.writeText(summaryResult.summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-xl sm:text-2xl font-bold text-slate-800">
          AI Notes Summarizer & Exam Prep
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Synthesize long university textbooks, PDFs, and notes into structured study sheets and rapid revision notes using Gemini.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Form Controls */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
              <FileText className="w-4 h-4 text-indigo-600" /> Source Selection
            </h3>

            {/* Document Select */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Select Uploaded Document:
              </label>
              <select
                value={selectedDocId}
                onChange={(e) => {
                  setSelectedDocId(e.target.value);
                  if (e.target.value) setCustomText("");
                }}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">-- Or enter custom text below --</option>
                {documents.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.original_name} ({d.page_count} pgs)
                  </option>
                ))}
              </select>
            </div>

            {/* Or custom text */}
            {!selectedDocId && (
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  Or Paste Lecture Text / Notes:
                </label>
                <textarea
                  value={customText}
                  onChange={(e) => setCustomText(e.target.value)}
                  placeholder="Paste lecture excerpts, paragraphs, or textbook text here..."
                  rows={4}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                />
              </div>
            )}

            {/* Summary Format Types */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-2">
                Summary Type:
              </label>
              <div className="space-y-1.5 max-h-52 overflow-y-auto pr-1">
                {SUMMARY_TYPES.map((t) => (
                  <label
                    key={t.id}
                    className={`flex items-start gap-2.5 p-2 rounded-lg border cursor-pointer transition ${
                      summaryType === t.id
                        ? "bg-indigo-50/70 border-indigo-300 text-indigo-900"
                        : "bg-slate-50/60 border-slate-200 text-slate-700 hover:bg-slate-100"
                    }`}
                  >
                    <input
                      type="radio"
                      name="summaryType"
                      value={t.id}
                      checked={summaryType === t.id}
                      onChange={(e) => setSummaryType(e.target.value)}
                      className="mt-0.5 text-indigo-600 focus:ring-indigo-500"
                    />
                    <div>
                      <span className="text-xs font-semibold block">{t.label}</span>
                      <span className="text-[11px] text-slate-500 block leading-tight">{t.desc}</span>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            {/* Target Length */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Output Length:
              </label>
              <div className="grid grid-cols-3 gap-2">
                {["short", "medium", "comprehensive"].map((len) => (
                  <button
                    key={len}
                    type="button"
                    onClick={() => setLength(len)}
                    className={`py-1.5 px-2 rounded-lg text-xs capitalize font-medium border transition ${
                      length === len
                        ? "bg-indigo-600 text-white border-indigo-600 shadow-sm"
                        : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                    }`}
                  >
                    {len}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={handleSummarize}
              disabled={loading || (!selectedDocId && !customText.trim())}
              className="w-full py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs sm:text-sm transition flex items-center justify-center gap-2 shadow-md shadow-indigo-600/20"
            >
              <Sparkles className="w-4 h-4" />
              <span>{loading ? "Synthesizing Summary..." : "Generate AI Summary"}</span>
            </button>
          </div>
        </div>

        {/* Right Column: Generated Summary Output */}
        <div className="lg:col-span-7">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 min-h-[460px] flex flex-col">
            <div className="flex items-center justify-between pb-4 border-b border-slate-200 mb-4">
              <div>
                <h3 className="font-bold text-slate-800 text-base">Generated Study Notes</h3>
                <p className="text-xs text-slate-500">
                  {summaryResult ? `Source: ${summaryResult.source} • Engine: ${summaryResult.engine}` : "Awaiting input..."}
                </p>
              </div>

              {summaryResult && (
                <button
                  onClick={copyText}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-xs font-medium text-slate-700 transition"
                >
                  {copied ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-600" /> Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5" /> Copy Notes
                    </>
                  )}
                </button>
              )}
            </div>

            {loading ? (
              <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
                <div className="w-10 h-10 rounded-full border-4 border-indigo-200 border-t-indigo-600 animate-spin mb-4"></div>
                <p className="text-sm font-semibold text-slate-700">Synthesizing University Materials</p>
                <p className="text-xs text-slate-400 mt-1">Extracting core definitions and formulating examination notes...</p>
              </div>
            ) : error ? (
              <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs">
                {error}
              </div>
            ) : summaryResult ? (
              <div className="prose prose-sm max-w-none text-slate-800 text-xs sm:text-sm leading-relaxed whitespace-pre-wrap flex-1 overflow-y-auto">
                {summaryResult.summary}
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center text-slate-400 py-12">
                <BookOpen className="w-12 h-12 text-slate-200 mb-3" />
                <h4 className="font-semibold text-sm text-slate-600">No Summary Generated Yet</h4>
                <p className="text-xs max-w-xs text-slate-400 mt-1">
                  Choose a document or paste lecture notes from the left panel and click "Generate AI Summary".
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
