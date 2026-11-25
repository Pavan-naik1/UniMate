import React, { useState, useEffect, useRef } from "react";
import {
  Send,
  Plus,
  Trash2,
  FileText,
  Sparkles,
  Bot,
  User,
  Copy,
  Check,
  ChevronDown,
  Layers,
  BookOpen,
  AlertCircle
} from "lucide-react";
import {
  getConversations,
  createConversation,
  getMessages,
  sendChatMessage,
  clearChatMessages,
  getDocuments
} from "../services/api";

const EXAMPLE_PROMPTS = [
  "What is Generative AI and how does it differ from traditional programming?",
  "What is the minimum attendance requirement according to university regulations?",
  "What are the mandatory rules regarding hall tickets and examination conduct?",
  "Explain the CS-401 course modules and grading evaluation scheme.",
  "What is Retrieval-Augmented Generation (RAG) and what are its benefits?"
];

export default function Chatbot() {
  const [conversations, setConversations] = useState([]);
  const [currentConvId, setCurrentConvId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [documents, setDocuments] = useState([]);
  const [selectedDocId, setSelectedDocId] = useState("all");
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const messagesEndRef = useRef(null);

  // Load documents and conversations on mount
  useEffect(() => {
    getDocuments().then(setDocuments).catch(console.error);
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const convs = await getConversations();
      setConversations(convs || []);
      if (convs && convs.length > 0) {
        selectConversation(convs[0].id);
      } else {
        handleNewChat();
      }
    } catch (err) {
      console.error("Failed to load conversations:", err);
    }
  };

  const selectConversation = async (convId) => {
    setCurrentConvId(convId);
    try {
      const msgs = await getMessages(convId);
      setMessages(msgs || []);
    } catch (err) {
      console.error("Failed to fetch messages:", err);
    }
  };

  const handleNewChat = async () => {
    try {
      const newConv = await createConversation("Academic Study Session");
      setConversations((prev) => [newConv, ...prev]);
      setCurrentConvId(newConv.id);
      setMessages([]);
    } catch (err) {
      console.error("Failed to create conversation:", err);
    }
  };

  const handleClearChat = async () => {
    if (!currentConvId) return;
    try {
      await clearChatMessages(currentConvId);
      setMessages([]);
    } catch (err) {
      console.error("Failed to clear chat:", err);
    }
  };

  const handleSendMessage = async (textToSend = null) => {
    const text = textToSend || inputMessage;
    if (!text.trim() || loading) return;

    const userMsg = {
      id: "temp_user_" + Date.now(),
      sender: "user",
      content: text,
      created_at: new Date().toISOString()
    };
    setMessages((prev) => [...prev, userMsg]);
    setInputMessage("");
    setLoading(true);

    try {
      const res = await sendChatMessage(text, currentConvId, selectedDocId === "all" ? null : selectedDocId);
      const assistantMsg = {
        id: res.message_id || "temp_ai_" + Date.now(),
        sender: "assistant",
        content: res.answer,
        sources: res.sources || [],
        model_used: res.engine || "Gemini RAG",
        created_at: new Date().toISOString()
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      const errorMsg = {
        id: "err_" + Date.now(),
        sender: "assistant",
        content: `Error: ${err.message || "Could not retrieve response from AI service."}`,
        sources: [],
        model_used: "System Error"
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="h-[calc(100vh-8rem)] flex gap-4 max-w-7xl mx-auto">
      {/* Sidebar: Conversation history */}
      <div className="hidden lg:flex flex-col w-64 bg-white rounded-xl border border-slate-200 shadow-sm p-3">
        <button
          onClick={handleNewChat}
          className="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-lg bg-indigo-600 text-white font-medium text-xs hover:bg-indigo-700 transition shadow-sm mb-3"
        >
          <Plus className="w-4 h-4" /> New Conversation
        </button>

        <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-2 mb-2">
          Chat History
        </div>

        <div className="flex-1 overflow-y-auto space-y-1">
          {conversations.map((c) => (
            <button
              key={c.id}
              onClick={() => selectConversation(c.id)}
              className={`w-full text-left px-2.5 py-2 rounded-lg text-xs font-medium truncate transition ${
                currentConvId === c.id
                  ? "bg-indigo-50 text-indigo-700 border border-indigo-100"
                  : "text-slate-600 hover:bg-slate-50"
              }`}
            >
              {c.title}
            </button>
          ))}
          {conversations.length === 0 && (
            <p className="text-center text-xs text-slate-400 py-4">No conversations yet</p>
          )}
        </div>
      </div>

      {/* Main Chat Interface */}
      <div className="flex-1 flex flex-col bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        {/* Chat Control Header */}
        <div className="p-3.5 border-b border-slate-200 bg-slate-50 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 text-xs text-slate-600 font-medium">
              <Layers className="w-4 h-4 text-indigo-600" />
              <span>Query Scope:</span>
            </div>
            <select
              value={selectedDocId}
              onChange={(e) => setSelectedDocId(e.target.value)}
              className="text-xs bg-white border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-700 font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="all">All Uploaded Documents (Global RAG)</option>
              {documents.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.original_name}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleClearChat}
              title="Clear messages"
              className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition text-xs flex items-center gap-1"
            >
              <Trash2 className="w-3.5 h-3.5" /> Clear Chat
            </button>
          </div>
        </div>

        {/* Message Stream */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center max-w-xl mx-auto py-8">
              <div className="w-14 h-14 rounded-2xl bg-indigo-50 flex items-center justify-center text-indigo-600 mb-4 shadow-inner">
                <Bot className="w-8 h-8" />
              </div>
              <h3 className="font-bold text-lg text-slate-800">
                UniMate RAG Academic Chatbot
              </h3>
              <p className="text-xs text-slate-500 mt-1 mb-6 max-w-md">
                Ask any question regarding your university notes, regulations, syllabus, or exam policies. 
                Answers are grounded in your indexed documents and cite exact page references.
              </p>

              <div className="w-full space-y-2">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2">
                  Try asking an example question:
                </span>
                {EXAMPLE_PROMPTS.map((prompt, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(prompt)}
                    className="w-full text-left p-2.5 rounded-lg border border-slate-200 bg-slate-50/60 hover:bg-indigo-50/50 hover:border-indigo-200 text-xs text-slate-700 transition flex items-center justify-between"
                  >
                    <span>{prompt}</span>
                    <Sparkles className="w-3.5 h-3.5 text-indigo-500 flex-shrink-0" />
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex gap-3 max-w-3xl ${
                  msg.sender === "user" ? "ml-auto justify-end" : "mr-auto justify-start"
                }`}
              >
                {msg.sender === "assistant" && (
                  <div className="w-8 h-8 rounded-lg bg-indigo-600 text-white flex items-center justify-center flex-shrink-0 text-xs shadow-md shadow-indigo-600/20">
                    <Bot className="w-4 h-4" />
                  </div>
                )}

                <div
                  className={`rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                    msg.sender === "user"
                      ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/10 rounded-br-none"
                      : "bg-slate-50 border border-slate-200 text-slate-800 rounded-bl-none shadow-sm"
                  }`}
                >
                  {/* Message content */}
                  <div className="whitespace-pre-wrap">{msg.content}</div>

                  {/* Assistant Source Citations (Module 1 & 3 Requirement) */}
                  {msg.sender === "assistant" && msg.sources && msg.sources.length > 0 && (
                    <div className="mt-4 pt-3 border-t border-slate-200/80">
                      <div className="flex items-center gap-1.5 text-[11px] font-bold text-indigo-700 mb-2">
                        <BookOpen className="w-3.5 h-3.5" />
                        <span>Retrieved Document Citations ({msg.sources.length})</span>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {msg.sources.map((src, idx) => (
                          <div
                            key={idx}
                            className="p-2 rounded-lg bg-white border border-slate-200 text-slate-700 text-[11px]"
                          >
                            <div className="flex items-center justify-between font-semibold text-slate-800">
                              <span className="truncate max-w-[160px]">{src.document_name}</span>
                              <span className="px-1.5 py-0.5 rounded bg-indigo-50 text-indigo-600 text-[10px] font-bold">
                                Page {src.page_number}
                              </span>
                            </div>
                            {src.excerpt && (
                              <p className="mt-1 text-[10px] text-slate-500 line-clamp-2 italic">
                                "{src.excerpt}"
                              </p>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Footer toolbar */}
                  {msg.sender === "assistant" && (
                    <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-200/60">
                      <span className="flex items-center gap-1">
                        <Sparkles className="w-3 h-3 text-indigo-500" />
                        {msg.model_used || "RAG Engine"}
                      </span>
                      <button
                        onClick={() => copyToClipboard(msg.content, msg.id)}
                        className="flex items-center gap-1 hover:text-slate-600 transition"
                      >
                        {copiedId === msg.id ? (
                          <>
                            <Check className="w-3 h-3 text-emerald-600" /> Copied
                          </>
                        ) : (
                          <>
                            <Copy className="w-3 h-3" /> Copy Answer
                          </>
                        )}
                      </button>
                    </div>
                  )}
                </div>

                {msg.sender === "user" && (
                  <div className="w-8 h-8 rounded-lg bg-slate-800 text-white flex items-center justify-center flex-shrink-0 text-xs">
                    <User className="w-4 h-4" />
                  </div>
                )}
              </div>
            ))
          )}

          {/* Loading Indicator */}
          {loading && (
            <div className="flex gap-3 max-w-xl mr-auto">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 text-white flex items-center justify-center text-xs animate-pulse">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 text-xs text-slate-500 flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-indigo-600 animate-ping"></div>
                <span>Retrieving document passages from ChromaDB & generating answer...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Chat Input Bar */}
        <div className="p-3 sm:p-4 border-t border-slate-200 bg-white">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center gap-2"
          >
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask a question about syllabus, regulations, or study notes..."
              className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs sm:text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !inputMessage.trim()}
              className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold text-xs sm:text-sm transition flex items-center gap-1.5 shadow-md shadow-indigo-600/20"
            >
              <Send className="w-4 h-4" />
              <span className="hidden sm:inline">Ask AI</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
