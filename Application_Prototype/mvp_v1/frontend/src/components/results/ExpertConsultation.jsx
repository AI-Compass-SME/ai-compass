import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Calendar, CheckCircle, ArrowRight } from 'lucide-react';
import { toast } from "sonner";

export function ExpertConsultation() {
    const handleBooking = () => {
        toast.info("Consultation booking feature coming soon!", {
            description: "We are currently integrating with our scheduling system."
        });
    };

    return (
        <section className="py-6 relative isolate overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 -z-10 bg-slate-900" />
            <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-purple-900/50 via-slate-900 to-slate-900" />
            <div className="absolute top-0 right-0 -z-10 h-[500px] w-[500px] bg-indigo-600/30 rounded-full blur-[100px] opacity-50" />
            <div className="absolute bottom-0 left-0 -z-10 h-[500px] w-[500px] bg-blue-600/20 rounded-full blur-[100px] opacity-30" />

            <div className="mx-auto max-w-7xl px-6 lg:px-8">
                <div className="mx-auto max-w-2xl text-center mb-4">
                    <h2 className="text-2xl font-bold tracking-tight text-white sm:text-3xl">Expert Consultation & Next Steps</h2>
                    <p className="mt-2 text-base text-slate-300">
                        Transition from digital analysis to human-led transformation.
                    </p>
                </div>

                <div className="relative rounded-3xl bg-white/5 backdrop-blur-xl ring-1 ring-white/10 p-4 sm:p-6 overflow-hidden">
                    <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 bg-indigo-500/20 rounded-full blur-3xl" />

                    <div className="flex flex-col md:flex-row items-center gap-6 relative z-10">
                        {/* Left Content */}
                        <div className="flex-1 space-y-3 text-center md:text-left">
                            <h3 className="text-2xl md:text-3xl font-bold text-white tracking-tight">
                                Get in Touch for a Strategy Deep-Dive
                            </h3>

                            <p className="text-base text-slate-300 leading-relaxed max-w-xl">
                                Every SME journey is unique. Contact our AI Compass strategist to validate your roadmap and identify industry-specific 'Low-Hanging Fruit'.
                            </p>

                            <div className="space-y-2 pt-1">
                                {/* Contact Information */}
                                <div className="bg-slate-900/50 rounded-2xl p-4 ring-1 ring-white/10 max-w-md mx-auto md:mx-0">
                                    <div className="space-y-3">
                                        <div className="flex items-start gap-3">
                                            <div className="flex-none p-1.5 rounded-lg bg-indigo-500/20 text-indigo-300">
                                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                                                </svg>
                                            </div>
                                            <div className="flex-1">
                                                <p className="text-xs font-medium text-slate-400">Email</p>
                                                <a href="mailto:contact@ai-compass.com" className="text-white text-sm font-semibold hover:text-indigo-300 transition-colors">
                                                    contact@ai-compass.com
                                                </a>
                                            </div>
                                        </div>

                                        <div className="flex items-start gap-3">
                                            <div className="flex-none p-1.5 rounded-lg bg-indigo-500/20 text-indigo-300">
                                                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                                                </svg>
                                            </div>
                                            <div className="flex-1">
                                                <p className="text-xs font-medium text-slate-400">Phone</p>
                                                <a href="tel:+1234567890" className="text-white text-sm font-semibold hover:text-indigo-300 transition-colors">
                                                    +1 (234) 567-890
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Right Content / Features */}
                        <div className="flex-shrink-0 w-full md:w-auto">
                            <div className="bg-slate-900/50 rounded-2xl p-4 ring-1 ring-white/10 max-w-sm mx-auto">
                                <ul className="space-y-2.5">
                                    {[
                                        "30-minute expert session",
                                        "Industry-specific benchmarks",
                                        "Roadmap validation",
                                        "Budget ROI modeling"
                                    ].map((feature, i) => (
                                        <li key={i} className="flex items-center gap-2.5 text-slate-200 text-sm">
                                            <div className="flex-none p-0.5 rounded-full bg-emerald-500/20 text-emerald-400">
                                                <CheckCircle className="w-4 h-4" />
                                            </div>
                                            <span className="font-medium">{feature}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
