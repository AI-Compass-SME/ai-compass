import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';
import { Button } from "@/components/ui/button";
import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2, BarChart3, FileText, Lightbulb, Workflow, Network, Fingerprint, Hexagon } from 'lucide-react';

export default function HowItWorksPage() {
    useEffect(() => {
        document.title = "How It Works | AI Compass";
    }, []);

    const steps = [
        {
            id: 1,
            title: "Assess",
            description: "Answer a structured questionnaire covering 7 key dimensions of AI maturity. Our framework evaluates your capabilities across strategy, data, and technology.",
            icon: <FileText className="w-6 h-6 text-blue-600" />
        },
        {
            id: 2,
            title: "Analyze",
            description: "Our ML engine compares your data against industry benchmarks. We identify your 'Cluster Profile' using our proprietary maturity model.",
            icon: <BarChart3 className="w-6 h-6 text-indigo-600" />
        },
        {
            id: 3,
            title: "Act",
            description: "Receive a comprehensive strategic roadmap. Get concrete, actionable steps to move from your current state to the next maturity level.",
            icon: <Lightbulb className="w-6 h-6 text-violet-600" />
        }
    ];

    const dimensions = [
        "Strategy & Leadership",
        "Use Cases & Value",
        "Data & Infrastructure",
        "Talent & Culture",
        "Governance & Ethics",
        "Technology & Tools",
        "Partnerships & Ecosystem"
    ];

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-6 pt-28 pb-16 relative z-10">
                {/* Standardized Header */}
                <PageHeader
                    title="How It Works"
                    subtitle="THE AI COMPASS PROCESS"
                />

                {/* Content Card */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 md:p-12 space-y-12">

                    {/* Section 1: The Process */}
                    <section>
                        <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                            <div className="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center text-blue-600 border border-blue-200 shadow-sm">
                                <Workflow className="w-5 h-5" />
                            </div>
                            The Evaluation Process
                        </h2>
                        <div className="grid md:grid-cols-3 gap-8">
                            {steps.map((step) => (
                                <div key={step.id} className="bg-slate-50 p-6 rounded-xl border border-slate-100">
                                    <div className="w-12 h-12 bg-white rounded-lg shadow-sm flex items-center justify-center mb-4 border border-slate-100">
                                        {step.icon}
                                    </div>
                                    <h3 className="font-bold text-gray-900 mb-2">{step.title}</h3>
                                    <p className="text-sm text-gray-600 leading-relaxed">
                                        {step.description}
                                    </p>
                                </div>
                            ))}
                        </div>
                    </section>

                    <hr className="border-gray-100" />

                    {/* Section 2: The Framework */}
                    <section>
                        <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                            <div className="w-8 h-8 rounded-lg bg-indigo-100 flex items-center justify-center text-indigo-600 border border-indigo-200 shadow-sm">
                                <Network className="w-5 h-5" />
                            </div>
                            The 7-Dimension Framework
                        </h2>
                        <p className="text-gray-600 mb-6">
                            We don't just look at technology. True AI maturity requires a holistic approach across your entire organization. Our assessment evaluates:
                        </p>
                        <div className="grid sm:grid-cols-2 gap-4">
                            {dimensions.map((dim, idx) => (
                                <div key={idx} className="flex items-center gap-3 p-3 bg-white border border-slate-100 rounded-lg shadow-sm hover:border-indigo-100 transition-colors group">
                                    <div className="relative w-5 h-5 flex-shrink-0 flex items-center justify-center">
                                        <Hexagon className="w-5 h-5 text-indigo-500 absolute" />
                                        <Hexagon className="w-2.5 h-2.5 text-indigo-500 fill-indigo-500 absolute transition-transform group-hover:scale-110" />
                                    </div>
                                    <span className="font-medium text-gray-700">{dim}</span>
                                </div>
                            ))}
                        </div>
                    </section>

                    <div className="flex justify-center pt-8">
                        <Button asChild size="lg" className="px-8 h-12 text-base font-bold rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:shadow-lg hover:scene-pop transition-all">
                            <Link to="/snapshot" className="flex items-center gap-2">
                                Start Your Assessment
                                <ArrowRight className="w-5 h-5" />
                            </Link>
                        </Button>
                    </div>

                </div>
            </main>

            <Footer />
        </div>
    );
}
