import React from 'react';
import { FlipCard } from './FlipCard';
import { BarChart3, Users, TrendingUp, Shield, Target, Lightbulb } from 'lucide-react';

export function ValueProposition() {
    const cards = [
        {
            title: 'Assess Your Current AI Maturity Level',
            icon: BarChart3,
            what: 'A comprehensive multi-dimensional audit that evaluates your organization across 7 core pillars: Strategy, People, Data, Use Cases, Processes, Compliance, and Tech Infrastructure.',
            why: 'You cannot improve what you do not measure. By establishing an objective baseline, you move away from guesswork and gain a scientific understanding of your organization\'s actual readiness.',
        },
        {
            title: 'Benchmarking Beyond the Hype',
            icon: TrendingUp,
            what: 'A comparative analysis that measures your digital capabilities against a verified database of 500+ peer companies and industry leaders.',
            why: 'Strategic positioning is relative. Benchmarking tells you if you are truly leading your industry or if competitors are gaining a technological advantage that will be difficult to close later.',
        },
        {
            title: 'Bridging the Human-Tech Divide',
            icon: Users,
            what: 'An evaluation of organizational culture, employee mindset, and internal AI literacy levels.',
            why: 'Technology only scales as fast as your people. Identifying psychological resistance or skill gaps early ensures your culture supports your technical transformation instead of blocking it.',
        },
        {
            title: 'Risk & Compliance Safeguard',
            icon: Shield,
            what: 'A proactive audit of your alignment with emerging standards, such as the EU AI Act, and internal data ethics protocols.',
            why: 'Moving fast is important, but moving safely is vital. This safeguard protects your company\'s reputation and future-proofs your operations against shifting legal landscapes.',
        },
        {
            title: 'Identify Gaps and Opportunities',
            icon: Target,
            what: 'A precise gap-analysis tool that reveals hidden weaknesses in your digital foundation while highlighting untapped areas for innovation.',
            why: 'To reach the next maturity level, you must know exactly what is holding you back. Pinpointing these "friction points" allows you to fix the foundation while simultaneously seizing "low-hanging fruit."',
        },
        {
            title: 'Prioritized Strategic Advisory',
            icon: Lightbulb,
            what: 'A structured advisory module that translates your maturity gaps into a prioritized sequence of strategic topics and focus areas (e.g., "Data Foundation" before "Customer-facing AI").',
            why: 'SMEs often suffer from "pilot fatigue" by trying to do everything at once. This advisory ensures that you tackle the right topics in the right order, focusing resources on the thematic areas that will resolve your specific business bottlenecks most effectively.',
        },
    ];

    return (
        <section id="benefits" className="py-8 px-4 bg-gray-50">
            <div className="max-w-[80rem] mx-auto">
                <div className="text-center mb-4">
                    <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                        The Value Proposition
                    </h2>
                    <p className="text-sm text-gray-600 max-w-4xl mx-auto">
                        AI is not a tool you buy; it is a capability you build. The AI Compass is a professional consulting tool designed to provide the diagnostic clarity needed to ensure your investment leads to growth, not just expense.
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
