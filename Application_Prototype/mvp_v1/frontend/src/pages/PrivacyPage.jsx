import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';
import { Shield, Lock, Server, Mail, FileText, UserCheck, EyeOff, Building2 } from 'lucide-react';
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

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 md:p-12 space-y-10">

                    <p className="text-gray-600 text-sm italic border-l-4 border-blue-500 pl-4 py-1">
                        {t('pages.privacy.intro')}
                    </p>

                    <div className="grid md:grid-cols-2 gap-x-12 gap-y-10">
                        {/* 1. Controller */}
                        <Section title={t('pages.privacy.s1.title')} icon={UserCheck}>
                            <p>{t('pages.privacy.s1.p1')}</p>
                            <p className="font-semibold text-gray-900">
                                {t('pages.privacy.s1.address')}<br />
                                <a href="mailto:info@the-ai-compass.de" className="text-blue-600 hover:underline inline-flex items-center gap-1 mt-1">
                                    <Mail className="w-3 h-3" /> info@the-ai-compass.de
                                </a>
                            </p>
                        </Section>

                        {/* 2. Brevo (now in position 2) */}
                        <Section title={t('pages.privacy.s4.title')} icon={Mail}>
                            <p>{t('pages.privacy.s4.p1')}</p>
                        </Section>

                        {/* 3. Assessment & ML */}
                        <Section title={t('pages.privacy.s3.title')} icon={FileText}>
                            <div className="space-y-4">
                                <div>
                                    <h3 className="font-bold text-gray-900 text-xs uppercase tracking-wider mb-1">{t('pages.privacy.s3.h1')}</h3>
                                    <p>{t('pages.privacy.s3.p1')}</p>
                                    <p className="text-xs font-medium text-blue-700 mt-1">{t('pages.privacy.s3.purpose1')}</p>
                                    <p className="text-[10px] text-gray-500 leading-tight">{t('pages.privacy.s3.legal1')}</p>
                                </div>

                                <div>
                                    <h3 className="font-bold text-gray-900 text-xs uppercase tracking-wider mb-1">{t('pages.privacy.s3.h2')}</h3>
                                    <p>{t('pages.privacy.s3.p2')}</p>
                                    <ul className="list-disc pl-5 space-y-1 mt-1">
                                        <li><Trans i18nKey="pages.privacy.s3.l1"><strong>Clustering (K-Means):</strong> Assigns your profile...</Trans></li>
                                        <li><Trans i18nKey="pages.privacy.s3.l2"><strong>Benchmarking (k-NN):</strong> Compares your data...</Trans></li>
                                    </ul>
                                    <p className="text-[10px] text-gray-400 mt-2 leading-tight">{t('pages.privacy.s3.note')}</p>
                                </div>

                                <div>
                                    <h3 className="font-bold text-gray-900 text-xs uppercase tracking-wider mb-1">{t('pages.privacy.s3.h3')}</h3>
                                    <p>{t('pages.privacy.s3.p3')}</p>
                                    <p className="text-xs font-medium text-blue-700 mt-1">{t('pages.privacy.s3.purpose3')}</p>
                                    <p className="text-[10px] text-gray-500 leading-tight">{t('pages.privacy.s3.legal3')}</p>
                                </div>
                            </div>
                        </Section>

                        {/* 4. Hosting (now in position 4) */}
                        <Section title={t('pages.privacy.s2.title')} icon={Server}>
                            <p>{t('pages.privacy.s2.p1')}</p>
                            <p className="mt-2">{t('pages.privacy.s2.p2')}</p>
                            <ul className="list-disc pl-5 space-y-1 mt-1">
                                <li>{t('pages.privacy.s2.l1')}</li>
                                <li>{t('pages.privacy.s2.l2')}</li>
                                <li>{t('pages.privacy.s2.l3')}</li>
                            </ul>
                            <p className="text-xs text-gray-500 mt-2 italic">{t('pages.privacy.s2.footer')}</p>
                        </Section>

                        {/* 5. Security */}
                        <Section title={t('pages.privacy.s5.title')} icon={Lock}>
                            <ul className="list-disc pl-5 space-y-2">
                                <li><Trans i18nKey="pages.privacy.s5.l1"><strong>Verschlüsselung:</strong> ...</Trans></li>
                                <li><Trans i18nKey="pages.privacy.s5.l2"><strong>Kein LLM-Training:</strong> ...</Trans></li>
                                <li><Trans i18nKey="pages.privacy.s5.l3"><strong>Lokale Fonts:</strong> ...</Trans></li>
                                <li><Trans i18nKey="pages.privacy.s5.l4"><strong>Datenminimierung:</strong> ...</Trans></li>
                            </ul>
                        </Section>

                        {/* 6. User Rights */}
                        <Section title={t('pages.privacy.s6.title')} icon={Shield}>
                            <p>{t('pages.privacy.s6.p1')}</p>
                            <ul className="list-disc pl-5 space-y-1 mt-2">
                                <li>{t('pages.privacy.s6.l1')}</li>
                                <li>{t('pages.privacy.s6.l2')}</li>
                                <li>{t('pages.privacy.s6.l3')}</li>
                                <li>{t('pages.privacy.s6.l4')}</li>
                            </ul>
                        </Section>

                        {/* 7. Analytics */}
                        <Section title={t('pages.privacy.s7.title')} icon={EyeOff}>
                            <p>{t('pages.privacy.s7.p1')}</p>
                            <ul className="list-disc pl-5 space-y-1 mt-2">
                                <li>{t('pages.privacy.s7.l1')}</li>
                                <li>{t('pages.privacy.s7.l2')}</li>
                                <li>{t('pages.privacy.s7.l3')}</li>
                                <li>{t('pages.privacy.s7.l4')}</li>
                            </ul>
                            <p className="text-xs text-gray-500 mt-3 italic">{t('pages.privacy.s7.footer')}</p>
                        </Section>

                        {/* 8. AVV */}
                        <Section title={t('pages.privacy.s8.title')} icon={Building2}>
                            <p>{t('pages.privacy.s8.p1')}</p>
                        </Section>
                    </div>
                </div>

            </main>

            <Footer />
        </div>
    );
}
