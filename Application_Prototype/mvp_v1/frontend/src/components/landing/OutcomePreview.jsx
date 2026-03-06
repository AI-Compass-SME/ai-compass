import React from 'react';
import { motion } from 'framer-motion';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts';
import { Award, TrendingUp, Target, Zap } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export function OutcomePreview() {
    const { t } = useTranslation();
    const radarData = [
        { subject: t('landing.outcome.subjects.strategy'), value: 4, fullMark: 5 },
        { subject: t('landing.outcome.subjects.people'), value: 3, fullMark: 5 },
        { subject: t('landing.outcome.subjects.data'), value: 3.5, fullMark: 5 },
        { subject: t('landing.outcome.subjects.useCases'), value: 4.5, fullMark: 5 },
        { subject: t('landing.outcome.subjects.processes'), value: 2.5, fullMark: 5 },
        { subject: t('landing.outcome.subjects.compliance'), value: 3, fullMark: 5 },
        { subject: t('landing.outcome.subjects.tech'), value: 4, fullMark: 5 },
    ];

    const outcomes = [
        {
            icon: Award,
            title: t('landing.outcome.items.1.title'),
            description: t('landing.outcome.items.1.desc'),
        },
        {
            icon: TrendingUp,
            title: t('landing.outcome.items.2.title'),
            description: t('landing.outcome.items.2.desc'),
        },
        {
            icon: Target,
            title: t('landing.outcome.items.3.title'),
            description: t('landing.outcome.items.3.desc'),
        },
        {
            icon: Zap,
            title: t('landing.outcome.items.4.title'),
            description: t('landing.outcome.items.4.desc'),
        },
    ];

    return (
        <section className="py-10 px-6 bg-gradient-to-br from-gray-50 to-blue-50">
            <div className="max-w-[80rem] mx-auto">
                <div className="text-center mb-8">
                    <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">{t('landing.outcome.title')}</h2>
                    <p className="text-lg text-gray-600">{t('landing.outcome.subtitle')}</p>
                </div>

                <div className="grid lg:grid-cols-2 gap-8 items-center">
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        whileInView={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.6 }}
                        viewport={{ once: true }}
                        className="bg-white rounded-2xl shadow-xl p-6"
                    >
                        <h3 className="text-xl font-semibold text-gray-900 mb-4 text-center">
                            {t('landing.outcome.radarTitle')}
                        </h3>
                        <div className="h-[260px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <RadarChart data={radarData}>
                                    <PolarGrid stroke="#e5e7eb" />
                                    <PolarAngleAxis dataKey="subject" tick={{ fill: '#6b7280', fontSize: 13 }} />
                                    <PolarRadiusAxis angle={90} domain={[0, 5]} tick={{ fill: '#9ca3af', fontSize: 11 }} />
                                    <Radar
                                        name={t('landing.outcome.radarLabel')}
                                        dataKey="value"
                                        stroke="#3b82f6"
                                        fill="#3b82f6"
                                        fillOpacity={0.6}
                                    />
                                </RadarChart>
                            </ResponsiveContainer>
                        </div>
                    </motion.div>

                    <div className="space-y-3">
                        {outcomes.map((outcome, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, x: 20 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.5, delay: index * 0.1 }}
                                viewport={{ once: true }}
                                className="flex gap-4 bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow items-center"
                            >
                                <div className="flex-shrink-0">
                                    <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                                        <outcome.icon className="w-5 h-5 text-white" />
                                    </div>
                                </div>
                                <div>
                                    <h4 className="font-semibold text-gray-900 text-sm mb-0.5">{outcome.title}</h4>
                                    <p className="text-gray-600 text-xs">{outcome.description}</p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
