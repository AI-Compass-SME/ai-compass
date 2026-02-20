import React, { useEffect } from 'react';
import { Compass } from 'lucide-react';
import { PageBackground } from '@/components/ui/PageBackground';

export default function ComingSoonPage() {
    useEffect(() => {
        document.title = "Coming Soon | AI Compass";
    }, []);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />

            <main className="flex-grow flex items-center justify-center relative z-10 px-6 pt-10">
                <div className="max-w-3xl mx-auto text-center flex flex-col items-center">
                    {/* Centered Logo */}
                    <div className="flex items-center gap-3 mb-8">
                        <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2.5 rounded-xl shadow-sm">
                            <Compass className="w-8 h-8 text-white" />
                        </div>
                        <span className="text-3xl font-bold tracking-tight text-gray-900">AI Compass</span>
                    </div>

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
                </div>
            </main>
        </div>
    );
}
