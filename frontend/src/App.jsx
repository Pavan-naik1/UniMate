import React, { useState } from "react";
import MainLayout from "./layouts/MainLayout";
import Dashboard from "./pages/Dashboard";
import Chatbot from "./pages/Chatbot";
import Documents from "./pages/Documents";
import Summarizer from "./pages/Summarizer";
import QuizGenerator from "./pages/QuizGenerator";
import StudyPlanner from "./pages/StudyPlanner";
import Analytics from "./pages/Analytics";
import GenAIConcepts from "./pages/GenAIConcepts";
import AboutProject from "./pages/AboutProject";

export default function App() {
  const getInitialPage = () => {
    if (typeof window !== "undefined") {
      const urlParams = new URLSearchParams(window.location.search);
      const pageParam = urlParams.get("page");
      if (pageParam) return pageParam;
      const hash = window.location.hash.replace("#", "");
      if (hash) return hash;
    }
    return "dashboard";
  };

  const [activePage, setActivePage] = useState(getInitialPage);

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return <Dashboard setActivePage={setActivePage} />;
      case "chat":
        return <Chatbot />;
      case "documents":
        return <Documents setActivePage={setActivePage} />;
      case "summarizer":
        return <Summarizer />;
      case "quiz":
        return <QuizGenerator />;
      case "study_planner":
        return <StudyPlanner />;
      case "analytics":
        return <Analytics />;
      case "genai_concepts":
        return <GenAIConcepts />;
      case "about":
        return <AboutProject />;
      default:
        return <Dashboard setActivePage={setActivePage} />;
    }
  };

  return (
    <MainLayout activePage={activePage} setActivePage={setActivePage}>
      {renderPage()}
    </MainLayout>
  );
}
