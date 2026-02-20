import React, { useEffect } from 'react';
import { Compass, ArrowRight } from 'lucide-react';
import { PageBackground } from '@/components/ui/PageBackground';

export default function ComingSoonPage() {
    useEffect(() => {
        document.title = "Coming Soon | AI Compass";
    }, []);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />

            {/* Minimal Navigation just for the logo */}
            <nav className="absolute top-0 left-0 right-0 z-50">
                <div className="max-w-[80rem] mx-auto px-6 py-8 flex items-center justify-center md:justify-start">
                    <div className="flex items-center gap-3">
                        <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2.5 rounded-xl shadow-sm">
                            <Compass className="w-6 h-6 text-white" />
                        </div>
                        <span className="text-2xl font-bold tracking-tight text-gray-900">AI Compass</span>
                    </div>
                </div>
            </nav>

            <main className="flex-grow flex items-center justify-center relative z-10 px-6 pt-20">
                <div className="max-w-3xl mx-auto text-center">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-50/80 border border-blue-100 backdrop-blur-sm mb-8 animate-fade-in shadow-sm">
                        <span className="flex h-2 w-2 rounded-full bg-blue-600 animate-pulse"></span>
                        <span className="text-xs font-bold text-blue-900 uppercase tracking-wider">Preparing for Launch</span>
                    </div>

                    <h1 className="text-5xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-gray-900 via-slate-800 to-gray-900 tracking-tight mb-8 leading-[1.1] pb-2">
                        Something great is <br className="hidden md:block" />
                        <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">coming soon.</span>
                    </h1>

                    <p className="text-lg md:text-xl text-slate-600 mb-12 max-w-2xl mx-auto font-medium leading-relaxed">
                        We're putting the final touches on our AI maturity assessment platform.
                        The compass to your digital transformation is almost ready.
                    </p>

                    <div className="flex justify-center">
                        <a
                            href="mailto:contact@the-ai-compass.de"
                            className="inline-flex items-center justify-center gap-2 bg-slate-900 text-white px-8 py-4 rounded-xl font-bold text-base hover:bg-slate-800 transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5 active:scale-95"
                        >
                            Contact Us
                            <ArrowRight className="w-5 h-5" />
                        </a>
                    </div>
                </div>
            </main>
        </div>
    );
}
