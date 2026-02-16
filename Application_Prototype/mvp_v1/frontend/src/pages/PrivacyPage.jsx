import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';
import { Shield, Lock, Server, Mail, FileText, UserCheck } from 'lucide-react';

const Section = ({ title, icon: Icon, children }) => (
    <section className="mb-8">
        <div className="flex items-center gap-3 mb-3">
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
                <Icon className="w-5 h-5" />
            </div>
            <h2 className="text-lg font-bold text-gray-900">{title}</h2>
        </div>
        <div className="pl-12 text-sm text-gray-600 space-y-3 leading-relaxed">
            {children}
        </div>
    </section>
);

export default function PrivacyPage() {
    useEffect(() => {
        document.title = "Privacy Policy | AI Compass";
    }, []);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-6 pt-28 pb-16 relative z-10">

                <PageHeader
                    title="Privacy Policy"
                    subtitle="LAST UPDATED: FEBRUARY 2026 | COMPLIANT WITH EU GDPR"
                />

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 md:p-12 grid md:grid-cols-2 gap-x-12 gap-y-6">

                    {/* 1. Controller */}
                    <Section title="1. Responsible Party (Controller)" icon={UserCheck}>
                        <p>The responsible party for data processing on this website is:</p>
                        <p className="font-semibold text-gray-900">
                            Christian Miething<br />
                            Görschstrasse 10A<br />
                            13187 Berlin, Germany<br />
                            <a href="mailto:chris@the-ai-compass.io" className="text-blue-600 hover:underline">chris@the-ai-compass.io</a>
                        </p>
                    </Section>

                    {/* 2. Data Collection & Hosting */}
                    <Section title="2. Hosting & Server Logs" icon={Server}>
                        <p>
                            We host this website on <strong>ISO 27001-certified servers located within the European Union</strong>.
                            The provider automatically collects and stores information in server log files (Browser, OS, Referrer URL, IP Address, Time)
                            for the purpose of ensuring technical stability and security (Art. 6 Para. 1 lit. f GDPR).
                        </p>
                    </Section>

                    {/* 3. AI Assessment Logic */}
                    <Section title="3. AI Compass Assessment Processing" icon={FileText}>
                        <p><strong>Input Data:</strong> When you use the AI Compass, we process the answers you provide in the assessment across 7 business dimensions (Strategy, Data Readiness, etc.) to calculate your maturity level.</p>

                        <p><strong>Automated Processing (Machine Learning):</strong></p>
                        <ul className="list-disc pl-5 space-y-1">
                            <li><strong>Clustering (K-Means):</strong> Assigns your profile to one of 5 maturity archetypes.</li>
                            <li><strong>Benchmarking (k-NN):</strong> Compares your data against anonymized peer entries to identify strategic gaps.</li>
                        </ul>
                        <p className="text-xs text-gray-500 mt-2">
                            *Note: This processing generates advisory insights and does not constitute "automated decision-making" with legal effects under Art. 22 GDPR.
                        </p>

                        <p className="mt-4"><strong>Lead Data:</strong> If you request a full report, we store your Name, Company, Industry, and Email Address based on your consent (Art. 6 Para. 1 lit. a GDPR) or for contract performance.</p>
                    </Section>

                    {/* 4. Processors (Brevo) */}
                    <Section title="4. Email Delivery (Brevo)" icon={Mail}>
                        <p>
                            For the reliable delivery of your assessment report, we use <strong>Brevo</strong> (formerly Sendinblue), a GDPR-compliant provider based in Berlin/Paris.
                        </p>
                        <p>
                            Your Email address and Name are transferred to Brevo solely for the purpose of sending the requested report. We have concluded a Data Processing Agreement (AVV) with the provider to ensure the security of your data.
                        </p>
                    </Section>

                    {/* 5. Security */}
                    <Section title="5. Data Security & Technical Measures" icon={Lock}>
                        <ul className="list-disc pl-5 space-y-2">
                            <li><strong>Encryption in Transit:</strong> All communication is protected by TLS 1.2/1.3 encryption (HTTPS).</li>
                            <li><strong>Secure Infrastructure:</strong> Data is stored on secure, access-controlled servers with strict firewall rules.</li>
                            <li><strong>Data Minimization:</strong> We only collect the specific data points required for the K-Means clustering algorithm.</li>
                            <li><strong>No Public LLM Training:</strong> We strictly do <strong>not</strong> use your customer data to train public Large Language Models (like GPT-4). Your intellectual property remains yours.</li>
                            <li><strong>Local Fonts:</strong> We host all fonts locally. No connection is made to Google Fonts servers.</li>
                        </ul>
                    </Section>

                    {/* 6. User Rights */}
                    <Section title="6. Your Rights" icon={Shield}>
                        <p>
                            You have the right to request access to, rectification of, or deletion of your personal data at any time.
                            You may also withdraw your consent for future processing. To exercise these rights, please contact the responsible party listed in Section 1.
                        </p>
                    </Section>

                </div>

            </main>

            <Footer />
        </div>
    );
}
