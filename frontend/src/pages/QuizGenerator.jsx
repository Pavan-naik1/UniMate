import React, { useState, useEffect } from "react";
import {
  BrainCircuit,
  CheckCircle2,
  XCircle,
  HelpCircle,
  RotateCcw,
  Sparkles,
  Trophy,
  History,
  FileText
} from "lucide-react";
import { getDocuments, generateQuiz, submitQuiz, getQuizHistory } from "../services/api";

export default function QuizGenerator() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocId, setSelectedDocId] = useState("");
  const [topic, setTopic] = useState("");
  const [numQuestions, setNumQuestions] = useState(5);
  const [difficulty, setDifficulty] = useState("Medium");
  const [quizData, setQuizData] = useState(null);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [submissionResult, setSubmissionResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    getDocuments().then(setDocuments).catch(console.error);
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await getQuizHistory();
      setHistory(data || []);
    } catch (err) {
      console.error("Failed to load quiz history:", err);
    }
  };

  const handleGenerate = async () => {
    setLoading(true);
    setError("");
    setQuizData(null);
    setSubmissionResult(null);
    setSelectedAnswers({});

    try {
      const res = await generateQuiz({
        documentId: selectedDocId || null,
        topic: topic || null,
        numQuestions,
        difficulty,
      });
      setQuizData(res);
    } catch (err) {
      setError(err.message || "Failed to generate quiz.");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (qIdx, optIdx) => {
    if (submissionResult) return; // Locked after submission
    setSelectedAnswers((prev) => ({
      ...prev,
      [qIdx]: optIdx,
    }));
  };

  const handleSubmit = async () => {
    if (!quizData) return;
    const answersList = [];
    for (let i = 0; i < quizData.questions.length; i++) {
      answersList.push(selectedAnswers[i] !== undefined ? selectedAnswers[i] : -1);
    }

    setSubmitting(true);
    try {
      const res = await submitQuiz(quizData.quiz_id, answersList);
      setSubmissionResult(res);
      loadHistory();
    } catch (err) {
      setError("Failed to evaluate quiz.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div>
        <h1 className="text-xl sm:text-2xl font-bold text-slate-800">
          AI Examination Quiz Generator
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Generate realistic university-standard practice questions from your uploaded syllabi or custom subjects. Test your knowledge with immediate feedback.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Config Panel */}
        <div className="lg:col-span-4 space-y-4">
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
              <BrainCircuit className="w-4 h-4 text-indigo-600" /> Quiz Configuration
            </h3>

            {/* Document Select */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Select Base Document:
              </label>
              <select
                value={selectedDocId}
                onChange={(e) => {
                  setSelectedDocId(e.target.value);
                  if (e.target.value) setTopic("");
                }}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="">-- Or enter custom topic below --</option>
                {documents.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.original_name}
                  </option>
                ))}
              </select>
            </div>

            {/* Or custom topic */}
            {!selectedDocId && (
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  Or Enter Specific Subject/Topic:
                </label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="e.g. Transformer Self-Attention & RAG"
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            )}

            {/* Number of Questions */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Number of Questions:
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[3, 5, 10].map((n) => (
                  <button
                    key={n}
                    type="button"
                    onClick={() => setNumQuestions(n)}
                    className={`py-1.5 rounded-lg text-xs font-semibold border transition ${
                      numQuestions === n
                        ? "bg-indigo-600 text-white border-indigo-600"
                        : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                    }`}
                  >
                    {n} Questions
                  </button>
                ))}
              </div>
            </div>

            {/* Difficulty Level */}
            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Difficulty Level:
              </label>
              <div className="grid grid-cols-3 gap-2">
                {["Easy", "Medium", "Hard"].map((diff) => (
                  <button
                    key={diff}
                    type="button"
                    onClick={() => setDifficulty(diff)}
                    className={`py-1.5 rounded-lg text-xs font-semibold border transition ${
                      difficulty === diff
                        ? "bg-indigo-600 text-white border-indigo-600"
                        : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                    }`}
                  >
                    {diff}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={handleGenerate}
              disabled={loading || (!selectedDocId && !topic.trim())}
              className="w-full py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs sm:text-sm transition flex items-center justify-center gap-2 shadow-md shadow-indigo-600/20"
            >
              <Sparkles className="w-4 h-4" />
              <span>{loading ? "Generating Questions..." : "Create Practice Quiz"}</span>
            </button>
          </div>

          {/* Past Attempts History Card */}
          <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
            <h4 className="font-bold text-slate-800 text-xs flex items-center gap-1.5 mb-2">
              <History className="w-3.5 h-3.5 text-slate-500" /> Past Quiz Attempts
            </h4>
            <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
              {history.map((h) => (
                <div key={h.id} className="p-2 rounded-lg bg-slate-50 border border-slate-100 text-[11px] flex items-center justify-between">
                  <div className="truncate max-w-[150px]">
                    <span className="font-semibold text-slate-800 block truncate">{h.title}</span>
                    <span className="text-slate-400 text-[10px]">{h.difficulty} • {h.total_questions} Qs</span>
                  </div>
                  <span className={`px-2 py-0.5 rounded-full font-bold ${
                    (h.score / h.total_questions) >= 0.7 
                      ? "bg-emerald-50 text-emerald-700" 
                      : "bg-amber-50 text-amber-700"
                  }`}>
                    {h.score}/{h.total_questions} ({Math.round((h.score / h.total_questions) * 100)}%)
                  </span>
                </div>
              ))}
              {history.length === 0 && (
                <p className="text-center text-slate-400 text-xs py-3">No past attempts yet</p>
              )}
            </div>
          </div>
        </div>

        {/* Right Active Quiz Interface */}
        <div className="lg:col-span-8">
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 min-h-[460px] flex flex-col">
            {loading ? (
              <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
                <div className="w-10 h-10 rounded-full border-4 border-indigo-200 border-t-indigo-600 animate-spin mb-4"></div>
                <p className="text-sm font-semibold text-slate-700">Formulating Examination Questions</p>
                <p className="text-xs text-slate-400 mt-1">Extracting syllabus themes and crafting multiple-choice items...</p>
              </div>
            ) : quizData ? (
              <div className="space-y-6 flex-1">
                {/* Quiz Header & Score Banner if submitted */}
                <div className="pb-4 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h3 className="font-bold text-slate-900 text-base">{quizData.title}</h3>
                    <p className="text-xs text-slate-500">
                      Difficulty: <span className="font-semibold text-indigo-600">{quizData.difficulty}</span> • Total Questions: {quizData.total_questions}
                    </p>
                  </div>

                  {submissionResult && (
                    <div className="flex items-center gap-3 bg-indigo-50 border border-indigo-200 px-4 py-2 rounded-xl">
                      <Trophy className="w-6 h-6 text-amber-500" />
                      <div>
                        <span className="text-xs font-semibold text-indigo-900 block">Final Score:</span>
                        <span className="text-base font-extrabold text-indigo-700">
                          {submissionResult.score} / {submissionResult.total_questions} ({submissionResult.percentage}%)
                        </span>
                      </div>
                    </div>
                  )}
                </div>

                {/* Questions List */}
                <div className="space-y-6">
                  {quizData.questions.map((q, qIdx) => {
                    const resultInfo = submissionResult?.results?.[qIdx];
                    const selectedOpt = selectedAnswers[qIdx];

                    return (
                      <div key={qIdx} className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
                        <div className="flex items-start gap-2.5">
                          <span className="w-6 h-6 rounded-full bg-indigo-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0">
                            {qIdx + 1}
                          </span>
                          <h4 className="text-xs sm:text-sm font-semibold text-slate-900 leading-snug">
                            {q.question}
                          </h4>
                        </div>

                        {/* Options */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1 pl-8">
                          {q.options.map((opt, optIdx) => {
                            const isSelected = selectedOpt === optIdx;
                            let optionClass = "border-slate-200 hover:bg-slate-100 text-slate-700 bg-white";

                            if (submissionResult && resultInfo) {
                              const isCorrect = resultInfo.correct_answer === optIdx;
                              const isStudentPick = resultInfo.student_answer === optIdx;

                              if (isCorrect) {
                                optionClass = "border-emerald-500 bg-emerald-50 text-emerald-900 font-semibold";
                              } else if (isStudentPick && !isCorrect) {
                                optionClass = "border-rose-400 bg-rose-50 text-rose-900";
                              }
                            } else if (isSelected) {
                              optionClass = "border-indigo-600 bg-indigo-50 text-indigo-900 font-semibold";
                            }

                            return (
                              <button
                                key={optIdx}
                                type="button"
                                disabled={!!submissionResult}
                                onClick={() => handleSelectOption(qIdx, optIdx)}
                                className={`text-left p-3 rounded-lg border text-xs transition flex items-center justify-between ${optionClass}`}
                              >
                                <span>{opt}</span>
                                {submissionResult && resultInfo?.correct_answer === optIdx && (
                                  <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0 ml-1" />
                                )}
                                {submissionResult && resultInfo?.student_answer === optIdx && resultInfo?.correct_answer !== optIdx && (
                                  <XCircle className="w-4 h-4 text-rose-500 flex-shrink-0 ml-1" />
                                )}
                              </button>
                            );
                          })}
                        </div>

                        {/* Explanation post-submission */}
                        {submissionResult && resultInfo && (
                          <div className="ml-8 mt-2 p-3 rounded-lg bg-indigo-50/70 border border-indigo-100 text-xs text-indigo-950">
                            <span className="font-bold block mb-0.5 flex items-center gap-1 text-indigo-800">
                              <HelpCircle className="w-3.5 h-3.5" /> Explanation:
                            </span>
                            <p className="text-[11px] leading-relaxed text-indigo-900">{resultInfo.explanation}</p>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>

                {/* Submit button */}
                <div className="pt-4 border-t border-slate-200 flex justify-end">
                  {!submissionResult ? (
                    <button
                      onClick={handleSubmit}
                      disabled={submitting || Object.keys(selectedAnswers).length === 0}
                      className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs sm:text-sm transition flex items-center gap-2 shadow-md shadow-indigo-600/20"
                    >
                      <CheckCircle2 className="w-4 h-4" />
                      <span>{submitting ? "Evaluating..." : "Submit Examination Quiz"}</span>
                    </button>
                  ) : (
                    <button
                      onClick={handleGenerate}
                      className="px-6 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs sm:text-sm transition flex items-center gap-2"
                    >
                      <RotateCcw className="w-4 h-4" />
                      <span>Try Another Assessment</span>
                    </button>
                  )}
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center text-slate-400 py-12">
                <BrainCircuit className="w-12 h-12 text-slate-200 mb-3" />
                <h4 className="font-semibold text-sm text-slate-600">No Active Quiz</h4>
                <p className="text-xs max-w-xs text-slate-400 mt-1">
                  Configure your subject and difficulty on the left panel and click "Create Practice Quiz".
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
