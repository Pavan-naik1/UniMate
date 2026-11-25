import React, { useState, useEffect, useRef } from "react";
import {
  UploadCloud,
  FileText,
  Trash2,
  CheckCircle2,
  AlertCircle,
  Search,
  Layers,
  Sparkles,
  Calendar,
  Clock,
  RefreshCw,
  MessageSquare,
  FileUp,
  Cpu
} from "lucide-react";
import { getDocuments, uploadMultipleDocuments, uploadDocument, deleteDocument } from "../services/api";

export default function Documents({ setActivePage }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    setLoading(true);
    try {
      const data = await getDocuments();
      setDocuments(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to load documents:", err);
      setErrorMsg(
        err.message?.includes("Failed to fetch")
          ? "Could not connect to UniMate API. Please ensure the backend is running at http://127.0.0.1:8000."
          : (err.message || "Failed to load document library.")
      );
    } finally {
      setLoading(false);
    }
  };

  const processFiles = async (filesList) => {
    if (!filesList || filesList.length === 0) return;

    const files = Array.from(filesList);
    const nonPdfs = files.filter((f) => !f.name.toLowerCase().endsWith(".pdf"));
    if (nonPdfs.length > 0) {
      setErrorMsg(`Invalid file type: "${nonPdfs[0].name}". Only PDF documents (.pdf) are supported.`);
      return;
    }

    const overSized = files.filter((f) => f.size > 25 * 1024 * 1024);
    if (overSized.length > 0) {
      setErrorMsg(`File "${overSized[0].name}" exceeds the 25MB maximum size limit.`);
      return;
    }

    const emptyFiles = files.filter((f) => f.size === 0);
    if (emptyFiles.length > 0) {
      setErrorMsg(`File "${emptyFiles[0].name}" is empty (0 bytes). Please select valid PDF documents.`);
      return;
    }

    setUploading(true);
    setErrorMsg("");
    setSuccessMsg("");
    setUploadStatus(
      files.length === 1
        ? `Processing "${files[0].name}": Extracting text with PyMuPDF -> Vectorizing with Sentence-Transformers -> Indexing in ChromaDB...`
        : `Processing ${files.length} documents: Extracting text with PyMuPDF -> Vectorizing with Sentence-Transformers -> Indexing in ChromaDB...`
    );

    try {
      let res;
      if (files.length === 1) {
        res = await uploadDocument(files[0]);
      } else {
        res = await uploadMultipleDocuments(files);
      }

      setSuccessMsg(
        res.message ||
          `Successfully uploaded and indexed ${files.length} document(s) with ${res.chunks_created || 0} semantic chunks!`
      );
      // Automatically refresh document library
      await loadDocuments();
    } catch (err) {
      setErrorMsg(err.message || "Upload and indexing failed. Please verify the PDF is readable.");
    } finally {
      setUploading(false);
      setUploadStatus("");
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleFileInputChange = (e) => {
    processFiles(e.target.files);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer && e.dataTransfer.files) {
      processFiles(e.dataTransfer.files);
    }
  };

  const handleDelete = async (docId, name) => {
    if (!window.confirm(`Are you sure you want to delete "${name}" from ChromaDB and the library?`)) {
      return;
    }
    try {
      await deleteDocument(docId);
      setSuccessMsg(`Deleted "${name}" from indexed library.`);
      await loadDocuments();
    } catch (err) {
      setErrorMsg("Failed to delete document.");
    }
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return "Pre-indexed";
    try {
      const d = new Date(dateStr);
      return (
        d.toLocaleDateString(undefined, {
          year: "numeric",
          month: "short",
          day: "numeric",
        }) +
        " • " +
        d.toLocaleTimeString(undefined, {
          hour: "2-digit",
          minute: "2-digit",
        })
      );
    } catch {
      return dateStr;
    }
  };

  const filteredDocs = documents.filter((d) =>
    (d.original_name || "").toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header with Top Upload Button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-slate-800 flex items-center gap-2">
            <FileText className="w-6 h-6 text-indigo-600" />
            University Document Management
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl">
            Upload syllabi, lecture notes, regulations, and question papers. Extracted text is divided into overlapping chunks and vectorized into 384D dense embeddings for ChromaDB semantic RAG retrieval.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <label className={`cursor-pointer inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-white font-semibold text-xs sm:text-sm transition shadow-md ${
            uploading
              ? "bg-indigo-400 cursor-not-allowed"
              : "bg-indigo-600 hover:bg-indigo-700 shadow-indigo-600/20 active:scale-95"
          }`}>
            <UploadCloud className="w-4 h-4" />
            <span>{uploading ? "Uploading..." : "Upload PDF"}</span>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              multiple
              onChange={handleFileInputChange}
              disabled={uploading}
              className="hidden"
            />
          </label>
        </div>
      </div>

      {/* Notifications */}
      {successMsg && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs sm:text-sm flex items-start justify-between shadow-sm animate-fadeIn">
          <div className="flex items-center gap-2.5">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0" />
            <span className="font-medium">{successMsg}</span>
          </div>
          <button
            onClick={() => setSuccessMsg("")}
            className="text-emerald-700 font-bold hover:underline text-xs ml-4"
          >
            Dismiss
          </button>
        </div>
      )}

      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs sm:text-sm flex items-start justify-between shadow-sm animate-fadeIn">
          <div className="flex items-center gap-2.5">
            <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0" />
            <span className="font-medium">{errorMsg}</span>
          </div>
          <button
            onClick={() => setErrorMsg("")}
            className="text-rose-700 font-bold hover:underline text-xs ml-4"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Upload Drag & Drop Area / Progress Card */}
      {uploading ? (
        <div className="bg-indigo-50/50 rounded-2xl border-2 border-indigo-300 p-8 text-center shadow-inner">
          <div className="max-w-md mx-auto flex flex-col items-center">
            <div className="relative mb-4">
              <div className="w-14 h-14 rounded-2xl bg-indigo-600 flex items-center justify-center text-white shadow-lg shadow-indigo-600/30 animate-bounce">
                <FileUp className="w-7 h-7" />
              </div>
              <span className="absolute -top-1 -right-1 flex h-4 w-4">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-4 w-4 bg-indigo-500"></span>
              </span>
            </div>
            <h3 className="font-bold text-slate-800 text-base">Processing & Indexing Document</h3>
            <p className="text-xs text-indigo-700 font-medium mt-1 mb-4 leading-relaxed max-w-sm">
              {uploadStatus}
            </p>
            <div className="w-full bg-indigo-200/60 rounded-full h-2 overflow-hidden">
              <div className="bg-indigo-600 h-2 rounded-full w-3/4 animate-pulse"></div>
            </div>
            <div className="mt-4 flex items-center justify-center gap-4 text-[11px] text-slate-500">
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> PyMuPDF Parsing
              </span>
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> 384D Embeddings
              </span>
              <span className="flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> ChromaDB Store
              </span>
            </div>
          </div>
        </div>
      ) : (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`rounded-2xl border-2 border-dashed transition p-8 text-center bg-white shadow-sm ${
            isDragging
              ? "border-indigo-600 bg-indigo-50/50 scale-[1.005]"
              : "border-indigo-200 hover:border-indigo-400 hover:bg-slate-50/50"
          }`}
        >
          <div className="max-w-lg mx-auto flex flex-col items-center">
            <div className="w-14 h-14 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-3 shadow-sm border border-indigo-100">
              <UploadCloud className="w-8 h-8" />
            </div>
            <h3 className="font-bold text-slate-800 text-base">
              Drag & Drop University PDFs Here, or Browse
            </h3>
            <p className="text-xs text-slate-500 mt-1 mb-5 leading-relaxed">
              Upload multiple course syllabi, lecture notes, academic regulations, or question papers.
              Files up to 25MB are parsed and indexed for immediate AI Chatbot Q&A.
            </p>
            <label className="cursor-pointer inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs sm:text-sm transition shadow-md shadow-indigo-600/20 active:scale-95">
              <FileUp className="w-4 h-4" />
              <span>Select PDF Files</span>
              <input
                type="file"
                accept=".pdf"
                multiple
                onChange={handleFileInputChange}
                className="hidden"
              />
            </label>
            <p className="text-[11px] text-slate-400 mt-2.5">
              Supports multiple files simultaneously • .pdf format only
            </p>
          </div>
        </div>
      )}

      {/* Documents Library Table View */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        {/* Table Toolbar */}
        <div className="p-4 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/50">
          <div className="flex items-center gap-2.5">
            <h3 className="font-bold text-slate-800 text-sm">Indexed Document Library</h3>
            <span className="px-2.5 py-0.5 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold">
              {documents.length} {documents.length === 1 ? "document" : "documents"}
            </span>
            <button
              onClick={loadDocuments}
              className="p-1 rounded-lg text-slate-400 hover:text-indigo-600 hover:bg-white transition"
              title="Refresh library"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin text-indigo-600" : ""}`} />
            </button>
          </div>

          <div className="relative w-full sm:w-72">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search uploaded documents..."
              className="w-full bg-white border border-slate-200 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
            />
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-100/70 text-slate-600 uppercase text-[10px] tracking-wider border-b border-slate-200 font-bold">
              <tr>
                <th className="py-3 px-4">Document Name</th>
                <th className="py-3 px-4">Upload Date</th>
                <th className="py-3 px-4">Pages</th>
                <th className="py-3 px-4">Semantic Chunks</th>
                <th className="py-3 px-4">Indexing Status</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {filteredDocs.map((doc) => (
                <tr key={doc.id} className="hover:bg-indigo-50/20 transition">
                  {/* Document Name & File Size */}
                  <td className="py-3.5 px-4 font-semibold text-slate-900">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center flex-shrink-0 border border-indigo-100">
                        <FileText className="w-4 h-4" />
                      </div>
                      <div className="min-w-0">
                        <span className="truncate block font-semibold text-slate-900 max-w-xs sm:max-w-sm">
                          {doc.original_name}
                        </span>
                        <span className="text-[11px] text-slate-400 font-normal">
                          {(doc.file_size / 1024).toFixed(1)} KB
                        </span>
                      </div>
                    </div>
                  </td>

                  {/* Upload Date */}
                  <td className="py-3.5 px-4 text-slate-500">
                    <span className="inline-flex items-center gap-1.5 text-[11px]">
                      <Clock className="w-3 h-3 text-slate-400" />
                      {formatDate(doc.upload_date)}
                    </span>
                  </td>

                  {/* Pages */}
                  <td className="py-3.5 px-4 font-medium">
                    <span className="inline-flex items-center gap-1 text-[11px] bg-slate-100 px-2 py-0.5 rounded-md text-slate-700">
                      <FileText className="w-3 h-3 text-slate-500" />
                      {doc.page_count} {doc.page_count === 1 ? "Page" : "Pages"}
                    </span>
                  </td>

                  {/* Semantic Chunks */}
                  <td className="py-3.5 px-4">
                    <span className="inline-flex items-center gap-1 font-semibold text-indigo-700 bg-indigo-50 border border-indigo-100 px-2.5 py-0.5 rounded-full text-[11px]">
                      <Layers className="w-3 h-3 text-indigo-600" />
                      {doc.chunk_count} Chunks
                    </span>
                  </td>

                  {/* Indexing Status */}
                  <td className="py-3.5 px-4">
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                      <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                      Vectorized (ChromaDB)
                    </span>
                  </td>

                  {/* Actions */}
                  <td className="py-3.5 px-4 text-right space-x-2">
                    <button
                      onClick={() => setActivePage("chat")}
                      className="inline-flex items-center gap-1 px-3 py-1 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 font-medium text-[11px] transition shadow-sm"
                      title="Ask questions grounded in this document"
                    >
                      <MessageSquare className="w-3 h-3" />
                      Ask AI
                    </button>
                    <button
                      onClick={() => handleDelete(doc.id, doc.original_name)}
                      className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition"
                      title="Delete document and remove vector embeddings"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}

              {filteredDocs.length === 0 && (
                <tr>
                  <td colSpan="6" className="text-center py-10 text-slate-400">
                    <FileText className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                    <p className="text-sm font-medium text-slate-600">
                      {searchQuery
                        ? `No documents found matching "${searchQuery}".`
                        : "No documents in library yet."}
                    </p>
                    <p className="text-xs text-slate-400 mt-1">
                      Upload a PDF document above to start indexing for AI Chatbot and Summaries.
                    </p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
