import React, { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileDown, Check, Download, Loader2 } from 'lucide-react';
import { toast } from "sonner";
import { api } from '@/lib/api';
import { useTranslation } from 'react-i18next';

export function DownloadCTA({ responseId }) {
    const { t, i18n } = useTranslation();
    const [isDownloading, setIsDownloading] = useState(false);

    const handleDownload = async () => {
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
            toast.success(t('results.download.toastSuccess'));
        } catch (error) {
            console.error("Download failed", error);
            toast.error(t('results.download.toastError'));
        } finally {
            setIsDownloading(false);
        }
    };

    return (
        <section className="py-12" id="download-cta">
            <div className="relative rounded-3xl overflow-hidden p-[1px] bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 shadow-2xl">
                <div className="bg-white rounded-[23px] relative overflow-hidden">
                    <div className="absolute top-0 right-0 -mt-20 -mr-20 w-80 h-80 bg-blue-100 rounded-full blur-3xl opacity-50" />
                    <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-80 h-80 bg-purple-100 rounded-full blur-3xl opacity-50" />

                    <div className="relative z-10 p-8 md:p-12 flex flex-col md:flex-row items-center gap-10 text-center md:text-left">
                        {/* Icon Section */}
                        <div className="flex-shrink-0">
                            <div className="w-24 h-24 rounded-2xl bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white shadow-xl rotate-3 transform hover:rotate-6 transition-transform duration-300">
                                <FileDown className="w-10 h-10" />
                            </div>
                        </div>

                        {/* Content Section */}
                        <div className="flex-1 space-y-6">
                            <div>
                                <h2 className="text-3xl font-bold text-slate-900 tracking-tight">{t('results.download.title')}</h2>
                                <p className="text-slate-600 text-lg mt-2">
                                    {t('results.download.desc')}
                                </p>
                            </div>

                            {/* Features Grid */}
                            <div className="flex flex-wrap gap-4 justify-center md:justify-start">
                                {[
                                    t('results.download.features.technical', 'Full Technical Analysis'),
                                    t('results.download.features.executive', 'Executive Summary'),
                                    t('results.download.features.charts', 'High-Resolution Charts'),
                                    t('results.download.features.licensing', 'Team Licensing Included')
                                ].map((feature, i) => (
                                    <div key={i} className="flex items-center gap-2 bg-slate-50 px-4 py-2 rounded-lg border border-slate-100 text-sm font-semibold text-slate-700">
                                        <Check className="w-4 h-4 text-emerald-500" /> {feature}
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Button Section */}
                        <div className="flex-shrink-0 w-full md:w-auto">
                            <Button
                                onClick={handleDownload}
                                disabled={isDownloading}
                                size="lg"
                                className="w-full md:w-auto relative px-8 h-16 text-lg font-bold rounded-2xl transition-all shadow-[0_10px_40px_-10px_rgba(79,70,229,0.5)] active:scale-95 bg-gradient-to-r from-indigo-600 to-violet-600 hover:from-indigo-700 hover:to-violet-700 text-white border-0 ring-1 ring-white/20 overflow-hidden group"
                            >
                                <div className="absolute inset-0 -translate-x-full group-hover:animate-[shimmer_2s_infinite] bg-gradient-to-r from-transparent via-white/20 to-transparent z-10" />
                                <span className="relative z-20 flex items-center">
                                    {isDownloading ? <Loader2 className="w-5 h-5 mr-2 animate-spin" /> : <Download className="mr-2 w-5 h-5" />}
                                    {isDownloading ? t('results.download.btnGenerating', "Generating...") : t('results.download.btnDownload', "Download Full PDF Report")}
                                </span>
                            </Button>
                            <p className="text-xs text-center mt-3 text-slate-400 font-medium">
                                {t('results.download.instantly', 'Generated instantly • PDF')}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
