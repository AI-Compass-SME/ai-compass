import React, { useState } from 'react';
import { Compass, Download, Loader2, ArrowRight } from 'lucide-react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { api } from '../lib/api';
import { initializeVisitorSession } from '../lib/assessment';
import { toast } from "sonner";
import { useTranslation } from 'react-i18next';

export function Navigation() {
    const { t, i18n } = useTranslation();
    const location = useLocation();
    const showDownload = location.pathname.includes('/results/');
    const showStart = location.pathname === '/';
    const responseId = showDownload ? location.pathname.split('/results/')[1] : null;
    const [isDownloading, setIsDownloading] = useState(false);

    const toggleLanguage = () => {
        const newLang = i18n.language === 'en' ? 'de' : 'en';
        i18n.changeLanguage(newLang);
    };

    const handleDownload = async () => {
        if (!responseId) return;
        try {
            setIsDownloading(true);
            const blob = await api.downloadPDF(responseId, i18n.language);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `ai_maturity_report_${responseId}_${i18n.language}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            toast.success(t('download.toastSuccess', "Report downloaded successfully!"));
        } catch (error) {
            console.error("Download failed", error);
            toast.error(t('download.toastError', "Failed to download report."));
        } finally {
            setIsDownloading(false);
        }
    };

    const navigate = useNavigate();
    const [isStarting, setIsStarting] = useState(false);

    const handleStartAssessment = async () => {
        try {
            setIsStarting(true);
            const session = await initializeVisitorSession(i18n.language);
            toast.success(t('landing.hero.success', "Assessment started!"), { duration: 1000 });
            navigate(`/assessment/${session.responseId}`);
        } catch (error) {
            toast.error(t('landing.hero.error', "Failed to start assessment."));
            console.error(error);
        } finally {
            setIsStarting(false);
        }
    };

    return (
        <nav className="fixed top-0 left-0 right-0 bg-white/90 backdrop-blur-sm z-50 border-b border-gray-200">
            <div className="max-w-[80rem] mx-auto px-6 py-4 flex items-center justify-between">
                <Link to="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
                    <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2 rounded-lg">
                        <Compass className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-xl font-semibold text-gray-900">AI Compass</span>
                </Link>
                <div className="flex items-center gap-3">
                    {showDownload && (
                        <Button
                            size="sm"
                            disabled={isDownloading}
                            className="relative px-6 h-10 text-sm font-semibold rounded-xl transition-colors bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 shadow-sm"
                            onClick={handleDownload}
                        >
                            <span className="flex items-center">
                                {isDownloading ? <Loader2 className="w-4 h-4 mr-2 animate-spin text-slate-400" /> : <Download className="w-4 h-4 mr-2 text-slate-400" />}
                                {isDownloading ? t('nav.generatingPdf', "Generating...") : t('nav.downloadReport', "Download Report")}
                            </span>
                        </Button>
                    )}
                    {showStart && (
                        <Button
                            onClick={handleStartAssessment}
                            disabled={isStarting}
                            size="sm"
                            className="hidden md:inline-flex items-center justify-center relative px-6 h-10 text-sm font-semibold rounded-xl transition-colors bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 shadow-sm"
                        >
                            {isStarting ? (
                                <>
                                    <Loader2 className="w-4 h-4 mr-2 animate-spin text-slate-400" />
                                    {t('nav.starting', "Starting...")}
                                </>
                            ) : (
                                <>
                                    {t('nav.getStarted')}
                                    <ArrowRight className="w-4 h-4 ml-2 text-slate-400" />
                                </>
                            )}
                        </Button>
                    )}

                    <button
                        onClick={toggleLanguage}
                        className="flex items-center justify-between w-[68px] h-8 bg-slate-100 rounded-full p-1 relative cursor-pointer border border-slate-200 transition-colors hover:border-slate-300 shadow-inner md:ml-2"
                        aria-label="Toggle language"
                    >
                        <div
                            className={`absolute left-1 top-1 bottom-1 w-7 bg-white rounded-full shadow transition-transform duration-300 ease-in-out ${i18n.language === 'en' ? 'translate-x-[30px]' : 'translate-x-0'}`}
                        />
                        <span className={`relative z-10 w-7 text-center text-xs font-bold transition-colors duration-300 flex items-center justify-center ${i18n.language === 'de' ? 'text-slate-900' : 'text-slate-400 hover:text-slate-600'}`}>DE</span>
                        <span className={`relative z-10 w-7 text-center text-xs font-bold transition-colors duration-300 flex items-center justify-center ${i18n.language === 'en' ? 'text-slate-900' : 'text-slate-400 hover:text-slate-600'}`}>EN</span>
                    </button>
                </div>
            </div>
        </nav>
    );
}
