import React from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { ArrowRight, Star, TrendingUp, AlertCircle, CheckCircle2 } from 'lucide-react';
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";

// Phase Definitions from ML v5 Spec
// Phase Definitions from ML v5 Spec
const PHASES = [
    {
        key: "phase_1",
        step: "01",
        title: "Foundation",
        timeframe: "0-3 Months",
        color: "bg-blue-50/50 border-blue-100",
        headerColor: "text-blue-700 bg-blue-100/50",
        stepStyle: "bg-blue-100 text-blue-700 ring-blue-50",
        titleStyle: "text-blue-900",
        borderColor: "border-l-blue-500",
        gradientFrom: "from-blue-500"
    },
    {
        key: "phase_2",
        step: "02",
        title: "Implementation",
        timeframe: "3-9 Months",
        color: "bg-indigo-50/50 border-indigo-100",
        headerColor: "text-indigo-700 bg-indigo-100/50",
        stepStyle: "bg-indigo-100 text-indigo-700 ring-indigo-50",
        titleStyle: "text-indigo-900",
        borderColor: "border-l-indigo-500",
        gradientFrom: "from-indigo-500"
    },
    {
        key: "phase_3",
        step: "03",
        title: "Scale & Governance",
        timeframe: "9+ Months",
        color: "bg-purple-50/50 border-purple-100",
        headerColor: "text-purple-700 bg-purple-100/50",
        stepStyle: "bg-purple-100 text-purple-700 ring-purple-50",
        titleStyle: "text-purple-900",
        borderColor: "border-l-purple-500",
        gradientFrom: "from-purple-500"
    }
];

// Helper to determine badge type
const getRecommendationType = (rec) => {
    const source = (rec.source || "").toLowerCase();
    const impact = rec.impact_score || 0;

    if (source.includes("strategic gap") && impact > 10) {
        return { label: "Must-Win Battle", variant: "destructive", icon: AlertCircle };
    } else if (source.includes("growth") || source.includes("peer")) {
        return { label: "Peer Opportunity", variant: "secondary", icon: TrendingUp };
    }
    return { label: "Tactical Step", variant: "outline", icon: Star, className: "bg-amber-50/50 text-amber-700 border-amber-200 hover:bg-amber-100/50" };
};

export function Roadmap({ data }) {
    if (!data || (!data.roadmap && !data.phases)) return null;

    // Normalize data structure
    let phasesData = {};
    const sourceRoot = data.roadmap?.phases ? data.roadmap.phases : data.roadmap;

    if (sourceRoot) {
        phasesData = sourceRoot;
    }

    return (
        <section className="space-y-12">
            <div className="space-y-2 text-center max-w-3xl mx-auto">
                <h2 className="text-3xl font-bold tracking-tight text-black">"Next Best Action" Roadmap</h2>
                <p className="text-muted-foreground text-lg">Your personalized 3-phase transformation pathway.</p>
            </div>

            {/* Timeline Container */}
            <div className="relative">
                {/* Continuous Vertical Line - Desktop Only */}
                <div className="hidden md:block absolute top-0 bottom-0 w-0.5 -ml-px bg-gradient-to-b from-blue-200 via-indigo-200 to-purple-200 left-[calc(40%+80px)]" />

                <div className="space-y-16">
                    {PHASES.map((phaseDef, idx) => {
                        // Data Retrieval Logic
                        let phaseContent = phasesData[phaseDef.key];
                        if (!phaseContent) {
                            const matchingKey = Object.keys(phasesData).find(k => k.toLowerCase().includes(phaseDef.key.replace('_', ' ')));
                            if (matchingKey) phaseContent = phasesData[matchingKey];
                        }
                        const recommendations = phaseContent?.recommendations || (Array.isArray(phaseContent) ? phaseContent : []);

                        return (
                            <div key={phaseDef.key} className="relative grid grid-cols-1 md:grid-cols-[40%_auto_1fr] gap-8 md:gap-12 items-start">

                                {/* 1. Left Column: Phase Info (Aligned Right on Desktop) */}
                                <div className="md:text-right md:sticky md:top-24 pt-4">
                                    <div className={cn("block w-full text-left md:text-right rounded-2xl border p-6 shadow-sm transition-all bg-white relative overflow-hidden",
                                        `border-l-4 ${phaseDef.borderColor} border-y-slate-100 border-r-slate-100`
                                    )}>
                                        <div className={cn("absolute top-0 right-0 w-32 h-32 bg-gradient-to-br opacity-10 rounded-full -mr-16 -mt-16 pointer-events-none",
                                            `${phaseDef.gradientFrom} to-transparent`
                                        )} />

                                        <h3 className={cn("text-2xl font-bold tracking-tight mb-2 relative z-10", phaseDef.titleStyle)}>
                                            {phaseDef.title}
                                        </h3>

                                        <p className="text-slate-600 leading-relaxed md:ml-auto font-medium relative z-10">
                                            Focus on {phaseDef.title.toLowerCase()} activities to build momentum and establish core capabilities.
                                        </p>
                                    </div>
                                </div>

                                {/* 2. Center Column: Step Indicator */}
                                <div className="relative flex justify-center z-10 my-4 md:my-0">
                                    <div className={cn(
                                        "w-16 h-16 rounded-full border-4 border-white shadow-lg flex items-center justify-center text-xl font-bold ring-4",
                                        phaseDef.stepStyle
                                    )}>
                                        {phaseDef.step}
                                    </div>
                                </div>

                                {/* 3. Right Column: Recommendations */}
                                <div className="space-y-4">
                                    {recommendations.length > 0 ? (
                                        recommendations.map((rec, rIdx) => {
                                            const type = getRecommendationType(rec);
                                            const Icon = type.icon;

                                            return (
                                                <Card key={rIdx} className="border-slate-200 shadow-sm hover:shadow-md transition-all duration-200 group">
                                                    <CardHeader className="pb-3 p-5">
                                                        <div className="flex justify-between items-start gap-2 mb-3">
                                                            <Badge variant={type.variant} className={cn("text-[10px] px-2 py-0.5 h-5",
                                                                type.label === 'Must-Win Battle' ? "bg-red-100 text-red-700 hover:bg-red-200 border-red-200" :
                                                                    type.label === 'Peer Opportunity' ? "bg-blue-100 text-blue-700 hover:bg-blue-200 border-blue-200" : "",
                                                                type.className // Apply custom class from helper
                                                            )}>
                                                                <div className="flex items-center gap-1.5">
                                                                    <Icon className="w-3 h-3" />
                                                                    {type.label}
                                                                </div>
                                                            </Badge>
                                                            {rec.impact_score && (
                                                                <span className="text-[10px] font-mono font-medium text-slate-400 bg-slate-50 px-1.5 py-0.5 rounded">
                                                                    Score: {rec.impact_score.toFixed(1)}
                                                                </span>
                                                            )}
                                                        </div>
                                                        <CardTitle className="text-base font-bold text-slate-800 leading-tight">
                                                            {rec.theme || "Action Item"}
                                                        </CardTitle>
                                                        {rec.dimension && (
                                                            <CardDescription className="text-xs text-slate-500 mt-1 line-clamp-1">
                                                                {rec.dimension}
                                                            </CardDescription>
                                                        )}
                                                    </CardHeader>
                                                    <CardContent className="p-5 pt-0">
                                                        {(() => {
                                                            // Custom parser for the specific ML output format
                                                            // Format: "**Analysis**: Text... \n - **Action 1**: Text... \n - **Action 2**: Text..."
                                                            const parts = rec.explanation.split('\n').filter(line => line.trim().length > 0);
                                                            const analysisLine = parts.find(p => p.toLowerCase().includes('analysis')) || parts[0];
                                                            const actionLines = parts.filter(p => p.toLowerCase().includes('action'));

                                                            const analysisText = analysisLine
                                                                ? analysisLine.replace(/\*\*(.*?)\*\*/g, '').replace(/^:/, '').trim() // Strip **Analysis** prefix
                                                                : "";

                                                            return (
                                                                <div className="space-y-4">
                                                                    {/* Analysis Section */}
                                                                    <div className="text-sm text-slate-600 leading-relaxed">
                                                                        <span className="font-semibold text-slate-800">Analysis: </span>
                                                                        {analysisText.replace(/^Analysis:\s*/i, '')}
                                                                    </div>

                                                                    {/* Actions List */}
                                                                    {actionLines.length > 0 && (
                                                                        <div className="space-y-2 mt-3">
                                                                            {actionLines.map((action, i) => {
                                                                                // Strip formatting like "- **Action 1**: "
                                                                                const cleanAction = action
                                                                                    .replace(/^-/, '')
                                                                                    .replace(/\*\*(.*?)\*\*/g, '')
                                                                                    .replace(/^:/, '')
                                                                                    .trim();

                                                                                return (
                                                                                    <div key={i} className="flex gap-3 items-start p-2.5 bg-slate-50 rounded-lg border border-slate-100">
                                                                                        <div className="mt-0.5 shrink-0 w-5 h-5 rounded-full bg-white border border-slate-200 flex items-center justify-center shadow-sm">
                                                                                            <ArrowRight className="w-3 h-3 text-primary" />
                                                                                        </div>
                                                                                        <div className="text-sm text-slate-700">
                                                                                            <span className="font-semibold text-slate-900 text-xs uppercase tracking-wide mr-2">
                                                                                                Action {i + 1}:
                                                                                            </span>
                                                                                            {cleanAction.replace(/^Action \d+:\s*/i, '')}
                                                                                        </div>
                                                                                    </div>
                                                                                );
                                                                            })}
                                                                        </div>
                                                                    )}
                                                                </div>
                                                            );
                                                        })()}
                                                    </CardContent>
                                                </Card>
                                            );
                                        })
                                    ) : (
                                        <div className="p-8 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50/50 text-center">
                                            <p className="text-slate-400 text-sm italic">No critical actions identified for this phase.</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Footer */}
            <div className="mt-12 p-6 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row items-center gap-6 md:gap-8 text-center md:text-left hover:shadow-md transition-shadow duration-300">
                <div className="p-3 bg-emerald-50 rounded-xl shadow-sm shrink-0 border border-emerald-100">
                    <CheckCircle2 className="w-6 h-6 text-emerald-600" />
                </div>
                <div>
                    <h4 className="text-base text-slate-900">Why this roadmap?</h4>
                    <p className="text-sm text-slate-600 mt-1 leading-relaxed">
                        This plan is dynamically generated by comparing your profile against industry peer benchmarks. Phase 1 focuses on closing structural gaps blocking scalability, while Phases 2 & 3 target differentiation and leadership capabilities.
                    </p>
                </div>
            </div>

            <div className="mt-8 flex justify-center pb-8">
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-50 border border-slate-200 text-xs text-slate-500 shadow-sm">
                    <AlertCircle className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                    <p>
                        <strong>AI Transparency & Liability:</strong> This automated assessment utilizes K-Means Clustering and Generative AI to generate insights. Results are probabilistic and should be verified. Use of this tool does not create a professional client relationship or constitute legal advice.
                    </p>
                </div>
            </div>
        </section>
    );
}
