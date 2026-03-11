import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { useTranslation, Trans } from 'react-i18next';

// Base structural configurations (static height maps)
const CLUSTER_STRUCTURE = [
    { id: 1, height: "20%" },
    { id: 2, height: "40%" },
    { id: 3, height: "60%" },
    { id: 4, height: "80%" },
    { id: 5, height: "100%" }
];

export function ClusterProfile({ data }) {
    const { t } = useTranslation();
    if (!data || !data.cluster) return null;

    const activeClusterId = data.cluster.cluster_id || 0;

    // We get the localized active generic name from our own dict rather than using the raw DB string to ensure language match
    const activeClusterName = activeClusterId > 0 && activeClusterId <= 5
        ? t(`results.cluster.definitions.${activeClusterId}.name`)
        : (data.cluster.cluster_name || "Unknown").replace(/^\d+\s*-\s*/, '');

    const activeLevelOrdinal = activeClusterId > 0 && activeClusterId <= 5
        ? t(`results.cluster.definitions.${activeClusterId}.ordinal`)
        : "";

    const activeClusterGrammar = activeClusterId > 0 && activeClusterId <= 5
        ? t(`results.cluster.definitions.${activeClusterId}.grammar`)
        : activeClusterName;

    return (
        <section className="space-y-8 relative">
            <div className="absolute inset-0 bg-slate-50/50 -skew-y-1 transform rounded-3xl -z-10" />
            <div className="space-y-4 text-center max-w-5xl mx-auto mb-6 md:mb-8 pt-16 md:pt-24">
                <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-slate-800">
                    {t('results.cluster.title', { clusterName: activeClusterName })}
                </h2>
                <p className="text-lg text-muted-foreground leading-relaxed">
                    {t('results.cluster.description', { levelOrdinal: activeLevelOrdinal, clusterGrammar: activeClusterGrammar })}
                </p>
            </div>

            <Card className="border-none shadow-none bg-transparent">
                <CardContent className="p-0 space-y-4">
                    {/* Combined Visualization Area */}
                    <div className="relative">
                        {/* Y-Axis Label */}
                        <div className="absolute top-5 -left-8 md:-left-10 z-10 w-0 h-0">
                            <div className="absolute top-0 right-0 origin-top-right -rotate-90 flex items-center gap-3 text-[10px] md:text-[11px] font-bold text-slate-400 tracking-wider uppercase whitespace-nowrap">
                                {t('results.cluster.valueGrowth')}
                                <svg width="36" height="10" viewBox="0 0 64 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="shrink-0"><path d="M58 4l6 4-6 4" /><path d="M0 8h64" /></svg>
                            </div>
                        </div>

                        {/* X-Axis Label (Inside top left) */}
                        <div className="absolute top-4 left-4 md:left-6 z-10 flex items-center gap-3 text-[10px] md:text-[11px] font-bold text-slate-400 tracking-wider uppercase">
                            {t('results.cluster.aiMaturity')}
                            <svg width="48" height="12" viewBox="0 0 64 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="shrink-0"><path d="M58 4l6 4-6 4" /><path d="M0 8h64" /></svg>
                        </div>

                        {/* Chart Grid */}
                        <div className="grid grid-cols-5 gap-2 md:gap-4 h-[320px] items-end px-2 md:px-0 border-b border-slate-200 pb-0">
                            {CLUSTER_STRUCTURE.map((cluster) => {
                                const isActive = cluster.id === activeClusterId;
                                return (
                                    <div key={cluster.id} className="flex flex-col items-center justify-end h-full gap-0 group relative">
                                        {isActive && (
                                            <div
                                                className="absolute bg-slate-900 text-white text-[10px] md:text-xs font-bold px-2 md:px-3 py-1 md:py-1.5 rounded-full shadow-lg z-10 whitespace-nowrap"
                                                style={{ bottom: `calc(${cluster.height} + 16px)` }}
                                            >
                                                {t('results.cluster.youAreHere')}
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
                            {CLUSTER_STRUCTURE.map((cluster) => {
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
                                            "font-bold mb-1 md:mb-2 text-[11px] md:text-sm leading-tight",
                                            isActive ? "text-indigo-700" : "text-slate-700"
                                        )}>
                                            {t(`results.cluster.definitions.${cluster.id}.name`)}
                                        </h4>
                                        <p className="hidden md:block text-[11px] md:text-xs text-slate-600 leading-snug font-medium">
                                            {t(`results.cluster.definitions.${cluster.id}.description`)}
                                        </p>
                                    </div>
                                );
                            })}
                        </div>

                        {/* Old X-Axis Label removed */}
                    </div>
                </CardContent>
            </Card>
        </section >
    );
}
