import React from 'react';
import { motion } from 'framer-motion';
import { ClipboardList, Sparkles, Map } from 'lucide-react';

export function ProcessSection() {
    const steps = [
        {
            number: '01',
            title: 'Guided Assessment',
            description: '27 questions covering 7 key dimensions (Strategy, People, Data, Use Cases, Processes, Compliance, and Tech Infrastructure).',
            icon: ClipboardList,
        },
        {
            number: '02',
            title: 'Instant Analysis',
            description: 'Our AI supported algorithm identifies your unique Company Cluster Profile and your current potential.',
            icon: Sparkles,
        },
        {
            number: '03',
            title: 'Growth Roadmap',
            description: 'Receive custom recommendations to move from your current level to the next.',
            icon: Map,
        },
    ];

    return (
        <section id="how-it-works" className="py-10 px-6 bg-white">
            <div className="max-w-[80rem] mx-auto">
                <div className="text-center mb-8">
                    <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">The Process</h2>
                    <p className="text-xl text-gray-600">Three simple steps to your AI roadmap</p>
                </div>

                <div className="relative">
                    {/* Connection Line */}
                    <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-blue-200 via-purple-200 to-blue-200 -translate-y-1/2 z-0"></div>

                    <div className="grid md:grid-cols-3 gap-8 relative z-10">
                        {steps.map((step, index) => (
                            <motion.div
                                key={index}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.5, delay: index * 0.2 }}
                                viewport={{ once: true }}
                                className="relative"
                            >
                                <div className={`bg-white border-2 border-gray-200 rounded-xl p-6 hover:border-blue-600 transition-colors hover:shadow-xl ${index === 0 ? 'h-[300px]' : index === 1 ? 'h-[270px]' : 'h-[240px]'
                                    }`}>
                                    <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full mb-4 mx-auto">
                                        <step.icon className="w-6 h-6 text-white" />
                                    </div>
                                    <div className="text-center">
                                        <div className="text-4xl font-bold text-gray-200 mb-2">{step.number}</div>
                                        <h3 className="text-lg font-semibold text-gray-900 mb-2">{step.title}</h3>
                                        <p className="text-gray-600 leading-relaxed text-sm">{step.description}</p>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
