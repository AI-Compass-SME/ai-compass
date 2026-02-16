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

const MIN_LOADING_TIME_MS = 3000;

export default function CompanySnapshot() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        company_name: '',
        industry: '',
        website: '',
        number_of_employees: '',
        city: '',
        email: ''
    });
    const [agreedToGDPR, setAgreedToGDPR] = useState(false);
    const [status, setStatus] = useState('idle'); // idle, analyzing, complete

    // Load session
    useEffect(() => {
        const session = getSession();
        if (!session.responseId) {
            // If no session, redirect to landing
            toast.error("No active assessment found.");
            navigate('/');
        }
        document.title = "AI Compass: Company Profile";
    }, [navigate]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSelectChange = (name, value) => {
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!agreedToGDPR) {
            toast.error("Please agree to the privacy policy to continue.");
            return;
        }

        const session = getSession();
        if (!session.responseId) return;

        setStatus('analyzing');
        const startTime = Date.now();

        try {
            // 1. Trigger Backend Completion
            await api.completeAssessment(parseInt(session.responseId), formData);

            // 2. Ensure Minimum Loading Time
            const elapsed = Date.now() - startTime;
            const remaining = Math.max(0, MIN_LOADING_TIME_MS - elapsed);

            setTimeout(() => {
                setStatus('complete');
                toast.success("Analysis complete!");
                navigate(`/results/${session.responseId}`);
            }, remaining);

        } catch (error) {
            console.error('Error completing assessment:', error);
            toast.error(`Failed to complete assessment: ${error.message}`);
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

    return (
        <div className="flex items-center justify-center min-h-screen p-4 relative overflow-hidden font-sans">
            <PageBackground />

            <Card className="w-full max-w-2xl glass-premium shadow-2xl relative z-10 border-white/60">
                <CardHeader className="text-center space-y-1 pb-6 border-b border-white/20 bg-white/30">
                    <div className="mx-auto w-12 h-12 bg-gradient-to-br from-indigo-600 to-violet-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-indigo-500/30 ring-4 ring-white">
                        <Building2 className="w-6 h-6 text-white" />
                    </div>
                    <CardTitle className="text-3xl font-bold text-slate-900 font-heading">
                        Final Step: Company Profile
                    </CardTitle>
                    <CardDescription className="text-slate-600 text-base max-w-md mx-auto">
                        To provide accurate benchmarking, we need a few details about your organization.
                    </CardDescription>
                </CardHeader>
                <CardContent className="pt-8 px-6 md:px-8">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                            <div className="space-y-2 md:col-span-2">
                                <Label htmlFor="company_name" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    Company Name <span className="text-red-500">*</span>
                                </Label>
                                <div className="relative group">
                                    <Building2 className="absolute left-3 top-2.5 h-5 w-5 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="company_name"
                                        name="company_name"
                                        required
                                        placeholder="e.g. Acme Corp"
                                        value={formData.company_name}
                                        onChange={handleChange}
                                        className="pl-10 h-11 bg-white border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all text-base"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="industry" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    Industry <span className="text-red-500">*</span>
                                </Label>
                                <Select
                                    name="industry"
                                    value={formData.industry}
                                    onValueChange={(val) => handleSelectChange('industry', val)}
                                    required
                                >
                                    <SelectTrigger className="h-11 bg-white border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all text-base">
                                        <SelectValue placeholder="Select industry" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="Technology">Technology</SelectItem>
                                        <SelectItem value="Manufacturing">Manufacturing</SelectItem>
                                        <SelectItem value="Healthcare">Healthcare</SelectItem>
                                        <SelectItem value="Finance">Finance</SelectItem>
                                        <SelectItem value="Retail">Retail</SelectItem>
                                        <SelectItem value="Consulting">Consulting</SelectItem>
                                        <SelectItem value="Education">Education</SelectItem>
                                        <SelectItem value="Other">Other</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="number_of_employees" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    Company Size <span className="text-red-500">*</span>
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
                                            <SelectValue placeholder="Select size" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="1-10">1-10 employees</SelectItem>
                                            <SelectItem value="11-50">11-50 employees</SelectItem>
                                            <SelectItem value="51-200">51-200 employees</SelectItem>
                                            <SelectItem value="201-500">201-500 employees</SelectItem>
                                            <SelectItem value="500+">500+ employees</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>

                            <div className="space-y-2 md:col-span-2">
                                <Label htmlFor="website" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    Website <span className="text-slate-400 font-normal normal-case">(Optional)</span>
                                </Label>
                                <div className="relative group">
                                    <Globe className="absolute left-3 top-2.5 h-5 w-5 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="website"
                                        name="website"
                                        type="url"
                                        placeholder="https://example.com"
                                        value={formData.website}
                                        onChange={handleChange}
                                        className="pl-10 h-11 bg-white border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all text-base"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="city" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    Headquarters City
                                </Label>
                                <div className="relative group">
                                    <MapPin className="absolute left-3 top-2.5 h-5 w-5 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="city"
                                        name="city"
                                        placeholder="e.g. Berlin"
                                        value={formData.city}
                                        onChange={handleChange}
                                        className="pl-10 h-11 bg-white border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all text-base"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="email" className="text-slate-700 font-bold text-xs uppercase tracking-wide">
                                    Work Email <span className="text-red-500">*</span>
                                </Label>
                                <div className="relative group">
                                    <Mail className="absolute left-3 top-2.5 h-5 w-5 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="email"
                                        name="email"
                                        type="email"
                                        required
                                        placeholder="name@company.com"
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
                                        I consent to the processing of my data to generate the maturity report.
                                    </label>
                                    <p className="text-xs text-slate-500">
                                        We respect your privacy. Your data is used solely for benchmarking and generating your report.
                                        See our <a href="/privacy" className="underline text-blue-600 hover:text-blue-800" target="_blank">Privacy Policy</a>.
                                    </p>
                                </div>
                            </div>
                        </div>

                        <Button
                            type="submit"
                            size="lg"
                            className="w-full h-12 text-base font-bold bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 shadow-lg shadow-indigo-500/25 transition-all group"
                            disabled={status === ('analyzing')}
                        >
                            Generate My Report
                            <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
