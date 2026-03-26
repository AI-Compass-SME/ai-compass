import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { AlertTriangle, AlertOctagon, TrendingDown, ArrowRight, Zap, Target, Quote } from 'lucide-react';
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { useTranslation } from 'react-i18next';

export function GapAnalysis({ data }) {
    const { t, i18n } = useTranslation();
    if (!data || !data.strategic_gaps) return null;

    const DE_DIM_MAP = {
        'Strategy & Business Vision': 'Strategie & Geschäftsvision',
        'People & Culture': 'Mensch & Kultur',
        'Data Readiness & Literacy': 'Datenreife & -kompetenz',
        'Use Cases & Business Value': 'Use Cases & Business Value',
        'Processes & Scaling': 'Prozesse & Skalierung',
        'Governance & Compliance': 'Governance & Compliance',
        'Tech Infrastructure': 'Technische Infrastruktur',
    };

    const getDimName = (gap) => {
        if (i18n.language === 'de') {
            return gap.dimension_name_de || DE_DIM_MAP[gap.dimension_name] || gap.dimension_name;
        }
        return gap.dimension_name;
    };

    const gaps = data.strategic_gaps;
    const briefing = data.executive_briefing;

    // Helper for briefing text
    const formatBriefing = (text) => {
        if (!text) return "";
        let html = text
            .replace(/### (.*?)\n/g, '<h3 class="text-xl font-bold text-primary mb-6 flex items-center gap-2">$1</h3>')
            .replace(/\*\*(.*?)\*\*/g, '<strong class="text-slate-800 font-bold">$1</strong>')
            .split('\n\n')
            .map(para => {
                if (para.startsWith('<h3')) return para;
                return `<p class="mb-4 last:mb-0">${para.replace(/\n/g, '<br/>')}</p>`;
            })
            .join('');
        return html;
    };

    // Helper to determine gap visuals
    const getGapVisuals = (gap) => {
        const type = (gap.type || "").toLowerCase();

        if (type.includes('anomaly') || type.includes('structural')) {
            return {
                icon: AlertOctagon,
                colorClass: "text-amber-600",
                bgClass: "bg-amber-50 border-amber-200",
                gradient: "from-amber-500/10 to-transparent",
                label: t('results.gaps.structuralRisk')
            };
        } else {
            return {
                icon: TrendingDown,
                colorClass: "text-red-600",
                bgClass: "bg-red-50 border-red-200",
                gradient: "from-red-500/10 to-transparent",
                label: t('results.gaps.criticalWeakness')
            };
        }
    };

    return (
        <section className="space-y-8">
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div className="space-y-2">
                    <h2 className="text-3xl font-bold tracking-tight text-slate-800">{t('results.gaps.title')}</h2>
                    <p className="text-muted-foreground text-lg">{t('results.gaps.subtitle')}</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Executive Briefing Card - Merged */}
                {briefing && (
                    <Card className="col-span-full glass-premium overflow-hidden border-none relative shadow-md">
                        {/* Decorative background gradients for premium feel */}
                        <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-50/50 rounded-full -mr-48 -mt-48 blur-3xl pointer-events-none" />
                        <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-50/50 rounded-full -ml-32 -mb-32 blur-3xl pointer-events-none" />

                        <CardContent className="p-8 md:p-12 relative">
                            <div className="flex flex-col md:flex-row gap-8 items-start">
                                {/* Designer Quote Icon */}
                                <div className="hidden md:flex p-4 rounded-2xl bg-primary/5 text-primary/40 shrink-0 mt-2 border border-primary/10">
                                    <Quote className="w-10 h-10 rotate-180" />
                                </div>

                                <div className="flex-1">
                                    <h3 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">{t('results.briefing.title')}</h3>
                                    <div
                                        className="text-slate-600 leading-relaxed text-lg font-medium"
                                        dangerouslySetInnerHTML={{ __html: formatBriefing(briefing) }}
                                    />

                                    {/* Decorative line */}
                                    <div className="mt-8 pt-8 border-t border-slate-100 flex items-center justify-between">
                                        <span className="text-xs font-bold uppercase tracking-widest text-slate-400">{t('results.briefing.teamLabel')}</span>
                                        <div className="flex gap-1">
                                            {[1, 2, 3].map(i => (
                                                <div key={i} className="w-1.5 h-1.5 rounded-full bg-primary/20" />
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                )}

                {gaps.map((gap, idx) => {
                    const visuals = getGapVisuals(gap);
                    const Icon = visuals.icon;

                    return (
                        <Card key={idx} className="relative overflow-hidden border-slate-200 shadow-sm hover:shadow-md transition-all duration-300 group">
                            {/* Decorative Background Gradient */}
                            <div className={cn("absolute top-0 right-0 w-64 h-64 bg-gradient-to-br blur-3xl opacity-50 rounded-full -mr-16 -mt-16 pointer-events-none", visuals.gradient)} />

                            <CardHeader className="pb-4 relative">
                                <div className="flex items-start justify-between gap-4">
                                    <div className="flex items-start gap-3">
                                        <div className={cn("p-2.5 rounded-xl border shrink-0 mt-1", visuals.bgClass)}>
                                            <Icon className={cn("w-6 h-6", visuals.colorClass)} />
                                        </div>
                                        <div>
                                            <Badge variant="outline" className={cn("mb-2 font-semibold tracking-wide border-0 px-0", visuals.colorClass)}>
                                                {visuals.label}
                                            </Badge>
                                            <CardTitle className="text-xl font-bold text-slate-800 leading-snug">
                                                {gap.title.replace(/^(Critical Gap|Structural Imbalance):\s*/i, '')}
                                            </CardTitle>
                                        </div>
                                    </div>

                                    {/* Score Indicator */}
                                    <div className="flex flex-col items-end shrink-0">
                                        <div className="text-2xl font-bold text-slate-700">
                                            {gap.score ? gap.score.toFixed(1) : "N/A"}
                                        </div>
                                        <span className="text-[10px] items-center text-muted-foreground uppercase tracking-wider font-semibold">
                                            {t('results.gaps.impactScore')}
                                        </span>
                                    </div>
                                </div>
                            </CardHeader>

                            <CardContent className="space-y-6 relative">
                                {/* Context / Finding */}
                                <div className="text-slate-600 leading-relaxed text-base">
                                    {gap.context}
                                </div>

                                {/* Strategic Risk Warning Box */}
                                {gap.strategic_risk && (
                                    <div className="bg-slate-50 rounded-lg p-4 border border-slate-100 relative group-hover:border-slate-200 transition-colors">
                                        <div className="flex items-center gap-2 mb-2 text-slate-800">
                                            <Zap className="w-4 h-4 text-amber-500 fill-amber-500" />
                                            <h4 className="text-sm font-bold uppercase tracking-wide">{t('results.gaps.strategicImplication')}</h4>
                                        </div>
                                        <p className="text-sm text-slate-600 leading-relaxed italic">
                                            "{gap.strategic_risk}"
                                        </p>
                                    </div>
                                )}

                                {/* Bottom Meta Data */}
                                <div className="flex items-center gap-2 pt-2 text-xs font-medium text-slate-400">
                                    <Target className="w-3.5 h-3.5" />
                                    <span>{t('results.gaps.affects')}: {getDimName(gap) || gap.source_dim || t('results.gaps.generalCapability')}</span>
                                </div>
                            </CardContent>
                        </Card>
                    );
                })}

                {gaps.length === 0 && (
                    <div className="col-span-full py-12 text-center border-2 border-dashed border-slate-100 rounded-xl bg-slate-50/50">
                        <div className="p-4 bg-white rounded-full w-fit mx-auto shadow-sm mb-4">
                            <AlertTriangle className="w-8 h-8 text-slate-300" />
                        </div>
                        <h3 className="text-lg font-semibold text-slate-600">{t('results.gaps.noGaps')}</h3>
                        <p className="text-slate-400 max-w-sm mx-auto mt-1">{t('results.gaps.noGapsDesc')}</p>
                    </div>
                )}
            </div>
        </section>
    );
}
