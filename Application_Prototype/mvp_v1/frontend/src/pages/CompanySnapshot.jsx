import React, { useState, useEffect } from 'react';
import { PageBackground } from '@/components/ui/PageBackground';
import { useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";
import { Building2, Globe, Users, MapPin, Mail, ArrowRight } from 'lucide-react';

export default function CompanySnapshot() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        company_name: '',
        industry: 'Technology',
        website: '',
        number_of_employees: '1-10',
        city: '',
        email: ''
    });
    const [loading, setLoading] = useState(false);

    // Prefetch questionnaire data in background
    useEffect(() => {
        const prefetchData = async () => {
            try {
                // Check if already cached to avoid redundant calls
                if (!sessionStorage.getItem('cached_questionnaire_data')) {
                    console.log("SNAPSHOT: Starting background prefetch of questionnaire...");
                    console.time("prefetchDuration");
                    const data = await api.getQuestionnaire();
                    console.timeEnd("prefetchDuration");

                    if (data) {
                        try {
                            const stringified = JSON.stringify(data);
                            sessionStorage.setItem('cached_questionnaire_data', stringified);
                            console.log(`SNAPSHOT: Prefetch complete. Cached ${stringified.length} bytes.`);
                        } catch (writeErr) {
                            console.error("SNAPSHOT: Failed to write to sessionStorage", writeErr);
                        }
                    }
                } else {
                    console.log("SNAPSHOT: Data already in cache. Skipping prefetch.");
                }
            } catch (error) {
                console.warn("SNAPSHOT: Background prefetch failed:", error);
            }
        };
        prefetchData();
    }, []);

    // Set page title
    useEffect(() => {
        document.title = "AI Compass: Company Profile";
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            // 1. Create Company
            const company = await api.createCompany(formData);

            // 2. Initialize Response
            const response = await api.createResponse(company.company_id);

            // 3. Save IDs and redirect
            localStorage.setItem('current_response_id', response.response_id);
            toast.success("Company profile created!");
            navigate(`/assessment/${response.response_id}`);
        } catch (error) {
            console.error('Error starting assessment:', error);
            toast.error(`Failed to start assessment: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSelectChange = (name, value) => {
        setFormData({ ...formData, [name]: value });
    };

    return (
        <div className="flex items-center justify-center min-h-screen p-4 relative overflow-hidden">
            <PageBackground />

            <Card className="w-full max-w-xl glass shadow-2xl relative z-10 transition-all duration-500 hover:shadow-indigo-500/10">
                <CardHeader className="text-center space-y-1 pb-2">
                    <div className="mx-auto w-10 h-10 bg-gradient-to-br from-indigo-600 to-violet-600 rounded-xl flex items-center justify-center mb-2 shadow-lg shadow-indigo-500/30 ring-4 ring-white/50">
                        <Building2 className="w-5 h-5 text-white" />
                    </div>
                    <CardTitle className="text-2xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent font-heading">
                        Company Snapshot
                    </CardTitle>
                    <CardDescription className="text-slate-500 text-sm">
                        Tell us a bit about your organization to personalize your benchmark.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-3">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            <div className="space-y-1.5 md:col-span-2">
                                <Label htmlFor="company_name" className="text-slate-700 font-medium text-xs uppercase tracking-wide">
                                    Company Name <span className="text-red-500">*</span>
                                </Label>
                                <div className="relative group">
                                    <Building2 className="absolute left-3 top-2.5 h-4 w-4 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="company_name"
                                        name="company_name"
                                        required
                                        placeholder="Acme Corp"
                                        value={formData.company_name}
                                        onChange={handleChange}
                                        className="pl-9 h-10 text-sm bg-white/50 border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-indigo-500/20 transition-all"
                                    />
                                </div>
                            </div>

                            <div className="space-y-1.5">
                                <Label htmlFor="industry" className="text-slate-700 font-medium text-xs uppercase tracking-wide">
                                    Industry <span className="text-red-500">*</span>
                                </Label>
                                <Select
                                    name="industry"
                                    value={formData.industry}
                                    onValueChange={(val) => handleSelectChange('industry', val)}
                                >
                                    <SelectTrigger className="h-10 text-sm bg-white/50 border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-indigo-500/20 transition-all">
                                        <SelectValue placeholder="Select industry" />
                                    </SelectTrigger>
                                    <SelectContent className="bg-white border shadow-xl text-slate-900">
                                        <SelectItem value="Technology">Technology</SelectItem>
                                        <SelectItem value="Manufacturing">Manufacturing</SelectItem>
                                        <SelectItem value="Healthcare">Healthcare</SelectItem>
                                        <SelectItem value="Finance">Finance</SelectItem>
                                        <SelectItem value="Retail">Retail</SelectItem>
                                        <SelectItem value="Other">Other</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className="space-y-1.5">
                                <Label htmlFor="number_of_employees" className="text-slate-700 font-medium text-xs uppercase tracking-wide">
                                    Employees <span className="text-red-500">*</span>
                                </Label>
                                <div className="relative group">
                                    <Users className="absolute left-3 top-2.5 h-4 w-4 z-10 text-slate-400 pointer-events-none group-focus-within:text-indigo-600 transition-colors" />
                                    <Select
                                        name="number_of_employees"
                                        value={formData.number_of_employees}
                                        onValueChange={(val) => handleSelectChange('number_of_employees', val)}
                                    >
                                        <SelectTrigger className="h-10 pl-9 text-sm bg-white/50 border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-indigo-500/20 transition-all">
                                            <SelectValue placeholder="Select size" />
                                        </SelectTrigger>
                                        <SelectContent className="bg-white border shadow-xl text-slate-900">
                                            <SelectItem value="1-10">1-10</SelectItem>
                                            <SelectItem value="11-50">11-50</SelectItem>
                                            <SelectItem value="51-200">51-200</SelectItem>
                                            <SelectItem value="201-500">201-500</SelectItem>
                                            <SelectItem value="500+">500+</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>

                            <div className="space-y-1.5 md:col-span-2">
                                <Label htmlFor="website" className="text-slate-700 font-medium text-xs uppercase tracking-wide">Website</Label>
                                <div className="relative group">
                                    <Globe className="absolute left-3 top-2.5 h-4 w-4 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="website"
                                        name="website"
                                        type="url"
                                        placeholder="https://example.com"
                                        value={formData.website}
                                        onChange={handleChange}
                                        className="pl-9 h-10 text-sm bg-white/50 border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-indigo-500/20 transition-all"
                                    />
                                </div>
                            </div>

                            <div className="space-y-1.5">
                                <Label htmlFor="city" className="text-slate-700 font-medium text-xs uppercase tracking-wide">City</Label>
                                <div className="relative group">
                                    <MapPin className="absolute left-3 top-2.5 h-4 w-4 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="city"
                                        name="city"
                                        placeholder="New York"
                                        value={formData.city}
                                        onChange={handleChange}
                                        className="pl-9 h-10 text-sm bg-white/50 border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-indigo-500/20 transition-all"
                                    />
                                </div>
                            </div>

                            <div className="space-y-1.5">
                                <Label htmlFor="email" className="text-slate-700 font-medium text-xs uppercase tracking-wide">Email</Label>
                                <div className="relative group">
                                    <Mail className="absolute left-3 top-2.5 h-4 w-4 text-slate-400 group-focus-within:text-indigo-600 transition-colors" />
                                    <Input
                                        id="email"
                                        name="email"
                                        type="email"
                                        placeholder="contact@example.com"
                                        value={formData.email}
                                        onChange={handleChange}
                                        className="pl-9 h-10 text-sm bg-white/50 border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-indigo-500/20 transition-all"
                                    />
                                </div>
                            </div>
                        </div>

                        <p className="text-xs text-slate-400 text-center">* fields are required</p>
                        <Button
                            type="submit"
                            size="lg"
                            className="w-full h-10 mt-2 text-base font-medium group transition-all"
                            disabled={loading}
                        >
                            {loading ? 'Starting...' : 'Continue to Assessment'}
                            {!loading && <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
