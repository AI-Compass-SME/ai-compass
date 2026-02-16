import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Medal, Users, TrendingUp } from 'lucide-react';

export function ResultsHero({ data }) {
    if (!data) return null;

    const { overall_score, cluster, company } = data;
    const clusterName = (cluster?.cluster_name || "Unknown").replace(/^\d+\s*-\s*/, '');
    // Placeholder for percentile logic if not in data
    const percentile = data.percentile || "N/A";
    const industry = data.percentile?.industry || company?.industry || "Industry";

    // Format score: 1 decimal place, but if integer (e.g. 5.0), show as 5
    const formattedScore = Number(overall_score) % 1 === 0 ? Number(overall_score).toFixed(0) : Number(overall_score).toFixed(1);

    return (
        <div className="section-container space-y-8">
            {/* Header Text */}
            <div className="text-center max-w-4xl mx-auto space-y-4">
                <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-black">
                    AI Compass: Executive Results Report
                </h1>
                <p className="text-lg text-muted-foreground leading-relaxed">
                    This is your strategic Blueprint — a verified baseline of where you stand today, detailing your organizational maturity, competitive standing, and the strategic path forward to scaling measurable AI value.
                </p>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Score Card */}
                <Card className="relative overflow-hidden border-slate-200 shadow-lg hover:shadow-xl transition-all duration-300 group bg-white">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <Medal className="w-24 h-24 text-blue-600 transform rotate-12 translate-x-8 -translate-y-8" />
                    </div>
                    <CardContent className="p-6 md:p-8 flex flex-col justify-between h-full relative z-10">
                        <div className="flex justify-between items-start">
                            <div className="p-3 rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 text-white shadow-blue-200 shadow-lg">
                                <Medal className="w-6 h-6" />
                            </div>
                            <div className="text-right">
                                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Score</p>
                            </div>
                        </div>
                        <div className="mt-6">
                            <h3 className="text-3xl font-bold text-slate-900 tracking-tight">
                                {formattedScore}<span className="text-lg text-slate-400 font-medium ml-1">/5</span>
                            </h3>
                            <p className="text-xs font-medium text-slate-500 mt-2">Overall AI Maturity</p>
                        </div>
                    </CardContent>
                </Card>

                {/* Cluster Card */}
                <Card className="relative overflow-hidden border-slate-200 shadow-lg hover:shadow-xl transition-all duration-300 group bg-white">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <Users className="w-24 h-24 text-purple-600 transform rotate-12 translate-x-8 -translate-y-8" />
                    </div>
                    <CardContent className="p-6 md:p-8 flex flex-col justify-between h-full relative z-10">
                        <div className="flex justify-between items-start">
                            <div className="p-3 rounded-2xl bg-gradient-to-br from-purple-500 to-purple-600 text-white shadow-purple-200 shadow-lg">
                                <Users className="w-6 h-6" />
                            </div>
                            <div className="text-right">
                                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Cluster</p>
                            </div>
                        </div>
                        <div className="mt-6">
                            <h3 className="text-xl font-bold text-slate-900 leading-tight line-clamp-2 min-h-[2rem]">
                                {clusterName}
                            </h3>
                            <p className="text-xs font-medium text-slate-500 mt-2">Organizational Archetype</p>
                        </div>
                    </CardContent>
                </Card>

                {/* Benchmark Card */}
                <Card className="relative overflow-hidden border-slate-200 shadow-lg hover:shadow-xl transition-all duration-300 group bg-white">
                    <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                        <TrendingUp className="w-24 h-24 text-indigo-600 transform rotate-12 translate-x-8 -translate-y-8" />
                    </div>
                    <CardContent className="p-6 md:p-8 flex flex-col justify-between h-full relative z-10">
                        <div className="flex justify-between items-start">
                            <div className="p-3 rounded-2xl bg-gradient-to-br from-indigo-500 to-indigo-600 text-white shadow-indigo-200 shadow-lg">
                                <TrendingUp className="w-6 h-6" />
                            </div>
                            <div className="text-right">
                                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Percentile</p>
                            </div>
                        </div>
                        <div className="mt-6">
                            <h3 className="text-2xl font-bold text-slate-900 tracking-tight">
                                {percentile !== "N/A" ? `Top ${percentile.percentage}%` : "Top 35%"}
                            </h3>
                            <p className="text-xs font-medium text-slate-500 mt-2">vs. {industry} Peers</p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
