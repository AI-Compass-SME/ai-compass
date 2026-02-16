import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';

export default function ImprintPage() {
    useEffect(() => {
        document.title = "Imprint | AI Compass";
    }, []);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-6 pt-28 pb-16 relative z-10">

                <PageHeader
                    title="Imprint"
                    subtitle="LEGAL INFORMATION"
                />

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 md:p-12">
                    <div className="grid md:grid-cols-2 gap-x-12 gap-y-6 text-sm text-gray-700">
                        <section>
                            <h2 className="text-sm font-bold text-gray-900 mb-1 uppercase tracking-wide text-xs">Information according to § 5 DDG</h2>
                            <p className="leading-relaxed">
                                Christian Miething<br />
                                Görschstrasse 10A<br />
                                13187 Berlin, Germany
                            </p>
                        </section>

                        <section>
                            <h2 className="text-sm font-bold text-gray-900 mb-1 uppercase tracking-wide text-xs">Contact</h2>
                            <p className="leading-relaxed">
                                Phone: TBD<br />
                                Email: chris@the-ai-compass.io<br />
                                Website: www.the-ai-compass.io
                            </p>
                        </section>

                        <section>
                            <h2 className="text-sm font-bold text-gray-900 mb-1 uppercase tracking-wide text-xs">Responsible for content (§ 18 MStV)</h2>
                            <p className="leading-relaxed">
                                Christian Miething<br />
                                Görschstrasse 10A<br />
                                13187 Berlin, Germany
                            </p>
                        </section>

                        <section>
                            <h2 className="text-sm font-bold text-gray-900 mb-1 uppercase tracking-wide text-xs">EU Dispute Resolution</h2>
                            <p className="leading-relaxed">
                                The European Commission provides a platform for online dispute resolution (ODR):{' '}
                                <a href="https://consumer-redress.ec.europa.eu/index_de" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                                    ec.europa.eu/consumers/odr
                                </a>.
                            </p>
                        </section>

                        <section className="md:col-span-2">
                            <h2 className="text-sm font-bold text-gray-900 mb-1 uppercase tracking-wide text-xs">Consumer dispute resolution</h2>
                            <p className="leading-relaxed">
                                We are not willing or obliged to participate in dispute resolution proceedings before a consumer arbitration board.
                            </p>
                        </section>

                        <section className="md:col-span-2 bg-gray-50 p-4 rounded-lg border border-gray-200 mt-2">
                            <h2 className="text-xs font-bold text-gray-900 mb-1 uppercase tracking-wide">
                                Disclaimer for AI-Generated Content
                            </h2>
                            <p className="text-xs text-gray-600 leading-relaxed">
                                The "AI Compass" uses automated machine learning models (specifically K-Means Clustering and k-Nearest Neighbors) to analyze data.
                                The results, maturity scores, and roadmaps provided are for informational and orientation purposes only. They do not constitute professional business, legal, or strategic consulting.
                                The operator assumes no liability for business decisions made based on the generated output.
                            </p>
                        </section>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}
