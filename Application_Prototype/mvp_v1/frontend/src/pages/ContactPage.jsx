import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';
import { Mail, Phone, MapPin, Scale, Shield } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function ContactPage() {
    useEffect(() => {
        document.title = "Contact | AI Compass";
    }, []);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-6 pt-28 pb-16 relative z-10">

                <PageHeader
                    title="Contact the AI Compass Team"
                    subtitle="DIRECT SUPPORT FOR YOUR AI TRANSFORMATION"
                />

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 md:p-12 mx-auto">

                    <div className="mb-10 text-left w-full">
                        <p className="text-lg text-gray-700 leading-relaxed">
                            We prioritize personal exchange. If you have questions regarding the AI Maturity Assessment, our Clustering Methodology, or bespoke consulting, please reach out to us directly.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-2 gap-8 md:gap-12">

                        {/* Left Column: Direct Contact */}
                        <div className="space-y-8">
                            {/* Phone */}
                            <div className="flex items-start gap-4">
                                <div className="bg-blue-50 p-3 rounded-lg text-blue-600 mt-1">
                                    <Phone className="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 className="text-base font-bold text-gray-900 mb-1">Phone</h3>
                                    <p className="text-sm font-medium text-gray-900">Main Line: <span className="text-gray-500 font-normal">+49 tbd</span></p>
                                    <p className="text-xs text-gray-500 mt-1">Available Monday – Friday, 09:00 – 18:00 (CET)</p>
                                </div>
                            </div>

                            {/* Email */}
                            <div className="flex items-start gap-4">
                                <div className="bg-purple-50 p-3 rounded-lg text-purple-600 mt-1">
                                    <Mail className="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 className="text-base font-bold text-gray-900 mb-1">E-Mail</h3>
                                    <p className="text-sm font-medium text-gray-900">Contact: <span className="text-gray-500 font-normal">tbd</span></p>
                                    <p className="text-xs text-gray-500 mt-1">We typically respond to all inquiries within one business day.</p>
                                </div>
                            </div>

                            {/* Office */}
                            <div className="flex items-start gap-4">
                                <div className="bg-emerald-50 p-3 rounded-lg text-emerald-600 mt-1">
                                    <MapPin className="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 className="text-base font-bold text-gray-900 mb-1">Office Location</h3>
                                    <p className="text-sm text-gray-600 leading-relaxed">
                                        Christian Miething<br />
                                        Görschstrasse 10A<br />
                                        13187 Berlin, Germany
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Right Column: Legal & Privacy */}
                        <div className="bg-gray-50 rounded-xl p-6 border border-gray-100 h-full">
                            <div className="flex items-center gap-2 mb-4">
                                <div className="relative w-5 h-5 flex-shrink-0 flex items-center justify-center">
                                    <Shield className="w-5 h-5 text-gray-600 absolute" />
                                    <Shield className="w-2.5 h-2.5 text-gray-600 fill-gray-600 absolute" />
                                </div>
                                <h3 className="text-base font-bold text-gray-900">Legal & Privacy</h3>
                            </div>

                            <div className="space-y-6 text-sm text-gray-600">
                                <div>
                                    <strong className="block text-gray-900 mb-1 text-xs uppercase tracking-wide">Privacy</strong>
                                    <p className="leading-relaxed">
                                        By contacting us, you acknowledge that your data will be processed for the purpose of handling your inquiry in accordance with our <Link to="/privacy" className="text-blue-600 hover:underline">Privacy Policy</Link>.
                                    </p>
                                </div>

                                <div>
                                    <strong className="block text-gray-900 mb-1 text-xs uppercase tracking-wide">Imprint</strong>
                                    <p className="leading-relaxed">
                                        For formal legal disclosures, please visit our <Link to="/imprint" className="text-blue-600 hover:underline">Imprint</Link>.
                                    </p>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}
