// UniMate Client API Service
// Automatically detects host/port to guarantee seamless communication without IPv6/CORS mismatch

function getApiBase() {
  if (typeof window !== "undefined") {
    // If running on port 8000 (FastAPI static frontend) or Vite dev server with proxy, relative "/api" works seamlessly
    if (window.location.port === "8000" || window.location.port === "5173") {
      return "/api";
    }
    // Match current host (127.0.0.1 or localhost) to prevent cross-origin loopback resolution issues
    const host = window.location.hostname || "127.0.0.1";
    return `http://${host}:8000/api`;
  }
  return "http://127.0.0.1:8000/api";
}

const API_BASE = getApiBase();

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

// Chat API
export async function getConversations() {
  const res = await fetch(`${API_BASE}/chat/conversations`);
  return res.json();
}

export async function createConversation(title = "Academic Study Session") {
  const res = await fetch(`${API_BASE}/chat/conversations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  return res.json();
}

export async function getMessages(convId) {
  const res = await fetch(`${API_BASE}/chat/messages/${convId}`);
  return res.json();
}

export async function sendChatMessage(message, conversationId = null, documentId = null) {
  const res = await fetch(`${API_BASE}/chat/message`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
      document_id: documentId,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || "Failed to send message");
  }
  return res.json();
}

export async function clearChatMessages(convId) {
  const res = await fetch(`${API_BASE}/chat/clear/${convId}`, {
    method: "POST",
  });
  return res.json();
}

// Documents API
export async function getDocuments() {
  const res = await fetch(`${API_BASE}/documents/list`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `HTTP ${res.status}: Failed to fetch documents` }));
    throw new Error(err.detail || "Failed to fetch documents");
  }
  return res.json();
}

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE}/documents/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `Upload failed (HTTP ${res.status})` }));
    throw new Error(err.detail || "Failed to upload document");
  }
  return res.json();
}

export async function uploadMultipleDocuments(files) {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append("files", files[i]);
  }
  const res = await fetch(`${API_BASE}/documents/upload-multiple`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: `Upload failed (HTTP ${res.status})` }));
    throw new Error(err.detail || "Failed to upload documents");
  }
  return res.json();
}

export async function deleteDocument(docId) {
  const res = await fetch(`${API_BASE}/documents/${docId}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Delete failed" }));
    throw new Error(err.detail || "Failed to delete document");
  }
  return res.json();
}

// Summarizer API
export async function generateSummary({ documentId, customText, summaryType, length }) {
  const res = await fetch(`${API_BASE}/summarize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      document_id: documentId || null,
      custom_text: customText || null,
      summary_type: summaryType || "detailed",
      length: length || "medium",
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Summarization failed" }));
    throw new Error(err.detail || "Failed to generate summary");
  }
  return res.json();
}

// Quiz API
export async function generateQuiz({ documentId, topic, numQuestions, difficulty }) {
  const res = await fetch(`${API_BASE}/quiz/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      document_id: documentId || null,
      topic: topic || null,
      num_questions: parseInt(numQuestions) || 5,
      difficulty: difficulty || "Medium",
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Quiz generation failed" }));
    throw new Error(err.detail || "Failed to generate quiz");
  }
  return res.json();
}

export async function submitQuiz(quizId, answers) {
  const res = await fetch(`${API_BASE}/quiz/submit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      quiz_id: quizId,
      answers,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Submission failed" }));
    throw new Error(err.detail || "Failed to submit quiz");
  }
  return res.json();
}

export async function getQuizHistory() {
  const res = await fetch(`${API_BASE}/quiz/history`);
  return res.json();
}

// Study Planner API
export async function generateStudyPlan({ subject, topics, dailyHours, examDate, difficulty }) {
  const res = await fetch(`${API_BASE}/study-planner/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      subject,
      topics,
      daily_hours: parseFloat(dailyHours) || 2.5,
      exam_date: examDate,
      difficulty,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Plan generation failed" }));
    throw new Error(err.detail || "Failed to generate study plan");
  }
  return res.json();
}

export async function getStudyPlans() {
  const res = await fetch(`${API_BASE}/study-planner/plans`);
  return res.json();
}

export async function getPlanTopics(planId) {
  const res = await fetch(`${API_BASE}/study-planner/plan/${planId}/topics`);
  return res.json();
}

export async function toggleTopicCompleted(topicId, completed) {
  const res = await fetch(`${API_BASE}/study-planner/topic/${topicId}/toggle`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  return res.json();
}

// Analytics API
export async function getAnalytics() {
  const res = await fetch(`${API_BASE}/analytics/overview`);
  return res.json();
}

// GenAI Concepts API
export async function getGenAIConcepts() {
  const res = await fetch(`${API_BASE}/genai-concepts`);
  return res.json();
}
