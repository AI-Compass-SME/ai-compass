import React, { useEffect, useState } from 'react';
import { PageBackground } from '@/components/ui/PageBackground';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { api } from '../lib/api';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Loader2, CheckCircle2, XCircle, FileText, ArrowRight } from 'lucide-react';
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { useTranslation } from 'react-i18next';

export default function VerifyPage() {
    const { t } = useTranslation();
    const [searchParams] = useSearchParams();
    const token = searchParams.get('token');
    const navigate = useNavigate();
    const [status, setStatus] = useState('verifying'); // verifying, success, error

    useEffect(() => {
        if (!token) {
            setStatus('error');
            return;
        }

        async function verify() {
            try {
                await api.verifyEmail(token);
                setStatus('success');
                // Auto-redirect to the results after brief success message
                setTimeout(() => {
                    navigate(`/results/${token}`);
                }, 3000);
            } catch (err) {
                console.error("Verification failed:", err);
                setStatus('error');
                toast.error(err.message || t('verify.toasts.invalidLink', "Invalid or expired verification link"));
            }
        }

        // Slight delay for UI smoothing
        const timer = setTimeout(() => verify(), 800);
        return () => clearTimeout(timer);

    }, [token, navigate]);

    useEffect(() => {
        document.title = t('verify.pageTitle', "AI Compass: Verifying Email...");
    }, [t]);

    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4 relative overflow-hidden font-sans">
            <PageBackground />
            <Card className="w-full max-w-lg glass-premium shadow-2xl relative z-10 border-white/60 text-center">

                {status === 'verifying' && (
                    <>
                        <CardHeader className="space-y-4 pb-6 border-b border-white/20 bg-white/30">
                            <div className="mx-auto w-16 h-16 bg-white rounded-2xl flex items-center justify-center mb-2 shadow-xl ring-1 ring-slate-100">
                                <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
                            </div>
                            <CardTitle className="text-2xl font-bold text-slate-900 font-heading">
                                {t('verifyPage.verifying.title', "Verifying your email...")}
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-8 px-6 text-slate-600">
                            <p>{t('verifyPage.verifying.desc', "Please wait while we securely validate your link and generate your maturity report PDF.")}</p>
                        </CardContent>
                    </>
                )}

                {status === 'success' && (
                    <>
                        <CardHeader className="space-y-4 pb-6 border-b border-white/20 bg-emerald-50/50">
                            <div className="mx-auto w-16 h-16 bg-gradient-to-br from-emerald-400 to-emerald-600 rounded-full flex items-center justify-center mb-2 shadow-lg ring-4 ring-white">
                                <CheckCircle2 className="w-8 h-8 text-white" />
                            </div>
                            <CardTitle className="text-2xl font-bold text-slate-900 font-heading">
                                {t('verifyPage.success.title', "Email Verified Successfully!")}
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-8 px-6 text-slate-600 space-y-4 flex flex-col items-center">
                            <p className="text-base text-slate-700 font-medium">
                                {t('verifyPage.success.sent', "We've sent your PDF report to your inbox.")}
                            </p>
                            <p className="text-sm">
                                {t('verifyPage.success.redirecting', "Redirecting you to your interactive dashboard...")}
                            </p>
                            <Loader2 className="w-5 h-5 text-emerald-600 animate-spin mt-2" />
                        </CardContent>
                    </>
                )}

                {status === 'error' && (
                    <>
                        <CardHeader className="space-y-4 pb-6 border-b border-white/20 bg-red-50/50">
                            <div className="mx-auto w-16 h-16 bg-gradient-to-br from-red-400 to-red-600 rounded-full flex items-center justify-center mb-2 shadow-lg ring-4 ring-white">
                                <XCircle className="w-8 h-8 text-white" />
                            </div>
                            <CardTitle className="text-2xl font-bold text-slate-900 font-heading">
                                {t('verifyPage.error.title', "Verification Failed")}
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-8 px-6 text-slate-600">
                            <p className="mb-6">{t('verifyPage.error.desc', "The verification link is invalid, expired, or may have already been used.")}</p>
                            <Button asChild size="lg" className="w-full bg-slate-900 text-white hover:bg-slate-800">
                                <Link to="/">{t('verifyPage.error.return', "Return to Homepage")}</Link>
                            </Button>
                        </CardContent>
                    </>
                )}
            </Card>
        </div>
    );
}
