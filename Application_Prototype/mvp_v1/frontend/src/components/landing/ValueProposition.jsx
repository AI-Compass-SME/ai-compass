import React from 'react';
import { FlipCard } from './FlipCard';
import { BarChart3, Users, TrendingUp, Shield, Target, Lightbulb } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export function ValueProposition() {
    const { t } = useTranslation();
    const cards = [
        {
            title: t('landing.value.cards.1.title'),
            icon: BarChart3,
            what: t('landing.value.cards.1.what'),
            why: t('landing.value.cards.1.why'),
        },
        {
            title: t('landing.value.cards.2.title'),
            icon: TrendingUp,
            what: t('landing.value.cards.2.what'),
            why: t('landing.value.cards.2.why'),
        },
        {
            title: t('landing.value.cards.3.title'),
            icon: Users,
            what: t('landing.value.cards.3.what'),
            why: t('landing.value.cards.3.why'),
        },
        {
            title: t('landing.value.cards.4.title'),
            icon: Shield,
            what: t('landing.value.cards.4.what'),
            why: t('landing.value.cards.4.why'),
        },
        {
            title: t('landing.value.cards.5.title'),
            icon: Target,
            what: t('landing.value.cards.5.what'),
            why: t('landing.value.cards.5.why'),
        },
        {
            title: t('landing.value.cards.6.title'),
            icon: Lightbulb,
            what: t('landing.value.cards.6.what'),
            why: t('landing.value.cards.6.why'),
        },
    ];

    return (
        <section id="benefits" className="py-8 px-4 bg-gray-50">
            <div className="max-w-[80rem] mx-auto">
                <div className="text-center mb-4">
                    <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                        {t('landing.value.title')}
                    </h2>
                    <p className="text-sm text-gray-600 max-w-4xl mx-auto">
                        {t('landing.value.subtitle')}
                    </p>
                </div>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-2">
                    {cards.map((card, index) => (
                        <FlipCard
                            key={index}
                            title={card.title}
                            icon={card.icon}
                            what={card.what}
                            why={card.why}
                            index={index}
                        />
                    ))}
                </div>
            </div>
        </section>
    );
}
