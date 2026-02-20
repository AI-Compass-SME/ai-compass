import React from 'react';
import { Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import CompanySnapshot from './pages/CompanySnapshot';
import QuestionnaireWizard from './pages/QuestionnaireWizard';
import ResultsPage from './pages/ResultsPage';
import ImprintPage from './pages/ImprintPage';
import PrivacyPage from './pages/PrivacyPage';
import MethodologyPage from './pages/MethodologyPage';
import AboutPage from './pages/AboutPage';

import ContactPage from './pages/ContactPage';
import HowItWorksPage from './pages/HowItWorksPage';
import ComingSoonPage from './pages/ComingSoonPage';

import { Toaster } from "@/components/ui/sonner"

function App() {
  // Check if we are running locally
  const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

  // If not localhost, show the Coming Soon page and block the rest of the app
  if (!isLocalhost) {
    return <ComingSoonPage />;
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/snapshot" element={<CompanySnapshot />} />
        <Route path="/assessment/:responseId" element={<QuestionnaireWizard />} />
        <Route path="/results/:responseId" element={<ResultsPage />} />
        <Route path="/imprint" element={<ImprintPage />} />
        <Route path="/privacy" element={<PrivacyPage />} />
        <Route path="/methodology" element={<MethodologyPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/how-it-works" element={<HowItWorksPage />} />
      </Routes>
      <Toaster />
    </div>
  );
}

export default App;
