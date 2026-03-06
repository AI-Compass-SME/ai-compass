import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';
import { Shield, Lock, Server, Mail, FileText, UserCheck, EyeOff } from 'lucide-react';
import { useTranslation, Trans } from 'react-i18next';

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
    const { t } = useTranslation();

    useEffect(() => {
        document.title = `${t('pages.privacy.title')} | AI Compass`;
    }, [t]);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-6 pt-28 pb-16 relative z-10">

                <PageHeader
                    title={t('pages.privacy.title')}
                    subtitle={t('pages.privacy.subtitle')}
                />

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 md:p-12 grid md:grid-cols-2 gap-x-12 gap-y-6">

                    {/* 1. Controller */}
                    <Section title={t('pages.privacy.s1.title')} icon={UserCheck}>
                        <p>{t('pages.privacy.s1.p1')}</p>
                        <p className="font-semibold text-gray-900">
                            Christian Miething<br />
                            Görschstrasse 10A<br />
                            13187 Berlin, Germany<br />
                            <a href="mailto:chris@the-ai-compass.de" className="text-blue-600 hover:underline">chris@the-ai-compass.de</a>
                        </p>
                    </Section>

                    {/* 2. No Tracking */}
                    <Section title={t('pages.privacy.s2.title')} icon={EyeOff}>
                        <p>
                            <Trans i18nKey="pages.privacy.s2.p1">We respect your privacy. This website does <strong>not</strong> use tracking cookies, Google Analytics, or any other third-party user tracking services. We only utilize strictly necessary, functional cookies required for the interface to operate (e.g., sidebar status).</Trans>
                        </p>
                    </Section>

                    {/* 3. Hosting & Server Logs */}
                    <Section title={t('pages.privacy.s3.title')} icon={Server}>
                        <p>
                            <Trans i18nKey="pages.privacy.s3.p1">We host this website on <strong>ISO 27001-certified servers located within the European Union</strong>.
                                The provider automatically collects and stores information in server log files (Browser, OS, Referrer URL, IP Address, Time)
                                for the purpose of ensuring technical stability and security (Art. 6 Para. 1 lit. f GDPR).</Trans>
                        </p>
                    </Section>

                    {/* 4. AI Assessment Logic */}
                    <Section title={t('pages.privacy.s4.title')} icon={FileText}>
                        <p><Trans i18nKey="pages.privacy.s4.p1"><strong>Input Data:</strong> When you use the AI Compass, we process the answers you provide in the assessment across 7 business dimensions (Strategy, Data Readiness, etc.) to calculate your maturity level.</Trans></p>

                        <p><Trans i18nKey="pages.privacy.s4.p2"><strong>Automated Processing (Machine Learning):</strong></Trans></p>
                        <ul className="list-disc pl-5 space-y-1">
                            <li><Trans i18nKey="pages.privacy.s4.l1"><strong>Clustering (K-Means):</strong> Assigns your profile to one of 5 maturity archetypes.</Trans></li>
                            <li><Trans i18nKey="pages.privacy.s4.l2"><strong>Benchmarking (k-NN):</strong> Compares your data against anonymized peer entries to identify strategic gaps.</Trans></li>
                        </ul>
                        <p className="text-xs text-gray-500 mt-2">
                            {t('pages.privacy.s4.note')}
                        </p>

                        <p className="mt-4"><Trans i18nKey="pages.privacy.s4.p3"><strong>Lead Data:</strong> If you request a full report, we store your Name, Company, Industry, and Email Address based on your consent (Art. 6 Para. 1 lit. a GDPR) or for contract performance.</Trans></p>
                    </Section>

                    {/* 5. Processors (Brevo) */}
                    <Section title={t('pages.privacy.s5.title')} icon={Mail}>
                        <p>
                            <Trans i18nKey="pages.privacy.s5.p1">For the reliable delivery of your assessment report, we use <strong>Brevo</strong> (formerly Sendinblue), a GDPR-compliant provider based in Berlin/Paris.</Trans>
                        </p>
                        <p>
                            {t('pages.privacy.s5.p2')}
                        </p>
                    </Section>

                    {/* 6. Security */}
                    <Section title={t('pages.privacy.s6.title')} icon={Lock}>
                        <ul className="list-disc pl-5 space-y-2">
                            <li><Trans i18nKey="pages.privacy.s6.l1"><strong>Encryption in Transit:</strong> All communication is protected by TLS 1.2/1.3 encryption (HTTPS).</Trans></li>
                            <li><Trans i18nKey="pages.privacy.s6.l2"><strong>Secure Infrastructure:</strong> Data is stored on secure, access-controlled servers with strict firewall rules.</Trans></li>
                            <li><Trans i18nKey="pages.privacy.s6.l3"><strong>Data Minimization:</strong> We only collect the specific data points required for the K-Means clustering algorithm.</Trans></li>
                            <li><Trans i18nKey="pages.privacy.s6.l4"><strong>No Public LLM Training:</strong> We strictly do <strong>not</strong> use your customer data to train public Large Language Models (like GPT-4). Your intellectual property remains yours.</Trans></li>
                            <li><Trans i18nKey="pages.privacy.s6.l5"><strong>Local Fonts:</strong> We host all fonts locally. No connection is made to Google Fonts servers.</Trans></li>
                        </ul>
                    </Section>

                    {/* 7. User Rights */}
                    <Section title={t('pages.privacy.s7.title')} icon={Shield}>
                        <p>
                            {t('pages.privacy.s7.p1')}
                        </p>
                    </Section>

                </div>

            </main>

            <Footer />
        </div>
    );
}
