import React, { useState, useEffect } from 'react';
import { PageBackground } from '@/components/ui/PageBackground';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { getSession } from '../lib/assessment';
import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";
import { Building2, Globe, Users, MapPin, Mail, ArrowRight, Loader2, Lock } from 'lucide-react';
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";

const MIN_LOADING_TIME_MS = 3000;

export default function CompanySnapshot() {
    const navigate = useNavigate();
    const { t, i18n } = useTranslation();
    const [formData, setFormData] = useState({
        company_name: '',
        industry: '',
        website: '',
        number_of_employees: '',
        city: '',
        email: ''
    });
    const [agreedToGDPR, setAgreedToGDPR] = useState(false);
    const [status, setStatus] = useState('idle'); // idle, analyzing, verify_email
    const [userEmail, setUserEmail] = useState('');

    // Load session
    useEffect(() => {
        const session = getSession();
        if (!session.responseId) {
            // If no session, redirect to landing
            toast.error(t('snapshot.toasts.noActiveAssessment', "No active assessment found."));
            navigate('/');
        }
        document.title = t('snapshot.pageTitle', "AI Compass: Company Profile");
    }, [navigate, t]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSelectChange = (name, value) => {
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!agreedToGDPR) {
            toast.error(t('snapshot.toasts.agreePrivacy', "Please agree to the privacy policy to continue."));
            return;
        }

        const session = getSession();
        if (!session.responseId) return;

        setStatus('analyzing');
        const startTime = Date.now();

        try {
            // 1. Trigger Backend Completion
            const { result_hash } = await api.completeAssessment(parseInt(session.responseId), formData, i18n.language);

            // 2. Ensure Minimum Loading Time
            const elapsed = Date.now() - startTime;
            const remaining = Math.max(0, MIN_LOADING_TIME_MS - elapsed);

            setTimeout(() => {
                setStatus('verify_email');
                setUserEmail(formData.email);
            }, remaining);

        } catch (error) {
            console.error('Error completing assessment:', error);
            toast.error(t('snapshot.toasts.submitError', `Failed to complete assessment: ${error.message}`));
            setStatus('idle');
        }
    };

    if (status === 'analyzing') {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen p-4 relative overflow-hidden font-sans">
                <PageBackground />
                <div className="relative z-10 flex flex-col items-center text-center">
                    <div className="relative mb-8">
                        <div className="absolute inset-0 bg-blue-500 blur-xl opacity-20 animate-pulse rounded-full"></div>
                        <div className="w-20 h-20 bg-white rounded-2xl shadow-xl flex items-center justify-center ring-1 ring-slate-100">
                            <Loader2 className="w-10 h-10 text-blue-600 animate-spin" />
                        </div>
                    </div>
                    <motion.h2
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-2xl font-bold text-slate-900 mb-2 font-heading"
                    >
                        Finalizing your strategic AI roadmap...
                    </motion.h2>
                    <p className="text-slate-500 max-w-md">
                        Verifying your industry benchmarks and generating actionable insights.
                    </p>
                </div>
            </div>
        );
    }

    if (status === 'verify_email') {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen p-4 relative overflow-hidden font-sans">
                <PageBackground />
                <Card className="w-full max-w-lg glass-premium shadow-2xl relative z-10 border-white/60 text-center">
                    <CardHeader className="space-y-4 pb-6 border-b border-white/20 bg-white/30">
                        <div className="mx-auto w-16 h-16 bg-gradient-to-br from-indigo-500 to-emerald-500 rounded-full flex items-center justify-center mb-2 shadow-lg ring-4 ring-white">
                            <Mail className="w-8 h-8 text-white" />
                        </div>
                        <CardTitle className="text-2xl font-bold text-slate-900 font-heading">
                            Please Verify Your Email
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="pt-8 px-6 text-slate-600">
                        <p className="mb-4 text-base">
                            We've sent a secure verification link to:<br />
                            <strong className="text-slate-900">{userEmail}</strong>
                        </p>
                        <p className="text-sm">
                            Click the link in the email to instantly access your <strong>results page</strong> and receive your comprehensive <strong>PDF report</strong>.
                        </p>
                        <div className="mt-8">
                            <Button
                                variant="outline"
                                onClick={() => window.location.href = '/'}
                                className="w-full bg-white/50 border-slate-200"
                            >
                                Return to Homepage
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="flex items-start justify-center min-h-screen pt-20 pb-8 px-4 relative overflow-hidden font-sans">
            <PageBackground />

            <Card className="w-full max-w-4xl glass-premium shadow-2xl relative z-10 border-white/60">
                <CardHeader className="text-center space-y-1 pb-2 border-b border-white/20 bg-white/30">
                    <div className="mx-auto w-12 h-12 bg-gradient-to-br from-indigo-600 to-violet-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-indigo-500/30 ring-4 ring-white">
                        <Building2 className="w-6 h-6 text-white" />
                    </div>
                    <CardTitle className="text-3xl font-bold text-slate-900 font-heading">
                        {i18n.language === 'de' ? 'Letzter Schritt: Unternehmensprofil' : 'Final Step: Company Profile'}
                    </CardTitle>
                    <CardDescription className="text-slate-600 text-base max-w-md mx-auto">
                        {i18n.language === 'de' ? 'Norden Sie Ihren KI-Kompass: Nur noch diese Details trennen Sie von Ihrem glasklaren Fahrplan für die Umsetzung.' : 'To provide accurate benchmarking, we need a few details about your organization.'}
                    </CardDescription>
                </CardHeader>
                <CardContent className="pt-3 px-6 md:px-8">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                            <div className="space-y-2">
                                <Label htmlFor="company_name" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    {i18n.language === 'de' ? 'Unternehmensname' : 'Company Name'} <span className="text-red-500">*</span>
                                </Label>
                                <div className="relative group">
                                    <Building2 className="absolute left-3 top-2.5 h-5 w-5 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="company_name"
                                        name="company_name"
                                        required
                                        placeholder={i18n.language === 'de' ? 'z.B. Muster GmbH' : 'e.g. Acme Corp'}
                                        value={formData.company_name}
                                        onChange={handleChange}
                                        className="pl-10 h-11 bg-white border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all text-base"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="industry" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    {i18n.language === 'de' ? 'Branche' : 'Industry'} <span className="text-red-500">*</span>
                                </Label>
                                <Select
                                    name="industry"
                                    value={formData.industry}
                                    onValueChange={(val) => handleSelectChange('industry', val)}
                                    required
                                >
                                    <SelectTrigger className="h-11 bg-white border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all text-base">
                                        <SelectValue placeholder={i18n.language === 'de' ? 'Branche wählen' : 'Select industry'} />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {i18n.language === 'de' ? (
                                            <>
                                                <SelectItem value="Industrie & Produktion">Industrie & Produktion</SelectItem>
                                                <SelectItem value="Handwerk & Baugewerbe">Handwerk & Baugewerbe</SelectItem>
                                                <SelectItem value="Handel & E-Commerce">Handel & E-Commerce</SelectItem>
                                                <SelectItem value="Dienstleistungen & Beratung">Dienstleistungen & Beratung</SelectItem>
                                                <SelectItem value="IT & Software">IT & Software</SelectItem>
                                                <SelectItem value="Gesundheits- & Sozialwesen">Gesundheits- & Sozialwesen</SelectItem>
                                                <SelectItem value="Logistik & Transport">Logistik & Transport</SelectItem>
                                                <SelectItem value="Sonstige">Sonstige</SelectItem>
                                            </>
                                        ) : (
                                            <>
                                                <SelectItem value="Technology">Technology</SelectItem>
                                                <SelectItem value="Manufacturing">Manufacturing</SelectItem>
                                                <SelectItem value="Healthcare">Healthcare</SelectItem>
                                                <SelectItem value="Finance">Finance</SelectItem>
                                                <SelectItem value="Retail">Retail</SelectItem>
                                                <SelectItem value="Consulting">Consulting</SelectItem>
                                                <SelectItem value="Education">Education</SelectItem>
                                                <SelectItem value="Other">Other</SelectItem>
                                            </>
                                        )}
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="number_of_employees" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    {i18n.language === 'de' ? 'Unternehmensgröße' : 'Company Size'} <span className="text-red-500">*</span>
                                </Label>
                                <div className="relative group">
                                    <Users className="absolute left-3 top-2.5 h-5 w-5 z-10 text-slate-400 pointer-events-none group-focus-within:text-indigo-600 transition-colors" />
                                    <Select
                                        name="number_of_employees"
                                        value={formData.number_of_employees}
                                        onValueChange={(val) => handleSelectChange('number_of_employees', val)}
                                        required
                                    >
                                        <SelectTrigger className="h-11 pl-10 bg-white border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all text-base">
                                            <SelectValue placeholder={i18n.language === 'de' ? 'Größe wählen' : 'Select size'} />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {i18n.language === 'de' ? (
                                                <>
                                                    <SelectItem value="1">Selbstständig / 1 Mitarbeiter</SelectItem>
                                                    <SelectItem value="2-10">2 – 10 Mitarbeiter</SelectItem>
                                                    <SelectItem value="11-50">11 – 50 Mitarbeiter</SelectItem>
                                                    <SelectItem value="51-250">51 – 250 Mitarbeiter</SelectItem>
                                                    <SelectItem value="250+">Über 250 Mitarbeiter</SelectItem>
                                                </>
                                            ) : (
                                                <>
                                                    <SelectItem value="1-10">1-10 employees</SelectItem>
                                                    <SelectItem value="11-50">11-50 employees</SelectItem>
                                                    <SelectItem value="51-200">51-200 employees</SelectItem>
                                                    <SelectItem value="201-500">201-500 employees</SelectItem>
                                                    <SelectItem value="500+">500+ employees</SelectItem>
                                                </>
                                            )}
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="website" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    {i18n.language === 'de' ? 'Website' : 'Website'} <span className="text-slate-400 font-normal normal-case">({i18n.language === 'de' ? 'Optional' : 'Optional'})</span>
                                </Label>
                                <div className="relative group">
                                    <Globe className="absolute left-3 top-2.5 h-5 w-5 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="website"
                                        name="website"
                                        type="url"
                                        placeholder={i18n.language === 'de' ? 'https://ihre-firma.de' : 'https://example.com'}
                                        value={formData.website}
                                        onChange={handleChange}
                                        className="pl-10 h-11 bg-white border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all text-base"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="city" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    {i18n.language === 'de' ? 'Hauptsitz' : 'Headquarters'} <span className="text-slate-400 font-normal normal-case">({i18n.language === 'de' ? 'Optional' : 'Optional'})</span>
                                </Label>
                                <div className="relative group">
                                    <MapPin className="absolute left-3 top-2.5 h-5 w-5 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="city"
                                        name="city"
                                        placeholder={i18n.language === 'de' ? 'z.B. Hamburg' : 'e.g. Berlin'}
                                        value={formData.city}
                                        onChange={handleChange}
                                        className="pl-10 h-11 bg-white border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all text-base"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="email" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    {i18n.language === 'de' ? 'Geschäftliche E-Mail' : 'Work Email'} <span className="text-red-500">*</span>
                                </Label>
                                <div className="relative group">
                                    <Mail className="absolute left-3 top-2.5 h-5 w-5 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="email"
                                        name="email"
                                        type="email"
                                        required
                                        placeholder={i18n.language === 'de' ? 'name@unternehmen.de' : 'name@company.com'}
                                        value={formData.email}
                                        onChange={handleChange}
                                        className="pl-10 h-11 bg-white border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all text-base"
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="pt-4 border-t border-slate-100">
                            <div className="flex items-start space-x-3 p-4 bg-blue-50/50 rounded-xl border border-blue-100">
                                <Checkbox
                                    id="gdpr"
                                    checked={agreedToGDPR}
                                    onCheckedChange={setAgreedToGDPR}
                                    className="mt-1 data-[state=checked]:bg-blue-600"
                                />
                                <div className="grid gap-1.5 leading-none">
                                    <label
                                        htmlFor="gdpr"
                                        className="text-sm font-medium leading-normal text-slate-700 cursor-pointer"
                                    >
                                        {i18n.language === 'de' ? 'Ich willige in die Verarbeitung meiner Daten zur Erstellung meiner individuellen KI-Potenzialanalyse ein.' : 'I consent to the processing of my data to generate the maturity report.'}
                                    </label>
                                    <p className="text-xs text-slate-500">
                                        {i18n.language === 'de' ? 'Wir nehmen Datenschutz ernst: Ihre Daten werden ausschließlich für das Benchmarking und die Erstellung Ihres individuellen Reports verwendet. Details finden Sie in unserer ' : 'We respect your privacy. Your data is used solely for benchmarking and generating your report. See our '}
                                        <a href="/privacy" className="underline text-blue-600 hover:text-blue-800" target="_blank">{i18n.language === 'de' ? 'Datenschutzerklärung' : 'Privacy Policy'}</a>.
                                    </p>
                                    <div className="border-t border-blue-100 mt-2 pt-2">
                                        <p className="text-xs font-semibold text-slate-600 mb-1">
                                            {i18n.language === 'de' ? 'KI-Transparenz & Methodik:' : 'AI Transparency & Methodology:'}
                                        </p>
                                        <p className="text-xs text-slate-500 leading-relaxed">
                                            {i18n.language === 'de'
                                                ? 'Der AI Compass kombiniert statistische Verfahren (K-Means-Clustering) mit generativer KI, um präzise Muster in Ihrer Unternehmensstruktur zu identifizieren. Alle Analyseergebnisse basieren auf modellbasierten Wahrscheinlichkeiten und dienen als strategische Orientierungshilfe; sie ersetzen keine individuelle Expertenprüfung. Die Nutzung dieser Plattform stellt keine Rechtsberatung dar und begründet kein formales Beratungsmandat.'
                                                : 'The AI Compass combines statistical methods (K-Means clustering) with generative AI to identify precise patterns in your organizational structure. All analysis results are based on model-driven probabilities and serve as strategic guidance; they do not replace individual expert review. Use of this platform does not constitute legal advice or establish a formal advisory relationship.'}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <Button
                            type="submit"
                            size="lg"
                            className="w-full h-12 text-base font-bold bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-500/25 transition-all group"
                            disabled={status === ('analyzing')}
                        >
                            {i18n.language === 'de' ? 'Meinen persönlichen Report erstellen' : 'Generate My Report'}
                            <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
