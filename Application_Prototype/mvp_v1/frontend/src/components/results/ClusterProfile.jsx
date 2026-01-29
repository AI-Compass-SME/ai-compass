import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

// Static definitions from spec 8.2
const CLUSTER_DEFINITIONS = [
    {
        id: 1,
        name: "The Traditionalist",
        height: "20%",
        description: "AI is not yet a topic of discussion. Operations are predominantly manual, data is siloed or analog, and there is often significant cultural skepticism."
    },
    {
        id: 2,
        name: "The Experimental Explorer",
        height: "40%",
        description: "The organization has started \"playing\" with AI through isolated tools like ChatGPT. There is curiosity but no formal strategy or oversight."
    },
    {
        id: 3,
        name: "The Structured Builder",
        height: "60%",
        description: "A solid technical and strategic foundation is being laid. High-level roadmaps and cloud infrastructure are in place, but scaling remains difficult."
    },
    {
        id: 4,
        name: "The Operational Scaler",
        height: "80%",
        description: "AI is delivering measurable ROI. Leadership is aligned, and the organization is moving multiple use cases into production."
    },
    {
        id: 5,
        name: "The AI-Driven Leader",
        height: "100%",
        description: "AI is a core strategic pillar. The workforce is highly literate, data flows are automated, and the company sets industry standards."
    }
];

export function ClusterProfile({ data }) {
    if (!data || !data.cluster) return null;

    const activeClusterId = data.cluster.cluster_id || 0;
    const activeClusterName = (data.cluster.cluster_name || "Unknown").replace(/^\d+\s*-\s*/, '');

    return (
        <section className="space-y-8 relative">
            <div className="absolute inset-0 bg-slate-50/50 -skew-y-1 transform rounded-3xl -z-10" />
            <div className="space-y-4 text-center max-w-3xl mx-auto mb-16">
                <h2 className="text-3xl font-bold tracking-tight text-slate-900">
                    <span className="font-normal text-slate-600">Your Cluster Profile:</span> <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">{activeClusterName}</span>
                </h2>
                <p className="text-slate-600 text-lg leading-relaxed">
                    A data-driven synthesis of your company's AI maturity level.
                </p>
            </div>

            <Card className="border-none shadow-none bg-transparent">
                <CardContent className="p-0 space-y-4">
                    {/* Combined Visualization Area */}
                    <div className="relative">
                        {/* Y-Axis Label */}
                        <div className="absolute left-0 top-0 bottom-32 -translate-x-full pr-4 flex items-center justify-center">
                            <span className="text-xs font-bold text-slate-400 -rotate-90 whitespace-nowrap tracking-wider uppercase">Value Growth</span>
                        </div>

                        {/* Chart Grid */}
                        <div className="grid grid-cols-5 gap-2 md:gap-4 h-[320px] items-end px-2 md:px-0 border-b border-slate-200 pb-0">
                            {CLUSTER_DEFINITIONS.map((cluster) => {
                                const isActive = cluster.id === activeClusterId;
                                return (
                                    <div key={cluster.id} className="flex flex-col items-center justify-end h-full gap-0 group relative">
                                        {isActive && (
                                            <div
                                                className="absolute bg-slate-900 text-white text-[10px] md:text-xs font-bold px-2 md:px-3 py-1 md:py-1.5 rounded-full shadow-lg animate-bounce z-10 whitespace-nowrap"
                                                style={{ bottom: `calc(${cluster.height} + 16px)` }}
                                            >
                                                You are here
                                            </div>
                                        )}
                                        <div
                                            className={cn(
                                                "w-full rounded-t-lg transition-all duration-700 ease-out relative overflow-hidden",
                                                isActive
                                                    ? "bg-gradient-to-t from-blue-600 via-indigo-600 to-purple-600 shadow-lg shadow-indigo-200"
                                                    : "bg-slate-200 group-hover:bg-slate-300"
                                            )}
                                            style={{ height: cluster.height }}
                                        >
                                            {isActive && <div className="absolute inset-0 bg-white/20 animate-pulse" />}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>

                        {/* X-Axis Description Cards (Aligned perfectly under bars via same grid) */}
                        <div className="grid grid-cols-5 gap-2 md:gap-4 mt-4 px-2 md:px-0">
                            {CLUSTER_DEFINITIONS.map((cluster) => {
                                const isActive = cluster.id === activeClusterId;
                                return (
                                    <div
                                        key={cluster.id}
                                        className={cn(
                                            "p-2 md:p-3 rounded-xl border transition-all duration-300 relative overflow-hidden flex flex-col",
                                            isActive
                                                ? "border-indigo-500 bg-white ring-2 ring-indigo-50 shadow-md z-10 scale-[1.02]"
                                                : "border-slate-100 bg-white/50 hover:border-slate-200 hover:bg-white"
                                        )}
                                    >
                                        <h4 className={cn(
                                            "font-bold mb-1 md:mb-2 text-[10px] md:text-xs leading-tight",
                                            isActive ? "text-indigo-700" : "text-slate-700"
                                        )}>
                                            {cluster.name}
                                        </h4>
                                        <p className="hidden md:block text-[10px] text-slate-500 leading-tight font-medium">
                                            {cluster.description}
                                        </p>
                                    </div>
                                );
                            })}
                        </div>

                        {/* X-Axis Label */}
                        <div className="mt-6 text-center">
                            <span className="text-xs font-bold text-slate-400 tracking-wider uppercase">AI Maturity</span>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </section>
    );
}
