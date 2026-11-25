import React, { useState, useEffect } from "react";
import {
  CalendarCheck2,
  Clock,
  BookOpen,
  CheckCircle2,
  Sparkles,
  Calendar,
  AlertCircle,
  Coffee,
  ListTodo,
  TrendingUp
} from "lucide-react";
import { generateStudyPlan, getStudyPlans, getPlanTopics, toggleTopicCompleted } from "../services/api";

export default function StudyPlanner() {
  const [subject, setSubject] = useState("Generative AI & LLMs (CS-401)");
  const [topicsInput, setTopicsInput] = useState(
    "Transformer Architecture, Self-Attention Mechanisms, Text Embeddings, ChromaDB Vector Stores, RAG Pipeline, Prompt Tuning"
  );
  const [dailyHours, setDailyHours] = useState(3.0);
  const [examDate, setExamDate] = useState("2026-12-15");
  const [difficulty, setDifficulty] = useState("Medium");
  const [activePlan, setActivePlan] = useState(null);
  const [topicsStatus, setTopicsStatus] = useState([]);
  const [pastPlans, setPastPlans] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadExistingPlans();
  }, []);

  const loadExistingPlans = async () => {
    try {
      const plans = await getStudyPlans();
      setPastPlans(plans || []);
      if (plans && plans.length > 0) {
        selectPlan(plans[0]);
      }
    } catch (err) {
      console.error("Failed to load study plans:", err);
    }
  };

  const selectPlan = async (plan) => {
    setActivePlan(plan);
    try {
      const topics = await getPlanTopics(plan.id);
      setTopicsStatus(topics || []);
    } catch (err) {
      console.error("Failed to fetch plan topics:", err);
    }
  };

  const handleGenerate = async (e) => {
    e.preventDefault();
    if (!subject.trim() || !topicsInput.trim()) return;

    setLoading(true);
    setError("");

    try {
      const res = await generateStudyPlan({
        subject,
        topics: topicsInput,
        dailyHours,
        examDate,
        difficulty,
      });
      loadExistingPlans();
    } catch (err) {
      setError(err.message || "Failed to generate study plan.");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTopic = async (topicId, currentVal) => {
    try {
      await toggleTopicCompleted(topicId, !currentVal);
      setTopicsStatus((prev) =>
        prev.map((t) => (t.id === topicId ? { ...t, completed: !currentVal ? 1 : 0 } : t))
      );
    } catch (err) {
      console.error("Failed to toggle topic:", err);
    }
  };

  const completedCount = topicsStatus.filter((t) => t.completed === 1).length;
  const totalCount = topicsStatus.length;
  const progressPercent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-xl sm:text-2xl font-bold text-slate-800">
          Personalized AI Study Planner
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Auto-generate structured daily revision schedules, study blocks, and break recommendations aligned to your exam timeline.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Form: Plan Configuration */}
        <div className="lg:col-span-4 space-y-4">
          <form onSubmit={handleGenerate} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="font-bold text-slate-800 text-sm flex items-center gap-2">
              <CalendarCheck2 className="w-4 h-4 text-indigo-600" /> Plan Parameters
            </h3>

            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                University Subject Name:
              </label>
              <input
                type="text"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="e.g. Distributed Operating Systems"
                className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Topics to Master (Comma-separated):
              </label>
              <textarea
                value={topicsInput}
                onChange={(e) => setTopicsInput(e.target.value)}
                rows={3}
                placeholder="Topic A, Topic B, Topic C..."
                className="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  Daily Study Hours:
                </label>
                <input
                  type="number"
                  step="0.5"
                  min="1"
                  max="12"
                  value={dailyHours}
                  onChange={(e) => setDailyHours(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">
                  Examination Date:
                </label>
                <input
                  type="date"
                  value={examDate}
                  onChange={(e) => setExamDate(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Subject Difficulty:
              </label>
              <div className="grid grid-cols-3 gap-2">
                {["Easy", "Medium", "Hard"].map((d) => (
                  <button
                    key={d}
                    type="button"
                    onClick={() => setDifficulty(d)}
                    className={`py-1.5 rounded-lg text-xs font-semibold border transition ${
                      difficulty === d
                        ? "bg-indigo-600 text-white border-indigo-600"
                        : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"
                    }`}
                  >
                    {d}
                  </button>
                ))}
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs sm:text-sm transition flex items-center justify-center gap-2 shadow-md shadow-indigo-600/20"
            >
              <Sparkles className="w-4 h-4" />
              <span>{loading ? "Constructing Timetable..." : "Generate AI Timetable"}</span>
            </button>
          </form>

          {/* Past Plans List */}
          {pastPlans.length > 0 && (
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <h4 className="font-bold text-slate-800 text-xs mb-2">Saved Study Plans</h4>
              <div className="space-y-1.5 max-h-40 overflow-y-auto">
                {pastPlans.map((p) => (
                  <button
                    key={p.id}
                    onClick={() => selectPlan(p)}
                    className={`w-full text-left p-2 rounded-lg text-xs font-medium truncate transition ${
                      activePlan?.id === p.id
                        ? "bg-indigo-50 text-indigo-700 border border-indigo-200"
                        : "text-slate-600 hover:bg-slate-50"
                    }`}
                  >
                    {p.subject} ({p.schedule?.length || 0} Days)
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Content: Schedule View & Progress Tracker */}
        <div className="lg:col-span-8 space-y-4">
          {activePlan ? (
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-6">
              {/* Plan Header & Progress Bar */}
              <div className="pb-4 border-b border-slate-200">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div>
                    <h3 className="font-bold text-slate-900 text-lg">{activePlan.subject}</h3>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Target Exam: <span className="font-semibold text-slate-700">{activePlan.exam_date}</span> • Daily Target: {activePlan.daily_hours} hrs/day
                    </p>
                  </div>
                  <div className="flex items-center gap-3 bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-200">
                    <TrendingUp className="w-4 h-4 text-emerald-600" />
                    <span className="text-xs font-bold text-slate-800">
                      {progressPercent}% Complete ({completedCount}/{totalCount} Topics)
                    </span>
                  </div>
                </div>

                {/* Progress bar */}
                <div className="w-full bg-slate-100 rounded-full h-2 mt-4 overflow-hidden">
                  <div
                    className="bg-emerald-500 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${progressPercent}%` }}
                  ></div>
                </div>
              </div>

              {/* Day-by-Day Timetable Schedule */}
              <div className="space-y-4">
                {activePlan.schedule?.map((dayPlan, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="px-2.5 py-1 rounded-lg bg-indigo-600 text-white font-bold text-xs">
                          {dayPlan.date_label || `Day ${dayPlan.day}`}
                        </span>
                        <h4 className="font-bold text-slate-900 text-sm">{dayPlan.focus_area}</h4>
                      </div>
                      <span className="text-xs text-slate-500 flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-indigo-500" /> {dayPlan.allocated_hours} Hours Allocated
                      </span>
                    </div>

                    {/* Sessions breakdown */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                      {dayPlan.sessions?.map((session, sIdx) => (
                        <div key={sIdx} className="p-2.5 rounded-lg bg-white border border-slate-200/80 text-xs">
                          <span className="font-semibold text-indigo-700 block text-[11px]">{session.time}</span>
                          <span className="text-slate-700 mt-0.5 block">{session.activity}</span>
                        </div>
                      ))}
                    </div>

                    {/* Topics Checklist for this Day */}
                    {dayPlan.topics && (
                      <div className="pt-2 border-t border-slate-200/60">
                        <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-1.5">
                          Topics for this Session:
                        </span>
                        <div className="flex flex-wrap gap-2">
                          {dayPlan.topics.map((tName, tIdx) => {
                            const matchingTopicObj = topicsStatus.find((ts) => ts.topic_name === tName && ts.day === dayPlan.day) ||
                              topicsStatus.find((ts) => ts.topic_name === tName);
                            const isDone = matchingTopicObj?.completed === 1;

                            return (
                              <button
                                key={tIdx}
                                type="button"
                                onClick={() => matchingTopicObj && handleToggleTopic(matchingTopicObj.id, isDone)}
                                className={`px-3 py-1 rounded-lg text-xs font-medium border flex items-center gap-1.5 transition ${
                                  isDone
                                    ? "bg-emerald-50 border-emerald-300 text-emerald-800 line-through"
                                    : "bg-white border-slate-200 text-slate-700 hover:border-indigo-300"
                                }`}
                              >
                                <CheckCircle2 className={`w-3.5 h-3.5 ${isDone ? "text-emerald-600" : "text-slate-300"}`} />
                                <span>{tName}</span>
                              </button>
                            );
                          })}
                        </div>
                      </div>
                    )}

                    {/* Revision tips */}
                    {dayPlan.revision_tips && (
                      <div className="p-2 rounded-lg bg-amber-50/70 border border-amber-200/60 text-[11px] text-amber-900 flex items-start gap-1.5">
                        <Coffee className="w-3.5 h-3.5 text-amber-600 flex-shrink-0 mt-0.5" />
                        <span><strong>Revision Tip:</strong> {dayPlan.revision_tips}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-12 text-center text-slate-400">
              <CalendarCheck2 className="w-12 h-12 text-slate-200 mx-auto mb-3" />
              <h4 className="font-semibold text-sm text-slate-600">No Active Study Timetable</h4>
              <p className="text-xs max-w-xs mx-auto text-slate-400 mt-1">
                Enter your subject topics and target exam date in the form on the left to generate an AI study timetable.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
