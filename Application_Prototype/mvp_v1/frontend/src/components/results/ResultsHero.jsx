import React from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Medal, Users, TrendingUp } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export function ResultsHero({ data }) {
    const { t } = useTranslation();
    if (!data) return null;

    const { overall_score, cluster, company } = data;
    const activeClusterId = cluster?.cluster_id || 0;
    const clusterName = activeClusterId > 0 && activeClusterId <= 5
        ? t(`results.cluster.definitions.${activeClusterId}.name`)
        : (cluster?.cluster_name || "Unknown").replace(/^\d+\s*-\s*/, '');
    const percentile = data.percentile || "N/A";
    const industry = data.percentile?.industry || company?.industry || "Industry";

    // Format score: 1 decimal place, but if integer (e.g. 5.0), show as 5
    const formattedScore = Number(overall_score) % 1 === 0 ? Number(overall_score).toFixed(0) : Number(overall_score).toFixed(1);

    return (
        <div className="section-container space-y-8">
            {/* Header Text */}
            <div className="text-center max-w-4xl mx-auto space-y-4">
                <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-black">
                    {t('results.hero.title')}
                </h1>
                <p className="text-lg text-muted-foreground leading-relaxed">
                    {t('results.hero.subtitle')}
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
                                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">{t('results.hero.score')}</p>
                            </div>
                        </div>
                        <div className="mt-6">
                            <h3 className="text-3xl font-bold text-slate-900 tracking-tight">
                                {formattedScore}<span className="text-lg text-slate-400 font-medium ml-1">/5</span>
                            </h3>
                            <p className="text-xs font-medium text-slate-500 mt-2">{t('results.hero.overallMaturity')}</p>
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
                                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">{t('results.hero.cluster')}</p>
                            </div>
                        </div>
                        <div className="mt-6">
                            <h3 className="text-xl font-bold text-slate-900 leading-tight line-clamp-2 min-h-[2rem]">
                                {clusterName}
                            </h3>
                            <p className="text-xs font-medium text-slate-500 mt-2">{t('results.hero.archetype')}</p>
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
                                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">{t('results.hero.percentile')}</p>
                            </div>
                        </div>
                        <div className="mt-6">
                            <h3 className="text-2xl font-bold text-slate-900 tracking-tight">
                                {percentile !== "N/A" ? `${t('results.hero.top')} ${percentile.percentage}%` : `${t('results.hero.top')} 35%`}
                            </h3>
                            <p className="text-xs font-medium text-slate-500 mt-2">{t('results.hero.vsPeers', { industry })}</p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
